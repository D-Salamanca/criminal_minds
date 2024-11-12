import logging
import socket
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from datetime import datetime


logger = logging.getLogger("KAFKA CONSUMER LOGGER")


connection_conf = {
    "bootstrap.server":"localhost:9092",
    "client.id": socket.gethostname() 
    }


topic = "criminaltopic"


try:
    logger.info("Start Consumer connection")
    consumer = Consumer(connection_conf)
    consumer.subscribe(topic)
except KafkaError as e:
    logger.error(f"[{datetime.now()}] The consumer could not connect to the topic {topic}")
    logger.error(e)
