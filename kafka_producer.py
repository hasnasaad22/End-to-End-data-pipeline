from kafka import KafkaProducer
import pandas as pd
import json
import time
import requests
import threading

# ================= KAFKA SETUP =================
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
            print(f"Kafka not ready... retry {i} | {e}")
            time.sleep(5)

    raise Exception("Failed to connect to Kafka")


producer = create_producer()
topic_name = "weather-events"


# ================= CSV DATA =================
df = pd.read_csv("data.csv")

def clean_value(v):
    return None if pd.isna(v) else v


def send_csv():
    for _, row in df.iterrows():

        record = {
            "source": "csv",
            "temperature": clean_value(row["temperature"]),
            "humidity": clean_value(row["humidity"]),
            "rolling_temp": clean_value(row["rolling_temp"]),
            "timestamp": time.time()
        }

        try:
            producer.send(topic_name, value=record)
            print("CSV Sent ✔️ ->", record)
        except Exception as e:
            print("CSV ERROR:", e)

        time.sleep(2)


# ================= API (Open-Meteo) =================
api_url = "https://api.open-meteo.com/v1/forecast?latitude=30.04&longitude=31.24&current_weather=true"

def fetch_weather():
    try:
        r = requests.get(api_url, timeout=5)
        data = r.json()

        if "current_weather" not in data:
            print("API error:", data)
            return None

        return {
            "location": "Munuf / Egypt",
            "temperature": data["current_weather"]["temperature"],
            "windspeed": data["current_weather"]["windspeed"],
            "timestamp": time.time()
        }

    except Exception as e:
        print("API ERROR:", e)
        return None


def send_api():
    while True:

        api_data = fetch_weather()

        if api_data:
            record = {
                "source": "api",
                "city": api_data["location"],
                "temperature": api_data["temperature"],
                "windspeed": api_data["windspeed"],
                "timestamp": api_data["timestamp"]
            }

            try:
                producer.send(topic_name, value=record)
                print("API Sent ✔️ ->", record)
            except Exception as e:
                print("API ERROR (Kafka):", e)

        time.sleep(5)


# ================= MAIN =================
if __name__ == "__main__":

    t1 = threading.Thread(target=send_csv)
    t2 = threading.Thread(target=send_api)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    producer.flush()
    producer.close()