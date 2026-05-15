from kafka import KafkaConsumer
import json
import psycopg2
import pandas as pd


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

# Create schema
cursor.execute("CREATE SCHEMA IF NOT EXISTS bronze;")

# Create table
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

    # safe NaN handling
    for key, value in data.items():
        if pd.isna(value):
            data[key] = None

    try:
        cursor.execute("""
            INSERT INTO bronze.weather_raw (raw_json)
            VALUES (%s)
        """, (json.dumps(data),))

        conn.commit()
        print("Inserted ✔️ ->", data)

    except Exception as e:
        print("DB Error:", e)
        conn.rollback()