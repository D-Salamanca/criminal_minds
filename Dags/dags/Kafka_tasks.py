import os
import json
import logging
from datetime import datetime
import time
from confluent_kafka import Producer
import pandas as pd

logger = logging.getLogger("[KAFKA_PRODUCER:logs]")

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} at offset {msg.offset()}")


def start_produce(**kwargs: json) -> None:
    ti = kwargs["ti"]
    xcom_value = ti.xcom_pull(task_ids="Extract_data")
    if xcom_value is None:
        raise ValueError("XCom returned None, check the 'Extract_data' task.")
     
    json_charge = json.loads(xcom_value)
    data = pd.json_normalize(data=json_charge)
    logger.info(f"{data.head(5)} - Data loaded")
    conf = {
        'bootstrap.servers': 'localhost:9092'
    }
    topic = "criminal_topic"
    producer = Producer(conf)

    for index, row in data.iterrows():
        data_dict = row.to_dict()
        data_json = json.dumps(data_dict)
        producer.produce(topic, value=data_json.encode('utf-8'), callback=delivery_report)
        producer.poll(0)
        time.sleep(2)

