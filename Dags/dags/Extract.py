# Extract.py
import sys
sys.path.append("/home/joan/Desktop/Proyect-ETL/criminal_minds/src")
from db_connection import conn  # Import the engine instead of conn
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker 
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("[Extracts:logs]")

def Extract() -> json:
    try:
        engine = conn.engine
        Session = sessionmaker(bind=engine)
        session = Session()
        q = "SELECT * FROM criminal_mind_raw"
        # Use the SQLAlchemy engine
        df = pd.read_sql(sql=q, con=engine)
        logger.info(f"[{datetime.now()}] - Postgres Connected -- data-loaded -- ")
        result = df.to_json(orient="records")
        print(df.head(5))
        return result
    except Exception as err:
        logger.error(f"[{datetime.now()}]: {err}")
        raise Exception("The Data wasn't load")
        
