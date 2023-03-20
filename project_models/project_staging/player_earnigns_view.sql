{{ config(materialized='view') }}

select 
PlayerId,
NameFirst as First_Name,
NameLast as Last_Name,
CurrentHandle as Gamer_Tag,
CountryCode as Country_Code,
cast(TotalUSDPrize as numeric) as Total_USD_Earnings,
Game,
Genre
from {{ source('project_staging','player_earnings_optimized') }}