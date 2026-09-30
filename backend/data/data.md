                    ┌── NRSC
                    ├── Census
                    ├── IMD
                    ├── OSM
                    ├── SRTM
                    └── Sentinel

#### this is the data layer we are using for real time data.


## ISRO / NRSC Bhuvan
NRSC Disaster Management Support- https://www.nrsc.gov.in/nrscnew/Services_Bhuvan_Disaster_Management_Support.php?utm_source=chatgpt.com

NDEM Disaster GIS Portal-https://ndem.nrsc.gov.in/#/

Bhuvan Disaster Services- https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php?utm_source=chatgpt.com

You can get
Flood inundation
Flood hazard zones
Historical flood layers
Landslide inventories
Landslide hazard information
Earthquake information
Forest-fire information
Disaster event information
River gauges
Some infrastructure/settlement layers

## IMD API — rainfall and weather
https://mausam.imd.gov.in/responsive/rainfallinformation_state.php
The official API provides:

District rainfall
State rainfall
Current weather
AWS/ARG station data
District warnings
Forecasts
Subdivision rainfall forecasts
River-basin quantitative precipitation forecasts
Weather observations


## Census of India — population/vulnerability

This is another source I strongly recommend.

[Census India Data Portal](https://censusindia.gov.in/census.website/en)

[Census API use guidelines](https://censusindia.gov.in/census.website/en/data/api)

The linked page currently exposes only the heading "Guidelines on API use"; it does not expose a callable endpoint, authentication requirements, response schema, or example population request. No Census API integration is configured until those details are available.

The Population Finder provides village-level indicators including:

Total population
Male/female population
Age groups
Scheduled caste/tribe population
Households
Work status
Other demographic indicators

## SRTM / DEM — elevation and slope

For your landslide model, elevation is extremely important.

## Verified live access and limitations

- IMD's district rainfall map currently embeds dated district observations in a public page response. The dashboard reads the actual, normal, departure, and report date fields from [the IMD district rainfall page](https://mausam.imd.gov.in/responsive/rainfallinformation/rfi_district.inc.php) and caches them for 30 minutes. This is an observed daily rainfall overlay, not an official documented API contract; the page structure may change.
- The IMD API portal at https://api.imd.gov.in provides registration and login. API credentials and a selected API product are needed before using its documented API as a production feed.
- Bhuvan's public WMS GetCapabilities endpoint (https://bhuvan-vec1.nrsc.gov.in/bhuvan/gwc/service/wms/?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities) responds with a layer catalog. WMS can supply map imagery, but the listed portal links do not establish a feature-download API or access to every disaster layer. NDEM states that its content is intended for authorized users. No NRSC data is used in automated scoring.
- OSM's Overpass endpoint (https://overpass-api.de/api/interpreter) accepts queries and returns current mapped features as JSON; a hospital-feature query was verified. OSM is licensed under ODbL, and local feature coverage must be checked before using missing features as evidence of poor access. It can support mapped infrastructure overlays, but does not provide validated capacity or vulnerability scores.
- `2011_population.xlsx` contains Census A-1 totals at state, district, and subdistrict levels, not village rows. The system matches 15 of 18 pilot blocks to Uttarakhand Census subdistricts by district and name (including explicit spelling aliases). Those 2011 totals size relocation scenarios and related resource requirements; unmatched blocks fall back to the prototype village estimate. Per-village population/vulnerability, site capacities, and resource inventory remain prototype values.
- The linked Census API guide still does not expose an endpoint or schema. No SRTM/DEM or Sentinel download endpoints are included either. Live rainfall is displayed separately and does not change risk scores or relocation recommendations; a validated rainfall-to-hazard model and verified village-level inputs are needed before it should drive those decisions.