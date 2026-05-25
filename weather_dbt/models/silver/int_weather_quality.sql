with base as (

    select *
    from {{ ref('stg_weather') }}

)

select
    temperature,
    humidity,
    ingestion_time,

    -- flag for missing data
    case 
        when temperature is null or humidity is null then 1
        else 0
    end as is_missing,

    -- basic validation rules
    case 
        when temperature < -50 or temperature > 60 then 1
        else 0
    end as temp_out_of_range,

    case 
        when humidity < 0 or humidity > 100 then 1
        else 0
    end as humidity_out_of_range

from base