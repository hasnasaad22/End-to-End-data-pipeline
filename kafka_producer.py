from kafka import KafkaProducer
import pandas as pd
import json
import time


def create_producer():
    for i in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers='127.0.0.1:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5
            )
            print("Connected to Kafka ✅")
            return producer
        except Exception as e:
            print(f"Kafka not ready... retry {i}")
            time.sleep(5)

    raise Exception("Failed to connect to Kafka")


producer = create_producer()

topic_name = "weather-events"

df = pd.read_csv("data.csv")


def send_data():
    for _, row in df.iterrows():

        # build record
        record = {
            "temperature": float(row["temperature"]),
            "humidity": float(row["humidity"]),
            "rolling_temp": row["rolling_temp"]
        }

        # 🔥 handle NaN safely
        for key in record:
            if pd.isna(record[key]):
                record[key] = None

        try:
            # async send (faster + production style)
            producer.send(topic_name, value=record)

            print("Sent ✔️ ->", record)

        except Exception as e:
            print("Send ERROR:", e)

        time.sleep(1)

    # ensure all messages are sent
    producer.flush()
    producer.close()


if __name__ == "__main__":
    send_data()