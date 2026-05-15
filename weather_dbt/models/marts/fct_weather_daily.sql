select
    date(ingestion_time) as date,
    avg(temperature) as avg_temperature,
    avg(humidity) as avg_humidity
from {{ ref('weather_clean') }}
group by 1