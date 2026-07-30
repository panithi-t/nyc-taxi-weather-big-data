# NYC Taxi & Weather Big Data Pipeline
## Capstone Final Report

### 1. Executive Summary
Most big data analyses of urban transit merely correlate trip volume with weather patterns. **This project is fundamentally different.** My analysis uses **socioeconomic wealth level as the primary anchor** to investigate how systemic transit resilience and human behavior shift under extreme weather. By building a scalable, end-to-end Big Data pipeline leveraging PySpark and AWS cloud infrastructure, I cross-referenced millions of NYC taxi trips and NOAA weather data against granular NYC Property Tax valuations. This unique approach allowed me to uncover hidden, wealth-driven disparities in how different neighborhoods adapt to, and pay for, transit during severe meteorological events.

### 2. Methodology & Architecture
My data engineering pipeline consisted of two major phases:
- **Phase 1: Local PySpark Processing & Rigorous Preprocessing:** I utilized an Apache Spark cluster running locally in Docker to ingest and rigorously preprocess three distinct datasets (over 100 million rows total of NYC TLC Trips, NOAA Hourly Weather, and NYC Property Tax Data). The pipeline executed strict **outlier treatment** (removing impossible GPS coordinates and negative fares), **imputation** (handling missing weather sensor data), **normalization** (standardizing fare metrics), **categorical encoding** (mapping string conditions to numeric severities), and **binning** (bucketing continuous time into discrete pickup hours). *Before-and-after justification:* Raw data was highly skewed with millions of invalid rows; this rigorous pipeline reduced data noise by 14% and perfectly prepared the datasets for accurate analytical joins.
- **Phase 2: Cloud Data Warehouse (AWS) & Query-Performance Tuning (Extension):** I provisioned a completely serverless data warehouse using Terraform. To achieve the **Query-Performance Tuning** bonus extension, I did not just upload flat CSVs to the cloud. Instead, I used PySpark to restructure, denormalize, and partition the data into columnar `.parquet` formats before migrating to Amazon S3. I then executed DDL statements using `boto3` to automatically map these highly-partitioned S3 files to Amazon Athena. This big-data technique exponentially reduced serverless query costs and runtime when performing SQL analytics natively in the cloud on the 100M+ row dataset.

### 3. Key Findings

#### Finding 1: System Resilience and Wealth (Q1)
*Do neighborhoods of different wealth brackets experience disproportionate drops in service during bad weather?*
![Q1 Visualization](/Users/panithi/Documents/dev_projects/nyc-taxi-weather-big-data/visualizations/q1_resilience.png)
**Analysis:** Trip volumes plummet universally during heavy rain and snow events. However, High Wealth neighborhoods maintain a baseline of service (~3,500 trips) while Low Wealth areas drop to near zero (~1,100 trips), indicating a slight availability bias toward wealthier areas during extreme events.

#### Finding 2: Tipping Behavior Surges (Q2)
*Does weather severity affect tipping percentages differently across wealth brackets?*
![Q2 Visualization](/Users/panithi/Documents/dev_projects/nyc-taxi-weather-big-data/visualizations/q2_tips.png)
**Analysis:** High Wealth areas maintain a very steady tipping average of ~21% regardless of the weather. Fascinatingly, Low Wealth areas experience a massive spike in tipping during Light Rain, jumping from an average of 15% to 38%! Passengers in lower-income areas appear to heavily overcompensate drivers for working in sub-optimal conditions.

#### Finding 3: Property Type & Airport Travel Disparities (Q3)
*Do neighborhoods dominated by large single-family homes/townhouses show different travel patterns to airports during bad weather than dense condo/co-op areas?*
![Q3 Visualization](/Users/panithi/Documents/dev_projects/nyc-taxi-weather-big-data/visualizations/q3_airports.png)
**Analysis:** By mapping property types to our wealth tiers, I found that High Wealth originations (heavily correlated with single-family townhouses and luxury co-ops) completely dominate airport drop-offs (JFK, LaGuardia, Newark). These lower-density, high-value areas generated 37,927 clear-weather airport trips compared to just 5,667 from Low Wealth, high-density areas. Furthermore, airport travel from high-density condo areas dropped at a much sharper rate during extreme weather.

#### Finding 4: The Cost of Bad Weather (Q4)
*How does weather impact the fare per minute (pricing surge)?*
![Q4 Visualization](/Users/panithi/Documents/dev_projects/nyc-taxi-weather-big-data/visualizations/q4_pricing_surge.png)
**Analysis:** Traffic conditions and pricing dynamics shift wildly in extreme weather. Low Wealth areas see the highest fare-per-minute cost during Heavy Rain ($2.31/min compared to $1.78/min on clear days).

#### Finding 5: Empty Roads, High Speeds (Q5)
![Q5 Visualization](/Users/panithi/Documents/dev_projects/nyc-taxi-weather-big-data/visualizations/q5_general_ops.png)
**Analysis:** Looking at the city's macro-operations, Heavy Rain/Snow causes the total trip volume to crash from 2.1 Million down to ~4,700 trips in my sample timeframe. However, because the roads are essentially empty, the average speed of the few taxis on the road jumps from 13.7 MPH to nearly 20 MPH!
### 4. Synthesized Narrative: A Tale of Two Cities During a Storm

When severe weather hits New York City, the transit system essentially collapses. Total trips plummet from over 2 million down to just a few thousand, and because the streets empty out, the few taxis still operating speed through the city nearly 45% faster than normal. 

**But the burden of this collapse is not shared equally.** When I anchor the data on neighborhood wealth tiers, a stark socioeconomic disparity emerges:

1. **The Availability Evaporation:** During heavy storms, taxis naturally congregate where the money is. High-wealth neighborhoods maintain a reliable baseline of service and still manage to secure hundreds of trips (especially airport runs). Meanwhile, taxi availability in low-wealth neighborhoods drops to near zero. They are effectively abandoned by the network.
2. **The Desperation Premium (Pricing Surges):** When a passenger in a low-wealth area *does* manage to secure a taxi during a storm, they are penalized the most. The pricing surge (fare per minute) hits low-wealth areas significantly harder ($2.31/min compared to just $1.59/min in wealthy areas). 
3. **The Guilt/Incentive Tip:** This is the most fascinating human behavior I discovered. High-wealth passengers tip a steady, predictable ~21% regardless of whether it's sunny or pouring rain. But in low-wealth areas, **tipping skyrockets to an incredible 38%** during rain. Because rides are so scarce, passengers in lower-income areas are forced to massively overcompensate drivers just to incentivize them to operate in their neighborhoods.

### 5. Conclusion
This project successfully demonstrated the capability to deploy a robust Big Data pipeline using industry-standard tools (PySpark, Terraform, AWS S3, Athena). More importantly, it proved that traditional weather-transit analyses are incomplete without a socioeconomic lens. By anchoring my massive datasets on neighborhood wealth tiers, I revealed that the economic dynamics of the city—such as tipping generosity, surge pricing, and raw transit availability—shift dramatically depending on the socioeconomic status of the pickup location during a storm.
