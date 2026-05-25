from kafka import KafkaConsumer
import json
import psycopg2
from psycopg2.extras import Json

consumer = KafkaConsumer(
    'weather-events',
    bootstrap_servers='127.0.0.1:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather-group-1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    host="127.0.0.1",
    database="airflow_db",
    user="airflow",
    password="airflow"
)

cursor = conn.cursor()

cursor.execute("CREATE SCHEMA IF NOT EXISTS bronze;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bronze.weather_raw (
    id SERIAL PRIMARY KEY,
    raw_json JSONB,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

print("Consumer started")

for message in consumer:

    data = message.value

    clean_data = {
        k: (None if v != v else v)
        for k, v in data.items()
    }

    try:
        cursor.execute("""
            INSERT INTO bronze.weather_raw (raw_json)
            VALUES (%s)
        """, (Json(clean_data),))

        conn.commit()

        print(f"Inserted from {clean_data.get('source')} ✔️ ->", clean_data)

    except Exception as e:
        print("DB Error:", e)
        conn.rollback()