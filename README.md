---

# Proyecto ETL - Análisis de Crímenes en Los Ángeles

Este proyecto se enfoca en el análisis de datos de crímenes reportados en Los Ángeles desde el año 2020, utilizando un enfoque de ETL (Extract, Transform, Load) para transformar y visualizar la información de manera eficiente.

## Descripción del Proyecto

El objetivo principal es extraer los datos de un archivo CSV, transformarlos para su limpieza y normalización, cargarlos en una base de datos relacional, y luego realizar un análisis exploratorio de datos (EDA) junto con la generación de visualizaciones interactivas para identificar patrones de criminalidad.

## Tecnologías Utilizadas

- **Python**: Utilizado para la manipulación y análisis de datos.
- **Jupyter Notebooks**: Empleado para documentar y ejecutar el proceso de análisis de datos.
- **PostgreSQL**: Base de datos relacional utilizada para almacenar los datos transformados.
- **Power BI**: Herramienta de visualización utilizada para crear reportes interactivos.
- **SQLAlchemy**: Utilizado para la conexión y operaciones con la base de datos PostgreSQL.
- **Docker**: Utilizado para desplegar bases de datos y diferentes herramientas como kafka para este proyecto
- **AIRFLOW**
- **KAFKA**

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

   Ejecuta el siguiente comando para instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configura la base de datos**:
   - Setear las variables de entorno de docker y pgadmin y quitar la extecion de eschema `Database/docker-secrets` & `Database/docker-secrets-pgadmin`
   - Levanta el contenedor `Database/docker-compose.yaml`.
     ```bash
     cd Database
     docker-compose up -d
      ```
   - Correr el Notebook de precarga de los datos `Notebooks/preload.ipynb`
   
5. **Configura Kafka**:
   - Levanta el contenedor `kafka/docker-compose.yaml`.
     ```bash
     cd kafka
     docker-compose up -d
      ```
   - Crear el topic
     ```bash
     docker exex -it <container_kafka_name> kafka-topics --create --topic criminaltopic --bootstrap-server localhost:9092
     ```

6. **Cofigurar Airflow**:
   - Dentro del entorno virtual de python instalar Airflow `!Debe ser un sistema basado en unix`
     ```bash
     source ruta/entorno/virtual/bin/activate
     source set_airflow_var.sh
     
     pip install apache-airflow
     ```

   - Correr Airflow
     ```bash
     source set_airflow_var.sh
     airflow standalone
     ```
   - Verificar que esta el DAG `Proyect_ETL_Criminal_Minds`
   
## Uso del Proyecto

### 1. Preparación de los Datos

Ejecuta el notebook `Notebooks/pre_load.ipynb` para cargar los datos del archivo CSV y realizar la limpieza inicial.

### 2. Migración de Datos a la Base de Datos

Después de la limpieza, migra los datos a PostgreSQL ejecutando el script `src/db_connection.py`:

```bash
python src/db_connection.py
```

### 3. Análisis Exploratorio de Datos (EDA)

Realiza el análisis exploratorio de datos abriendo y ejecutando el notebook `Notebooks/EDA.ipynb`. Aquí se generarán visualizaciones clave basadas en los datos almacenados en la base de datos.

### 4. Visualización en Power BI

Importa los datos desde PostgreSQL a Power BI para crear visualizaciones interactivas que reflejen los patrones de criminalidad en Los Ángeles.

## Estructura del Proyecto

- **Data/**: Carpeta destinada a los archivos de datos (actualmente vacía).
- **Notebooks/**: Contiene los notebooks de Jupyter para el análisis y exploración de datos.
- **src/**: Contiene el script para la conexión y migración de datos a la base de datos.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el proyecto.
- **README.md**: Documento que estás leyendo, con instrucciones para configurar y utilizar el proyecto.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-característica`).
3. Realiza los cambios necesarios.
4. Haz commit de los cambios (`git commit -am 'Añadí una nueva característica'`).
5. Haz push a la rama (`git push origin feature/nueva-característica`).
6. Crea un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
