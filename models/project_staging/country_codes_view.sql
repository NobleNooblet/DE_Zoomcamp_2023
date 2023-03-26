{{ config(materialized='view') }}

-- select 
-- Continent_Name,
-- Continent_Code,
-- Country_Name,
-- lower(Two_Letter_Country_Code) as Country_Code
-- from {{ source('project_staging','country_codes_optimized') }}

WITH distinct_country_codes as (
  select 
  Continent_Name,
  Continent_Code,
  Country_Name,
   lower(coalesce(Two_Letter_Country_Code,'na')) as Country_Code,
   RANK() OVER(PARTITION BY lower(Two_Letter_Country_Code) ORDER BY Continent_Name) as Rank 
 from {{ source('project_staging','country_codes_optimized') }}
)
select 
Continent_Name,
Continent_Code,
Country_Name,
Country_Code
FROM distinct_country_codes dcc
where dcc.Rank = 1