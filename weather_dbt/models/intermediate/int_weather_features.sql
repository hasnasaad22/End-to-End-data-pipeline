select
    ingestion_time,
    temperature,
    humidity,
    (temperature * 1.8 + 32) as temperature_fahrenheit
from {{ ref('weather_clean') }}