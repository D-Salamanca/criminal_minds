import json
import logging
import socket
import sys
sys.path.append("Elastic_search")
from index import (
    elastic_create_index,
    elastic_send_data
)
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from datetime import datetime


logger = logging.getLogger("KAFKA CONSUMER LOGGER")


connection_conf = {
    "bootstrap.server":"localhost:9092",
    "client.id": socket.gethostname() ,
    'group.id': 'mi_grupo_consumidor',
    'auto.offset.reset': 'latest'
    }

topic = "criminaltopic"


try:
    logger.info("Start Consumer connection")
    consumer = Consumer(connection_conf)
    consumer.subscribe(topic)
    index_name="ETLP3"
    elastic_create_index(index_name=index_name)
    while True:
        msg = consumer.poll(1)
        
        if msg == None:
            continue
        
        if msg.error():
            logger.error("Error with the messages")
            logger.error(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
            break

        data = json.loads(msg.value().decode('utf-8'))
        logger.info(f"Received message as dict: {data}")
        elastic_send_data(data=data, index_name=index_name)
        consumer.commit(msg)


except KafkaError as e:
    logger.error(f"[{datetime.now()}] The consumer could not connect to the topic {topic}")
    logger.error(e)

finally:
    consumer.close()
