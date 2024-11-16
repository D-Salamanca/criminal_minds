# Extract.py
import sys
sys.path.append("/criminal_minds/src")
from db_connection import conn  # Import the engine instead of conn
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker 
import json
import logging

logger = logging.getLogger("[Extracts:logs]")

def Extract() -> str:
    session = None
    try:
        engine = conn.engine
        Session = sessionmaker(bind=engine)
        session = Session()
        q = "SELECT * FROM criminal_mind_raw"
        df = pd.read_sql(sql=q, con=engine)
        logger.info(f"[{datetime.now()}] - Postgres Connected -- data-loaded -- ")
        result = df.to_json(orient="records")
        logger.info(f"Data Sample:\n{df.head(5)}")
        return result
    except Exception as err:
        logger.error(f"[{datetime.now()}]: {err}")
        raise Exception("The data wasn't loaded") from err
    finally:
        if session:
            session.close()
        
        
