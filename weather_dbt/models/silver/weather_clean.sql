SELECT
    raw_json->>'source' AS source,
    (raw_json->>'temperature')::float AS temperature,
    (raw_json->>'humidity')::int AS humidity,
    ingestion_time
FROM bronze.weather_raw