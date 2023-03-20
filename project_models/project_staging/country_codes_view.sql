{{ config(materialized='view') }}
select 
Continent_Name,
Continent_Code,
Country_Name,
lower(Two_Letter_Country_Code) as Country_Code
from {{ source('project_staging','country_codes_optimized') }}