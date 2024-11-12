from confluent_kafka import Producer
import socket
import logging

logger = logging.getLogger("KAFKA PRODUCER LOGGER")


connection_conf = {
        'bootstrap.server': "localhost:9092",
        'client.id': socekt.gethostname()
        }

producer = Producer(connection_conf)



try:
    producer.produce(topic, value='value')
    producer.flush()

except KafkaException:
    logger.error("The message dont was send")
    











def producer_task():
    pass
