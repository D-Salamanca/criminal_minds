# Proyecto ETL - Análisis de Crímenes en Los Ángeles

Este proyecto se enfoca en el análisis de datos de crímenes reportados en Los Ángeles desde el año 2020, utilizando un enfoque de ETL (Extract, Transform, Load) y herramientas modernas como Apache Airflow y Apache Kafka para procesar y transmitir datos, con visualizaciones interactivas creadas en Power BI.

## Descripción del Proyecto
El objetivo principal es construir un pipeline ETL que extrae datos de un archivo CSV y una API externa (CPI by Industry), limpia y normaliza los datos, y los carga en una base de datos relacional. Además, implementamos un sistema de transmisión en tiempo real con Kafka y visualizaciones interactivas para identificar patrones de criminalidad.

## Tecnologías Utilizadas

- **Python**: Para la manipulación y análisis de datos.
- **Jupyter Notebooks**: Documentación y ejecución de análisis de datos.
- **PostgreSQL**: Base de datos relacional para almacenar los datos transformados.
- **Power BI**: Herramienta de visualización para crear reportes interactivos.
- **Apache Airflow**: Orquestación de tareas ETL.
- **Apache Kafka**: Transmisión de datos en tiempo real.
- **SQLAlchemy**: Conexión y operaciones con la base de datos PostgreSQL.
- **Docker**: Contenedorización de la infraestructura, incluyendo bases de datos y Kafka.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas:

- Python 3.12
- Jupyter Notebook
- Docker
- Git

## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/etl-crime-analysis.git
   cd etl-crime-analysis
   ```

2. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos**:
   - Configura las variables de entorno para Docker y pgAdmin. Ajusta `Database/docker-secrets` y `Database/docker-secrets-pgadmin` según sea necesario.
   - Levanta el contenedor de la base de datos:
     ```bash
     cd Database
     docker-compose up -d
     ```
   - Ejecuta el notebook `Notebooks/preload.ipynb` para precargar los datos en PostgreSQL.

4. **Configura Kafka**:
   - Levanta el contenedor de Kafka:
     ```bash
     cd kafka
     docker-compose up -d
     ```
   - Crea el topic de Kafka:
     ```bash
     docker exec -it <nombre_del_contenedor_kafka> kafka-topics --create --topic criminaltopic --bootstrap-server localhost:9092
     ```

5. **Configura Airflow**:
   - Activa tu entorno virtual de Python y configura Airflow (recomendado en sistemas basados en Unix):
     ```bash
     source /ruta/a/tu/entorno/virtual/bin/activate
     source set_airflow_var.sh
     pip install apache-airflow
     ```
   - Ejecuta Airflow:
     ```bash
     source set_airflow_var.sh
     airflow standalone
     ```
   - Verifica que el DAG `Proyect_ETL_Criminal_Minds` esté disponible en la interfaz de Airflow.

## Uso del Proyecto

### 1. Preparación de los Datos
Ejecuta el notebook `Notebooks/pre_load.ipynb` para cargar y limpiar los datos del archivo CSV.

### 2. Migración de Datos a la Base de Datos
Ejecuta el script `src/db_connection.py` para migrar los datos limpios a PostgreSQL:

```bash
python src/db_connection.py
```

### 3. Análisis Exploratorio de Datos (EDA)
Realiza el análisis exploratorio abriendo y ejecutando el notebook `Notebooks/EDA.ipynb`. Aquí se generan visualizaciones clave a partir de los datos almacenados en la base de datos.

### 4. Visualización en Power BI
Importa los datos desde PostgreSQL a Power BI y crea reportes interactivos que visualicen los patrones de criminalidad.

## Estructura del Proyecto

- **Data/**: Carpeta para los archivos de datos (actualmente vacía).
- **Notebooks/**: Contiene los notebooks de Jupyter para análisis y exploración.
- **src/**: Contiene scripts de conexión y migración de datos.
- **Database/**: Configuraciones y secretos para la base de datos PostgreSQL y pgAdmin.
- **kafka/**: Configuración de Kafka y docker-compose para transmisión de datos.
- **requirements.txt**: Lista de dependencias necesarias.
- **README.md**: Documento con instrucciones de configuración y uso.

## Contribuciones

Las contribuciones son bienvenidas. Sigue estos pasos para contribuir:

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-característica`).
3. Realiza los cambios.
4. Haz commit (`git commit -am 'Añadí una nueva característica'`).
5. Haz push (`git push origin feature/nueva-característica`).
6. Crea un Pull Request.

