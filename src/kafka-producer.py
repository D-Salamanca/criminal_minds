import logging
import os
import socket
from confluent_kafka import Producer
from confluent_kafka import KafkaException

logger = logging.getLogger("KAFKA PRODUCER LOGGER")
topic = "criminaltopic"

connection_conf = {
        'bootstrap.server': "localhost:9092",
        'client.id': socket.gethostname()
        }

producer = Producer(connection_conf)




def producer_task():
    pass



if __name__ == "__main__":

    try:
        producer.produce(topic, value='value')
        producer.flush()

    except KafkaException:
        logger.error("The message dont was send")