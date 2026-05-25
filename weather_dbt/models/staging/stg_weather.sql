with source as (

    select
        raw_json,
        ingestion_time
    from {{ source('bronze', 'weather_raw') }}

)

select
    nullif(raw_json->>'source','') as source,

    case 
        when raw_json->>'temperature' in ('', 'null', 'None', 'NA')
        then null
        else (raw_json->>'temperature')::float
    end as temperature,


    case 
        when raw_json->>'humidity' in ('', 'null', 'NA') then null
        else raw_json->>'humidity'::float
    end
      

    ingestion_time

from source