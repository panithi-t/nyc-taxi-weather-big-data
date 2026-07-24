# Cloud-Scale Analysis of NYC Taxi Operations Under Different Weather Conditions

**Big Data Analytics at Cloud Scale**

**Author:** Panithi Tawethipong

---

## Project Overview

This project investigates how weather conditions influence New York City's taxi operations using Apache Spark and AWS cloud infrastructure.

By combining large-scale NYC Taxi & Limousine Commission (TLC) trip records with historical weather observations, this project analyzes how rain, snow, temperature, and other weather conditions affect:

- Taxi demand
- Trip duration
- Estimated travel speed
- Revenue
- Passenger tipping behavior

The project is developed locally using Apache Spark before being deployed to AWS for cloud-scale analytics on over **100 million taxi trip records**.

---

## Research Questions

This project aims to answer the following questions:

1. How does weather affect hourly taxi demand?
2. Does adverse weather increase trip duration?
3. How does weather affect average travel speed?
4. How does weather influence taxi revenue?
5. Does weather affect passenger tipping behavior?

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

### 3. NYC Taxi Zone Lookup

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

- Taxi demand by weather condition
- Revenue by weather condition
- Average trip duration
- Average travel speed
- Borough-level comparisons
- Hourly demand trends

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
