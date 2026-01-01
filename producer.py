import json
import time
import random
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

cities = ["Delhi", "Mumbai", "Bangalore", "Chennai"]

while True:
    event = {
        "user_id": random.randint(1, 1000),
        "age": random.randint(18, 65),
        "income": random.randint(25000, 150000),
        "city": random.choice(cities),
        "timestamp": int(time.time())
    }

    producer.send("user_events", value=event)
    print("Sent:", event)
    time.sleep(1)