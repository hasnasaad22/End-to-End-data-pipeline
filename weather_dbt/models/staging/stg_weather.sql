with source as (

    select
        raw_json,
        ingestion_time
    from {{ source('bronze', 'weather_raw') }}

)

select
    (raw_json->>'temperature')::float as temperature,
    (raw_json->>'humidity')::float as humidity,
    ingestion_time
from source