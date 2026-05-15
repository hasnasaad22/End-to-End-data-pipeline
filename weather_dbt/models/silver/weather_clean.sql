select
    temperature,
    humidity,
    ingestion_time
from {{ ref('stg_weather') }}
where temperature is not null