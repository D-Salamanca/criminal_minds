import sys
sys.path.append("/home/joan/Desktop/Proyect-ETL/criminal_minds/src")
import os
import json
import logging
from datetime import datetime
from db_connection import conn  # Import the engine instead of conn
import requests
import pandas as pd
from sqlalchemy.orm import sessionmaker 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[API:logs]")

def Extract() -> json:
    url = "https://apps.bea.gov/api/data"
    api_key = os.getenv("API_KEY")
    params = {
        "UserID": api_key,
        "method": "GetData",
        "datasetname": "GDPbyIndustry",
        "TableName": "ALL",
        "Year": "2017,2018,2019,2020,2021",  # Datos de los últimos 5 años
        "Frequency": "A",  # Datos anuales
        "Industry": "ALL",  # Todas las industrias
        "TableID": "ALL",  # Todas las tablas
        "ResultFormat": "json"
    }

    response = requests.get(url, params=params) 

    if response.status_code == 200:
        logger.info("Response OK")
        try:
            data = response.json().get("BEAAPI")["Results"][0]["Data"]

            if data != None:
                df = pd.DataFrame((i for i in data))
                results = df.to_json(orient="records")
                return results
        except KeyError:
            logger.error("Data is not found")
            raise Exception("Someting wrong in the extract api task")
        finally:
            logger.info(f"[{datetime.now()}] - Data loaded")


def Transform (**kwargs: json) -> json:
    ti = kwargs["ti"]
    xcom_value = ti.xcom_pull(task_ids="Extract_data")
    if xcom_value is None:
        raise ValueError("XCom returned None, check the 'Extract_data' task.")
     
    json_charge = json.loads(xcom_value)
    data = pd.json_normalize(data=json_charge)
    data.drop(columns=['Quarter', 'TableID', 'NoteRef'], inplace=True, errors='ignore')

    # Renombrar columnas para estandarización
    data.rename(columns={
        'Frequency': 'frequency',
        'Year': 'year',
        'Industry': 'industry',
        'IndustrYDescription': 'industry_description',
        'DataValue': 'data_value'
    }, inplace=True)

    # Verificar valores únicos en 'frequency' y eliminar la columna si solo hay un valor
    if data['frequency'].nunique() == 1:
        data.drop(columns=['frequency'], inplace=True)

    # Eliminar filas duplicadas, si existen
    data.drop_duplicates(inplace=True)

    # Diccionario para agrupar categorías en sectores amplios
    industry_groups = {
        # Sector Primario
        'Agriculture, forestry, fishing, and hunting': 'Sector Primario',
        'Farms': 'Sector Primario',
        'Forestry, fishing, and related activities': 'Sector Primario',
        'Mining': 'Sector Primario',
        'Oil and gas extraction': 'Sector Primario',
        'Mining, except oil and gas': 'Sector Primario',
        'Support activities for mining': 'Sector Primario',

        # Sector Secundario
        'Manufacturing': 'Sector Secundario',
        'Food and beverage and tobacco products': 'Sector Secundario',
        'Textile mills and textile product mills': 'Sector Secundario',
        'Apparel and leather and allied products': 'Sector Secundario',
        'Petroleum and coal products': 'Sector Secundario',
        'Chemical products': 'Sector Secundario',
        'Wood products': 'Sector Secundario',
        'Paper products': 'Sector Secundario',
        'Machinery': 'Sector Secundario',
        'Motor vehicles, bodies and trailers, and parts': 'Sector Secundario',
        'Durable goods': 'Sector Secundario',
        'Nondurable goods': 'Sector Secundario',

        # Sector Terciario
        'Wholesale trade': 'Sector Terciario',
        'Retail trade': 'Sector Terciario',
        'Air transportation': 'Sector Terciario',
        'Rail transportation': 'Sector Terciario',
        'Truck transportation': 'Sector Terciario',
        'Warehousing and storage': 'Sector Terciario',
        'Information': 'Sector Terciario',
        'Publishing industries, except internet (includes software)': 'Sector Terciario',
        'Motion picture and sound recording industries': 'Sector Terciario',
        'Data processing, internet publishing, and other information services': 'Sector Terciario',

        # Sector Cuaternario
        'Professional, scientific, and technical services': 'Sector Cuaternario',
        'Legal services': 'Sector Cuaternario',
        'Computer systems design and related services': 'Sector Cuaternario',
        'Management of companies and enterprises': 'Sector Cuaternario',
        'Educational services': 'Sector Cuaternario',
        'Health care and social assistance': 'Sector Cuaternario',

        # Sector Público
        'Government': 'Sector Público',
        'Federal': 'Sector Público',
        'State and local': 'Sector Público',
        'General government': 'Sector Público',
        'National defense': 'Sector Público',
        'Nondefense': 'Sector Público',

        # Bienes Raíces y Servicios Financieros
        'Finance and insurance': 'Bienes Raíces y Servicios Financieros',
        'Real estate and rental and leasing': 'Bienes Raíces y Servicios Financieros',
        'Insurance carriers and related activities': 'Bienes Raíces y Servicios Financieros',
        'Federal Reserve banks, credit intermediation, and related activities': 'Bienes Raíces y Servicios Financieros',
        'Funds, trusts, and other financial vehicles': 'Bienes Raíces y Servicios Financieros',

        # Energía y Servicios Públicos
        'Utilities': 'Energía y Servicios Públicos',
        'Pipeline transportation': 'Energía y Servicios Públicos',

        # Grandes industrias
        'Private industries': 'industria privada',
        'Compensation of employees': 'compensacion a empleados',
        'Taxes on production and imports less subsidies': 'tax y subsidios',
        
        # Otros
        'Gross domestic product': 'Otros',
        'Gross operating surplus': 'Otros',
    }

    # Crear la nueva columna con la agrupación
    data['sector_group'] = data['industry_description'].map(industry_groups)
    
    return data


def Load(**kwargs: json) -> None:
    ti = kwargs["ti"]
    xcom_value = ti.xcom_pull(task_ids="Extract_data")
    if xcom_value is None:
        raise ValueError("XCom returned None, check the 'Extract_data' task.")
     
    json_charge = json.loads(xcom_value)
    data = pd.json_normalize(data=json_charge)
    try:
        engine = conn.engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        data.to_sql("api_data", con=engine, if_exists='append', index=False)
    except:
        print("except")
    finally:
        session.close()