{{ config(materialized='view') }}

select
    -- identifiers
    {{ dbt_utils.surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    cast(PUlocationID as integer) as PUlocationID,
    cast(DOlocationID as integer) as DOlocationID,
    SR_Flag,
    Affiliated_base_number
from {{ source('staging','fhv_2019') }}