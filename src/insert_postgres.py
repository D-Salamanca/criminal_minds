import os
import requests
import psycopg2
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de la API desde la variable de entorno
api_key = os.getenv('BEA_API_KEY')

# Obtener la configuración de la base de datos desde las variables de entorno
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Definir la URL de la API de BEA
url = "https://apps.bea.gov/api/data"

# Parámetros de la solicitud para obtener datos de GDP por industria
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

# Realizar la solicitud GET a la API de BEA
response = requests.get(url, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error en la solicitud. Código de estado: {response.status_code}")
    exit()

# Verificar si la respuesta contiene datos
if 'Results' in data['BEAAPI']:
    results = data['BEAAPI']['Results'][0]['Data']
else:
    print("No se encontraron datos en la respuesta.")
    exit()

# Conectar a la base de datos PostgreSQL
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")
    exit()

# Crear la tabla para los datos sucios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pib_sucio (
        id SERIAL PRIMARY KEY,
        table_id INT,
        frequency VARCHAR(10),
        year VARCHAR(4),
        quarter VARCHAR(10),
        industry VARCHAR(50),
        industry_description VARCHAR(255),
        data_value VARCHAR(50),
        note_ref VARCHAR(50)
    );
''')

# Insertar los datos sucios en la tabla 'pib_sucio'
for record in results:
    try:
        cursor.execute('''
            INSERT INTO pib_sucio (table_id, frequency, year, quarter, industry, industry_description, data_value, note_ref)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        ''', (
            record.get('TableID'),
            record.get('Frequency'),
            record.get('Year'),
            record.get('Quarter'),
            record.get('Industry'),
            record.get('IndustrYDescription'),
            record.get('DataValue'),
            record.get('NoteRef')
        ))
    except Exception as e:
        print(f"Error al insertar el registro: {e}")

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Datos sucios insertados correctamente en la base de datos.")
