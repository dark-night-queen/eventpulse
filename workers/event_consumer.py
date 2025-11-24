# Standard Library imports
import time
from loguru import logger

# App imports
from apps.common.kafka.consumer import KafkaConsumer


consumer = KafkaConsumer(
    group_id="test-group",
    topics=["events"],
)

logger.info("Listening for events...")

try:
    while True:
        msg = consumer.poll_message()
        if msg:
            logger.info(f"Received: {msg}")
        time.sleep(0.1)
except KeyboardInterrupt:
    logger.warning("Shutting down consumer...")
finally:
    consumer.close()
    logger.info("Consumer closed.")
