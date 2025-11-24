# Standard Library imports
import json
from confluent_kafka import Producer

# Settings imports
from configs.settings import KAFKA_BOOTSTRAP_SERVERS


class KafkaProducer:
    """
    Design Pattern: Facade
        This gives you:
        - a clean API (send_message(...))
        - decoupling from the Confluent client
        - easier swapping (e.g., Redpanda → Kafka cluster → mock producer)
    """

    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send_message(self, topic: str, message: any, key: str = None):
        if not isinstance(message, str):
            message = json.dumps(message)

        self.producer.produce(
            topic,
            message.encode("utf-8"),
            key=key.encode("utf-8") if key else None,
        )

    def flush(self):
        self.producer.flush()
