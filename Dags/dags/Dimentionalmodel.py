# Dimentionalmodel.py
import sys
sys.path.append("/criminal_minds/src")
from db_connection import conn  # Import the engine.connect()
import pandas as pd
from datetime import datetime
import json
import logging
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[Charge:logs]")

def load_to_postgres(**kwargs):
    try:
        logger.info(f"[{datetime.now()}] -- Start to charge")
        
        # Extraer el valor de XCom
        ti = kwargs["ti"]
        xcom_value = ti.xcom_pull(task_ids="Extract_data")
        
        # Verificar si el valor de XCom no es None
        if xcom_value is None:
            logger.error("XCom returned None, check the 'Extract_data' task.")
            raise ValueError("XCom returned None, check the 'Extract_data' task.")
        
        logger.info(f"[{datetime.now()}] -- XCom Value: {xcom_value[:500]}...")  # Mostrar solo una parte del JSON
        
        # Cargar el JSON
        json_charge = json.loads(xcom_value)
        df = pd.json_normalize(data=json_charge)
    
        # Cargar la tabla "Area"
        Area = df[["AREA","AREA NAME"]].drop_duplicates()
        Area.sort_values(by="AREA", inplace=True)
        Area.rename(columns={"AREA NAME": "Area_name", "AREA": "Area_id"}, inplace=True)
        engine = conn.engine
        Session = sessionmaker(bind=engine)
        session = Session()
        Area.to_sql(name="area", con=engine, if_exists='replace', index=False)
        logger.info(f"[{datetime.now()}] -- charge Area")

        # Cargar la tabla "Status"
        Status = df[["Status","Status Desc"]].drop_duplicates()
        Status.reset_index(inplace=True)
        Status.drop(columns="index", inplace=True)
        Status.rename(columns={"Status Desc": "Status_Desc", "Status": "Status_id"}, inplace=True)
        Status.to_sql(name="status", con=engine, if_exists='replace', index=False)
        logger.info(f"[{datetime.now()}] -- charge status")

        # Cargar la tabla "Weapon"
        Weapon = df[["Weapon Used Cd", "Weapon Desc"]].drop_duplicates()
        Weapon.rename(columns={"Weapon Used Cd": "Weapon_id", "Weapon Desc": "Weapon_description"}, inplace=True)
        Weapon.sort_values("Weapon_id", ascending=True, inplace=True)
        Weapon.to_sql(name="weapon", con=engine, if_exists='replace', index=False)
        logger.info(f"[{datetime.now()}] -- charge weapon")

        # Cargar la tabla "Premis"
        Premis = df[["Premis Cd", "Premis Desc"]].drop_duplicates()
        Premis.rename(columns={"Premis Cd": "Premis_id", "Premis Desc": "Premis_description"}, inplace=True)
        Premis.sort_values("Premis_id", inplace=True)
        Premis.to_sql(name="premis", con=engine, if_exists='replace', index=False)
        logger.info(f"[{datetime.now()}] -- charge premis")

    except Exception as err:
        logger.error(f"[{datetime.now()}] - Error occurred: {err}")
        raise Exception("The task wasn't complete")
    except ValueError as err:
        logger.error(f"X-com null")
    finally:
        session.close()

