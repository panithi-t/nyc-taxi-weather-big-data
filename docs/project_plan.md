# Project Plan
 
**Project Title:** Cloud-Scale Analysis of NYC Taxi Operations Under Different Weather Conditions  
**Author:** Panithi Tawethipong

---

# 1. Project Overview

## Background

New York City generates millions of taxi trips every month, producing one of the largest publicly available urban transportation datasets. At the same time, weather conditions such as heavy rain, snow, extreme temperatures, and reduced visibility can significantly influence travel demand, traffic conditions, and passenger behavior. Furthermore, socio-economic factors like neighborhood wealth and real estate values add an additional layer of complexity to these patterns. Understanding these relationships can help transportation agencies, fleet operators, and city planners better anticipate demand and improve operational efficiency.

This project will analyze large-scale NYC Yellow Taxi trip records together with historical New York City weather observations and Kaggle NYC housing market data using Apache Spark. The analysis will first be developed locally using a small subset of the data and then deployed to AWS cloud infrastructure to process more than 100 million taxi trip records.

## Project Objectives

The primary objectives of this project are:

- Build a scalable Spark analytics pipeline for large transportation datasets.
- Integrate multiple public datasets through meaningful joins.
- Evaluate how weather conditions influence taxi demand and trip characteristics.
- Deploy the same analytics pipeline to AWS using cloud-native storage and query services.
- Demonstrate reproducible cloud infrastructure using Terraform.

# 2. Datasets

This project integrates four publicly available datasets that can be joined to analyze how weather and socio-economic factors influence taxi operations in New York City. The primary dataset consists of NYC Yellow Taxi trip records, while historical weather observations provide environmental context. A housing market dataset provides local real estate values, and a fourth lookup table maps taxi zone IDs to boroughs and neighborhoods for geographic analysis.

---

## Dataset 1: NYC TLC Yellow Taxi Trip Records

**Source:** New York City Taxi and Limousine Commission (TLC)

**Format:** Monthly Parquet files

**Scale:** Millions of trip records per month; the final cloud deployment will process over 100 million trip records.

### Key Fields

- Pickup timestamp
- Dropoff timestamp
- Pickup Location ID
- Dropoff Location ID
- Passenger count
- Trip distance
- Fare amount
- Tip amount
- Total amount
- Payment type

### Purpose

This dataset serves as the primary source for analyzing taxi demand, trip duration, revenue, passenger behavior, and travel efficiency.

---

## Dataset 2: Historical NYC Weather

**Source:** National Oceanic and Atmospheric Administration (NOAA)

**Format:** CSV

**Scale:** Hourly historical weather observations covering the same time period as the taxi data.

### Key Fields

- Observation timestamp
- Temperature
- Precipitation
- Wind speed
- Visibility
- Weather condition

### Purpose

This dataset provides environmental variables that may influence taxi demand, traffic conditions, and passenger behavior.

---

## Dataset 3: NYC Taxi Zone Lookup

**Source:** NYC Taxi and Limousine Commission (TLC)

**Format:** CSV

### Key Fields

- Location ID
- Borough
- Zone
- Service Zone

### Purpose

This lookup table maps pickup and dropoff location IDs to geographic areas, allowing borough-level and neighborhood-level analysis.

---

## Dataset 4: NYC Housing Market Data (Kaggle)

**Source:** Kaggle (nelgiriyewithana/new-york-housing-market)

**Format:** CSV

### Key Fields

- PRICE
- BEDS / BATH
- PROPERTYSQFT
- TYPE (Condo, Co-op, Townhouse)
- LATITUDE / LONGITUDE
- LOCALITY / SUBLOCALITY

### Purpose

This dataset provides socio-economic and real estate value indicators for different areas, allowing us to map wealth and property types to taxi demand behavior.

---

## Dataset Integration

The datasets will be integrated through two joins.

### Time-Based Join

Taxi trips will be matched with weather observations by truncating pickup timestamps to the nearest hour.

```
Taxi pickup timestamp
        ↓
Round to hour
        ↓
Hourly weather observation
```

### Geographic & Spatial Join

Taxi pickup and dropoff Location IDs will be joined with the Taxi Zone Lookup table to identify the corresponding borough and zone. Concurrently, the Housing Market Data will be spatially joined to the Taxi Zones based on Latitude and Longitude to calculate median property values and types per zone.

The resulting integrated dataset will enable analyses of taxi demand, revenue, trip duration, and passenger behavior under different weather conditions and socio-economic contexts across New York City.

# 3. Research Questions and Planned Analytics

The primary goal of this project is to quantify how weather conditions and socio-economic factors affect taxi operations in New York City. Using Apache Spark, the integrated dataset will be analyzed through large-scale spatial joins, aggregation, and filtering.

---

## Research Question 1

### Weather Resilience by Wealth

Do high-value real estate neighborhoods show less variance in taxi demand during severe weather compared to lower-value areas?

### Planned Analytics

- Spatially join housing data with TLC Taxi Zones
- Categorize neighborhoods by average property price
- Compare hourly demand drop-offs during rain/snow across wealth tiers

**Expected Output**

- Demand elasticity curves by neighborhood wealth
- Comparison of high vs low real estate value areas during storms

---

## Research Question 2

### The "Luxury Tip" Weather Effect

How does tipping behavior change during adverse weather, and is the percentage increase significantly higher in wealthy neighborhoods?

### Planned Analytics

- Calculate average tip percentage for trips dropping off in different zones
- Analyze tip variance during bad weather, segmented by the destination's median property value

**Expected Output**

- Average tip percentage by weather condition and wealth tier
- Tipping behavior heatmaps

---

## Research Question 3

### Property Type & Airport Travel

Do neighborhoods dominated by large single-family homes show different travel patterns to airports during bad weather than dense condo/co-op areas?

### Planned Analytics

- Use the `TYPE` and `PROPERTYSQFT` fields to categorize neighborhoods
- Analyze trip volumes to JFK and LaGuardia during rain/snow

**Expected Output**

- Airport travel volume comparisons across property types

---

## Research Question 4

### Pricing Surge Tolerance

When weather-induced delays increase fare costs (due to longer durations), are trips originating from high-price localities more resilient to these cost surges?

### Planned Analytics

- Calculate weather-induced fare premiums (duration delays)
- Measure the demand impact of these premiums across different neighborhood wealth tiers

**Expected Output**

- Price elasticity of demand across different weather conditions and wealth brackets

---

## Research Question 5

### General Operations

How does weather broadly affect hourly taxi demand, trip duration, and average travel speeds across the city?

### Planned Analytics

- Calculate average trip duration and speed
- Compare normal weather versus rain and snow city-wide

**Expected Output**

- Average trip duration and speed by weather condition
- Speed distribution and peak-hour comparison

---

## Summary of Planned Spark Analytics

The project will make extensive use of Apache Spark DataFrame operations and Spark SQL to perform:

- Large-scale joins across multiple datasets
- Aggregation using hourly, daily, and borough-level summaries
- Statistical comparisons across weather categories
- Feature engineering, including trip duration, estimated speed, temperature categories, and precipitation levels
- Cloud-scale processing of more than 100 million taxi trip records

# 4. Data Preprocessing Pipeline

Before performing analytics, both the taxi and weather datasets will undergo a preprocessing pipeline to improve data quality and ensure reliable analytical results. The preprocessing steps are designed to satisfy the project requirements while preparing the data for efficient large-scale processing in Apache Spark.

---

## 4.1 Missing Value Treatment

The first stage of preprocessing will identify missing or incomplete records in both datasets.

### Taxi Dataset

- Remove records missing essential fields such as pickup timestamp or pickup location.
- Review missing passenger count and payment type values and determine whether imputation or removal is more appropriate based on the frequency of missing data.

### Weather Dataset

- Fill small gaps in hourly weather observations using neighboring observations when appropriate.
- Missing precipitation values will be reviewed carefully before replacement to avoid introducing inaccurate weather conditions.

The percentage of missing values before and after preprocessing will be reported.

---

## 4.2 Outlier Detection and Treatment

The taxi dataset may contain invalid or unrealistic trips caused by data entry errors or sensor issues.

Examples include:

- Negative fare amounts
- Negative trip distances
- Extremely long trip durations
- Unrealistically high travel speeds
- Invalid passenger counts

Summary statistics and visual inspection will be used to identify outliers. Invalid observations will either be removed or capped using clearly documented rules.

---

## 4.3 Feature Normalization

Continuous numerical variables will be normalized where appropriate to improve consistency across variables and support potential machine learning extensions.

Examples include:

- Trip distance
- Trip duration
- Fare amount
- Temperature
- Wind speed

The normalization method will be selected based on the distribution of each variable.

---

## 4.4 Categorical Encoding

Several categorical variables will be encoded to improve analytical processing.

Examples include:

- Weather condition
- Payment type
- Borough
- Day of week
- Time of day

Encoding allows efficient grouping and comparison during Spark-based analytics.

---

## 4.5 Feature Binning

Continuous variables will be grouped into meaningful categories to simplify comparisons and improve interpretability.

Examples include:

### Temperature

- Very Cold
- Cold
- Mild
- Warm
- Hot

### Precipitation

- None
- Light
- Moderate
- Heavy

### Trip Distance

- Short
- Medium
- Long
- Very Long

### Time of Day

- Overnight
- Morning
- Afternoon
- Evening

These categories will support aggregated analyses and comparisons across different operating conditions.

---

## Preprocessing Summary

The completed preprocessing pipeline will produce a clean, integrated dataset suitable for cloud-scale analytics. The impact of each preprocessing step will be documented using summary statistics and record counts before and after processing.

# 5. Cloud Architecture and Technology Stack

The project will be developed using a local Apache Spark environment before being deployed to AWS for cloud-scale processing. This approach allows rapid development on small datasets while ensuring that the same analytics pipeline can scale to process more than 100 million taxi trip records.

---

## Overall Architecture

```
                 Public Datasets
        ┌─────────────────────────────┐
        │  NYC Taxi Trips (Parquet)   │
        │  NOAA Weather (CSV)         │
        │  Taxi Zone Lookup (CSV)     │
        └──────────────┬──────────────┘
                       │
                       ▼
              Apache Spark (PySpark)
      Data Cleaning • Feature Engineering
          Data Integration • Analytics
                       │
                       ▼
                 Amazon S3 Storage
             Processed Parquet Files
                       │
                       ▼
                 Amazon Athena
              Interactive SQL Queries
                       │
                       ▼
          Analysis, Results, and Reports
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Apache Spark (PySpark) | Distributed data processing and analytics |
| Docker | Local Spark development environment |
| Amazon S3 | Cloud storage for raw and processed datasets |
| Amazon Athena | Serverless SQL querying of processed data |
| Terraform | Infrastructure as Code (IaC) for AWS resources |
| GitHub | Source code management and version control |
| Python | Data processing and Spark application development |

---

## Local Development

The project will first be implemented locally using the course's Dockerized Spark environment. A small subset of the taxi and weather datasets will be used during development to allow rapid testing and debugging.

Developing locally reduces cloud costs while allowing the preprocessing pipeline, joins, and analytical queries to be validated before processing the full dataset.

---

## Cloud Deployment

After the local pipeline has been validated, the same Spark application will be deployed to AWS.

The cloud deployment will:

- Store raw datasets in Amazon S3.
- Process data using Apache Spark.
- Store cleaned datasets as Parquet files.
- Execute analytical SQL queries through Amazon Athena.
- Support processing of more than 100 million taxi trip records.

Using the same Spark pipeline for both local and cloud execution ensures reproducibility while minimizing changes between development and production environments.

---

## Infrastructure as Code

AWS resources will be provisioned using Terraform to ensure the cloud environment can be recreated consistently.

The infrastructure will include:

- Amazon S3 bucket(s)
- Athena workgroup
- Query results location
- Additional cloud resources provided by the course starter project

Using Infrastructure as Code improves reproducibility, simplifies deployment, and follows modern cloud engineering best practices.

---

## Cost Management

Because cloud computing resources incur usage charges, several strategies will be used to minimize costs:

- Develop locally whenever possible.
- Store processed data in compressed Parquet format.
- Partition large datasets where appropriate.
- Limit unnecessary Athena scans.
- Destroy cloud resources after project completion using Terraform.

# 6. Project Timeline, Deliverables, and Expected Outcomes

This project will be completed in two major phases. The first phase focuses on planning and validating the project design, while the second phase implements the complete cloud-scale analytics pipeline.

---

## Phase 1 – Project Planning (July 25)

By the project proposal deadline, the following components will be completed:

- Project scope and objectives
- Selection of public datasets
- Research questions
- Data preprocessing plan
- Cloud architecture design
- Technology stack selection
- GitHub repository initialization
- Project documentation

The purpose of this phase is to demonstrate that the proposed project is technically feasible and satisfies the course requirements.

---

## Phase 2 – Final Implementation (August 1)

The final project will include:

- Complete Apache Spark preprocessing pipeline
- Integration of multiple public datasets
- Cross-source analytical queries
- Cloud deployment using AWS
- Processing of more than 100 million taxi trip records
- Public GitHub repository containing source code, infrastructure, documentation, and execution instructions
- Final presentation and live demonstration

---

## Planned Project Deliverables

The final GitHub repository will include:

- Source code for data ingestion and preprocessing
- Spark analytics pipeline
- SQL queries
- Terraform infrastructure
- Project documentation
- Presentation slides
- Results and discussion
- Setup and execution instructions

---

## Planned Extension

To strengthen the project beyond the required coursework, the project will include the following optional extension:

### Query Performance Tuning

Performance will be evaluated by comparing different storage and processing strategies, including:

- CSV versus Parquet
- Partitioned versus non-partitioned datasets
- Query execution time
- Amount of data scanned
- Storage efficiency

This extension demonstrates practical big-data optimization techniques commonly used in production cloud environments.

---

## Expected Outcomes

Upon completion, the project is expected to:

- Demonstrate an end-to-end cloud-scale analytics workflow using Apache Spark and AWS.
- Successfully integrate multiple public datasets into a unified analytical dataset.
- Quantify the relationship between weather conditions and NYC taxi operations.
- Produce reproducible analytical results using scalable cloud infrastructure.
- Demonstrate modern data engineering practices including Infrastructure as Code, distributed processing, and cloud-native analytics.

---

## Current Progress

| Task | Status |
|------|--------|
| Project topic selected | ✅ Completed |
| Public GitHub repository created | ✅ Completed |
| Repository structure initialized | ✅ Completed |
| Project documentation | ✅ In Progress |
| Dataset selection | ✅ Completed |
| Research questions defined | ✅ Completed |
| Local Spark setup | ⬜ Planned |
| Data preprocessing pipeline | ⬜ Planned |
| AWS cloud deployment | ⬜ Planned |
| Cloud-scale analytics | ⬜ Planned |
| Final presentation | ⬜ Planned |
