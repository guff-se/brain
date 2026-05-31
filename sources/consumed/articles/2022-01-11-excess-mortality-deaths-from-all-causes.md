---
title: "Excess mortality: Deaths from all causes compared to projection"
summary: "Excess mortality: Deaths from all causes compared to projection
What you should know about this indicator
- Excess death…"
kind: "article"
party: "third"
register: "consumed"
source: "web"
source_id: "fb-1641927098"
url: "https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline?tab=map&time=2020-10-11&country=MEX~RUS~ZAF"
provenance: "extracted"
enrichment: "ok"
lang: "en"
tags: [excess-mortality, public-health, epidemiology]
status: "reference"
ingested: "2026-05-31"
created: "2022-01-11"
---

Excess mortality: Deaths from all causes compared to projection
What you should know about this indicator
- Excess deaths is estimated as Excess deaths = Number of reported deaths - Number of expected deaths. Excess mortality goes beyond confirmed COVID-19 fatalities by capturing all deaths above a projected baseline, including indirect deaths from pandemic-related disruptions.
- All-cause mortality data is from the Human Mortality Database (HMD) Short-term Mortality Fluctuations project and the World Mortality Dataset (WMD). Both sources are updated weekly.
- We use the baseline estimates by Ariel Karlinsky and Dmitry Kobak (2021) as part of their World Mortality Dataset (WMD).
- We do not use the data from some countries in WMD because they fail to meet the following data quality criteria: 1) at least three years of historical data; and 2) data published either weekly or monthly. The full list of excluded countries and reasons for exclusion can be found in this spreadsheet.
Related research and writing
Sources and processing
This data is based on the following sources
How we process data at Our World in Data
All data and visualizations on Our World in Data rely on data sourced from one or several original data providers. Preparing this original data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
At the link below you can find a detailed description of the structure of our data pipeline, including links to all the code used to prepare data across Our World in Data.
Reuse this work
Citations
How to cite this page
To cite this page overall, including any descriptions, FAQs or explanations of the data authored by Our World in Data, please use the following citation:
“Data Page: Excess mortality: Deaths from all causes compared to projection”. Our World in Data (2026). Data adapted from Human Mortality Database, Karlinsky and Kobak. Retrieved from https://archive.ourworldindata.org/20260524-063525/grapher/excess-mortality-p-scores-projected-baseline.html [online resource] (archived on May 24, 2026).
How to cite this data
In-line citationIf you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:
Human Mortality Database (2026); Karlinsky and Kobak (2021) – processed by Our World in Data
Full citation
Human Mortality Database (2026); Karlinsky and Kobak (2021) – processed by Our World in Data. “Excess mortality: Deaths from all causes compared to projection” [dataset]. Human Mortality Database, “Short-term Mortality Fluctuations”; Karlinsky and Kobak, “World Mortality Dataset”; Karlinsky and Kobak, “Excess mortality during the COVID-19 pandemic” [original data]. Retrieved May 25, 2026 from https://archive.ourworldindata.org/20260524-063525/grapher/excess-mortality-p-scores-projected-baseline.html (archived on May 24, 2026).
Download
Quick download
Download the data shown in this chart as a ZIP file containing a CSV file, metadata in JSON format, and a README. The CSV file can be opened in Excel, Google Sheets, and other data analysis tools.
Data API
Use these URLs to programmatically access this chart's data and configure your requests with the options below. Our documentation provides more information on how to use the API, and you can find a few code examples below.
Data URL (CSV format)
https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.csv?v=1&csvType=full&useColumnShortNames=false
Metadata URL (JSON format)
https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.metadata.json?v=1&csvType=full&useColumnShortNames=false
Excel / Google Sheets
=IMPORTDATA("https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.csv?v=1&csvType=full&useColumnShortNames=false")
Python with Pandas
import pandas as pd
import requests
# Fetch the data.
df = pd.read_csv("https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.csv?v=1&csvType=full&useColumnShortNames=false", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
# Fetch the metadata
metadata = requests.get("https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()
R
library(jsonlite)
# Fetch the data
df <- read.csv("https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.csv?v=1&csvType=full&useColumnShortNames=false")
# Fetch the metadata
metadata <- fromJSON("https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.metadata.json?v=1&csvType=full&useColumnShortNames=false")
Stata
import delimited "https://ourworldindata.org/grapher/excess-mortality-p-scores-projected-baseline.csv?v=1&csvType=full&useColumnShortNames=false", encoding("utf-8") clear
