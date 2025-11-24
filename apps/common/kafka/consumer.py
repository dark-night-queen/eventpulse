# Standard Library imports
import json
from confluent_kafka import Consumer

# Settings imports
from configs.settings import KAFKA_BOOTSTRAP_SERVERS


class KafkaConsumer:
    def __init__(
        self,
        group_id: str,
        topics: list,
        bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset: str = "earliest",
    ):
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": auto_offset_reset,
            }
        )
        self.subscribe(topics or [])

    def subscribe(self, topics: list):
        self.consumer.subscribe(topics)

    def poll_message(self, timeout: float = 1.0):
        msg = self.consumer.poll(timeout)
        if msg is None:
            return None

        if msg.error():
            raise msg.error()

        return {
            "topic": msg.topic(),
            "key": msg.key().decode("utf-8") if msg.key() else None,
            "value": json.loads(msg.value().decode("utf-8")),
            "partition": msg.partition(),
            "offset": msg.offset(),
        }

    def close(self):
        self.consumer.close()
