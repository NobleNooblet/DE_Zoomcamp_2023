{{ config(materialized='table') }}

with country_codes as (
    select *
    from {{ ref('country_codes_view')}}
),

player_earnings as (
    select *
    from {{ ref('player_earnings_view')}}
)
Select 
player_earnings.PlayerId,
player_earnings.First_Name,
player_earnings.Last_Name,
player_earnings.Gamer_Tag,
player_earnings.Country_Code,
player_earnings.Total_USD_Earnings,
player_earnings.Game,
player_earnings.Genre,
country_codes.Continent_Name,
country_codes.Continent_Code,
country_codes.Country_Name
from 
player_earnings 
inner join 
country_codes
on player_earnings.Country_Code = country_codes.Country_Code