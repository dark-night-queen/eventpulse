from confluent_kafka import Consumer

c = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "test-group",
        "auto.offset.reset": "earliest",
    }
)

c.subscribe(["events"])

print("Listening...")

while True:
    msg = c.poll(1.0)
    if msg is None:
        continue
    print("Received:", msg.value().decode("utf-8"))
