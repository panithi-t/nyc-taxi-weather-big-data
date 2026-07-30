# Cloud-Scale Analysis of NYC Taxi Operations Under Different Weather Conditions

**Big Data Analytics at Cloud Scale**

**Author:** Panithi Tawethipong

---

## Project Overview

This project investigates how weather conditions and neighborhood real estate values influence New York City's taxi operations using Apache Spark and AWS cloud infrastructure.

By combining large-scale NYC Taxi & Limousine Commission (TLC) trip records with historical weather observations and NYC housing market data, this project analyzes how rain, snow, temperature, and local wealth affect:

- Taxi demand and resilience to severe weather
- Trip duration and estimated travel speed
- Revenue and socio-economic tipping behavior
- Real estate-driven travel patterns

The project is developed locally using Apache Spark before being deployed to AWS for cloud-scale analytics on over **100 million taxi trip records**.

---

## Research Questions

This project aims to answer the following core questions:

1. **Weather Resilience by Wealth:** Do high-value real estate neighborhoods show less variance in taxi demand during severe weather compared to lower-value areas?
2. **The "Luxury Tip" Weather Effect:** How does tipping behavior change during adverse weather, and is the percentage increase significantly higher in wealthy neighborhoods?
3. **Property Type & Airport Travel:** Do neighborhoods dominated by large single-family homes show different travel patterns to airports during bad weather than dense condo/co-op areas?
4. **Pricing Surge Tolerance:** When weather-induced delays increase fare costs, are trips originating from high-price localities more resilient to these cost surges?
5. **General Operations:** How does weather broadly affect hourly taxi demand, trip duration, and average travel speeds across the city?

---

## Datasets

### 1. NYC TLC Yellow Taxi Trip Records

Primary dataset containing millions of taxi trips.

Example fields:

- pickup_datetime
- dropoff_datetime
- trip_distance
- fare_amount
- tip_amount
- total_amount
- passenger_count
- PULocationID

---

### 2. Historical NYC Weather

Historical hourly weather observations including:

- temperature
- precipitation
- wind speed
- visibility
- weather condition

---

### 3. NYC Housing Market Data (Kaggle)

Dataset containing real estate listings across New York City.

Example fields:
- PRICE
- BEDS / BATH
- PROPERTYSQFT
- TYPE (Condo, Co-op, Townhouse)
- LATITUDE / LONGITUDE
- LOCALITY / SUBLOCALITY

---

### 4. NYC Taxi Zone Lookup

Lookup table mapping taxi zones to boroughs.

---

## Technology Stack

- Apache Spark (PySpark)
- Docker
- AWS S3
- AWS Athena
- Terraform
- GitHub
- Python

---

## Planned Architecture

```
Public Datasets
        │
        ▼
   Apache Spark
(Data Cleaning & Joins)
        │
        ▼
      AWS S3
        │
        ▼
   AWS Athena
(SQL Analytics)
        │
        ▼
Results & Insights
```

---

## Preprocessing Pipeline

The preprocessing stage will include:

- Missing value treatment
- Outlier detection and removal
- Feature normalization
- Categorical encoding
- Feature binning

---

## Planned Analytics

Example analyses include:

- Spatial joins mapping housing coordinates to TLC Taxi Zones
- Taxi demand resilience by weather and neighborhood real estate value
- Tipping percentage variance segmented by weather and destination property value
- Average trip duration and travel speed drops during adverse weather
- Borough and neighborhood-level socio-economic comparisons

---

## Repository Structure

```
docs/
src/
sql/
slides/
results/
data/
infrastructure/
```

---

## Project Timeline

- **July 25:** Project proposal and scope review
- **August 1:** Final Spark pipeline, AWS deployment, presentation, and demo

---

## Current Status

✅ Repository created

✅ Project scope selected

⬜ Local Spark implementation

⬜ AWS deployment

⬜ Cloud-scale execution

⬜ Final presentation
