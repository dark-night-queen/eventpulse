import time
from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092"})

for i in range(5):
    msg = f"test event {i}"
    p.produce("events", msg.encode("utf-8"))
    print("Sent:", msg)
    time.sleep(1)

p.flush()
