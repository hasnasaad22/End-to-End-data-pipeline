select
    date(ingestion_time) as date,
    avg(temperature) as avg_temperature,
    avg(humidity) as avg_humidity,
    avg(temperature_fahrenheit) as avg_temperature_fahrenheit
from {{ ref('weather_metrics_staging') }}
group by 1