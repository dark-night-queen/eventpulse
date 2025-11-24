# Standard Library imports
import time

# App imports
from apps.common.kafka.consumer import KafkaConsumer


consumer = KafkaConsumer(
    group_id="test-group",
    topics=["events"],
)

print("Listening for events...")

while True:
    msg = consumer.poll_message()
    if msg:
        print("Received:", msg)
    time.sleep(0.1)
