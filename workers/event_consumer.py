# Standard Library imports
from loguru import logger

# App imports
from apps.common.kafka.consumer import KafkaConsumer
from workers.base_consumer import BaseWorker


class EventConsumerWorker(BaseWorker):
    group_id: str = "test-group"
    topics: list[str] = ["events"]

    def setup(self):
        self.consumer = KafkaConsumer(self.group_id, self.topics)
        logger.info("Listening for events...")

    def process(self):
        msg = self.consumer.poll_message()
        if msg:
            logger.info(f"Received: {msg}")

    def cleanup(self):
        self.consumer.close()
        logger.info("Kafka consumer closed.")


if __name__ == "__main__":
    consumer = EventConsumerWorker()
    consumer.run()
