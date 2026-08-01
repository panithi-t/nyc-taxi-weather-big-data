# Cloud-Scale Analysis of NYC Taxi Operations Under Different Weather Conditions
**A Socioeconomic Perspective on Urban Transit Resilience**

**Author:** Panithi Tawethipong

---

## Project Overview

Most big data analyses of urban transit merely correlate trip volume with weather patterns. **This project is fundamentally different.** My analysis uses **socioeconomic wealth level as the primary anchor** to investigate how systemic transit resilience and human behavior shift under extreme weather. 

By building a scalable, end-to-end Big Data pipeline leveraging PySpark and AWS cloud infrastructure, I cross-referenced over **100 million** NYC Taxi & Limousine Commission (TLC) trip records with historical NOAA weather observations and granular NYC Property Tax valuations. 

This unique approach allowed me to uncover a "Tale of Two Cities" during severe meteorological events—revealing hidden, wealth-driven disparities in how different neighborhoods adapt to, and pay for, transit when storms hit.

---

## The Story: A Tale of Two Cities During a Storm

When severe weather hits New York City, the transit system essentially collapses. Total trips plummet, and because the streets empty out, the few taxis still operating speed through the city nearly 45% faster than normal. **But the burden of this collapse is not shared equally:**

1. **The Availability Evaporation:** During heavy storms, taxis naturally congregate where the money is. High-wealth neighborhoods maintain a reliable baseline of service, while taxi availability in low-wealth neighborhoods drops to near zero. They are effectively abandoned by the network.
2. **The Desperation Premium (Pricing Surges):** When a passenger in a low-wealth area *does* manage to secure a taxi during a storm, they are penalized the most. The pricing surge (fare per minute) hits low-wealth areas significantly harder.
3. **The Guilt/Incentive Tip:** High-wealth passengers tip a steady, predictable ~21% regardless of whether it's sunny or pouring rain. But in low-wealth areas, tipping skyrockets to an incredible 38% during rain. Because rides are so scarce, passengers in lower-income areas are forced to massively overcompensate drivers just to incentivize them to operate in their neighborhoods.

---

## Core Research Questions Answered

1. **Weather Resilience by Wealth:** Do high-value real estate neighborhoods show less variance in taxi demand during severe weather compared to lower-value areas? 
2. **The "Luxury Tip" Weather Effect:** How does tipping behavior change during adverse weather, and is the percentage increase significantly higher in wealthy neighborhoods?
3. **Property Type & Airport Travel:** Do neighborhoods dominated by large single-family homes show different travel patterns to airports during bad weather than dense condo/co-op areas?
4. **Pricing Surge Tolerance:** When weather-induced delays increase fare costs, are trips originating from high-price localities more resilient to these cost surges?
5. **General Operations:** How does weather broadly affect hourly taxi demand, trip duration, and average travel speeds across the city?

---

## Datasets

1. **NYC TLC Yellow Taxi Trip Records:** Primary dataset containing millions of trips.
2. **Historical NYC Weather (NOAA):** Hourly observations (temperature, precipitation, wind speed, etc.).
3. **NYC Housing Market Data:** Real estate listings mapping property types and values.
4. **NYC Taxi Zone Lookup:** Geographic mapping for spatial joins.

---

## Architecture, Extensions & Technology Stack

- **Big Data at Real Scale:** Processed over 100+ million raw NYC Taxi records.
- **Query-Performance Tuning:** Instead of uploading flat CSVs, I used PySpark to aggressively restructure, denormalize, and partition the data into columnar `.parquet` formats. This big-data technique exponentially reduced serverless query costs and runtime when executing Athena queries on the 100M+ row dataset.

**Technologies Used:**
- Apache Spark (PySpark)
- Docker & Docker Compose
- AWS S3 (Data Lake)
- Amazon Athena (Serverless SQL Analytics)
- Terraform (IaC)
- Python (Pandas, Seaborn, Matplotlib)

**The Pipeline:**
```text
Public Datasets (100M+ Rows)
        │
        ▼
   Apache Spark (Local Docker Cluster)
(Rigorous Pipeline: Imputation, Outlier Treatment, Normalization, Encoding, Binning)
        │
        ▼
      AWS S3 (Cloud Data Lake - Parquet Partitioned)
        │
        ▼
   AWS Athena (Serverless Query Engine)
        │
        ▼
Results, Visualizations, & Insights
```

---

## Run Instructions

To reproduce this cloud-scale analytics pipeline from scratch:

1. **Local Setup:**
   - Clone the repository and run `docker compose up -d` to launch the Spark/Jupyter environment.
   - Run `python src/download_data.py` to acquire the raw datasets.
   - Run `python src/preprocess.py` to execute the PySpark preprocessing pipeline (imputation, outlier treatment, and Parquet partitioning).
2. **Cloud Deployment:**
   - Configure your AWS CLI credentials locally (`aws configure`).
   - Navigate to `cd infrastructure/` and run `terraform init` followed by `terraform apply -auto-approve` to provision the S3 Data Lake and Athena Workgroups.
3. **Analytics Execution:**
   - Upload the local `data/processed/` Parquet files to your new S3 bucket via the AWS CLI.
   - Run `python src/athena_analytics.py` to trigger the serverless SQL queries in Athena.
   - Run `python src/visualize.py` to generate the final PNG charts.
4. **Cleanup:**
   - Always run `cd infrastructure/ && terraform destroy` when finished to prevent AWS billing.

---

## Repository Structure

```text
docs/             # Project documentation and rubrics
src/              # Source code (PySpark preprocessing, Athena analytics, Visualizations)
visualizations/   # Generated .png charts showcasing analytical findings
sql/              # Raw SQL queries (if applicable)
results/          # Aggregated CSV outputs from Athena/PySpark
data/             # Local data storage (ignored in git)
infrastructure/   # Terraform code for AWS deployment
```

---

## Project Status

✅ Repository created
✅ Project scope & narrative defined
✅ Local Spark implementation & Data Cleaning
✅ AWS Infrastructure deployment (Terraform)
✅ Cloud-scale analytics execution (Athena)
✅ Final visual reporting and presentation generated
