# Final Capstone Demo Script: "A Tale of Two Cities During a Storm"

> **Preparation before presenting:** 
> 1. Open `presentation.md` in a VS Code preview window (or as exported slides).
> 2. Open your `src/preprocess.py` file in a VS Code tab.
> 3. Open a web browser with the AWS S3 Console and AWS Athena Console ready.
> 4. Open a terminal window ready to type `terraform destroy`.

---

### Part 1: The Hook & Introduction (1 Minute)
*(Show: Slide 1 of presentation)*

**You:** "Hello everyone. For my CS-675 Capstone, I decided to analyze New York City's transit resilience during extreme weather using over 100 million TLC taxi trip records and historical NOAA weather data. 

Most Big Data projects stop at correlating basic trip volumes with rainfall. But I wanted to go much deeper. I engineered a cross-source join with NYC Property Tax Data to use **socioeconomic wealth tier as my primary anchor.** I wanted to answer the question: *When a severe storm hits, does the transit system fail equally for everyone, or does it become a luxury service?*"

### Part 2: Data Engineering & Query Tuning (1.5 Minutes)
*(Show: Open `src/preprocess.py` in your editor)*

**You:** "To handle data at this massive scale, I built a rigorous preprocessing pipeline locally using PySpark. As you can see here, I didn't just pass raw data to the cloud. I performed strict **outlier treatment** to remove impossible GPS coordinates, **imputation** for missing sensor data, and **categorical encoding** to map string conditions to numeric severities.

*(Highlight the Parquet save command in your code)*
"More importantly, I implemented the **Query-Performance Tuning** extension. Instead of uploading slow, flat CSVs to the cloud, I used PySpark to aggressively restructure, denormalize, and partition the 100 million rows into a columnar `.parquet` format before uploading to AWS. This drastically optimized my cloud architecture."

### Part 3: Live Cloud Analytics Demo (2 Minutes)
*(Show: Switch to your browser, showing AWS S3)*

**You:** "For my cloud infrastructure, I used Terraform to provision a completely serverless Data Lake in Amazon S3, which you can see here hosting my partitioned Parquet files."

*(Show: Switch to the AWS Athena Console)*

**You:** "Instead of spinning up expensive clusters, I used `boto3` to dynamically map these S3 files to Amazon Athena. Let me run a quick query live to show the scale."
*(Action: Highlight a simple query like `SELECT * FROM ds_panithi.integrated_trips LIMIT 10;` and click **Run**)*

**You:** "As you can see, Athena is executing distributed SQL directly against the Parquet files in S3, returning results in seconds without maintaining any permanent databases."

### Part 4: The Results & Findings (2 Minutes)
*(Show: Switch back to your presentation slides, specifically the charts)*

**You:** "So, what did this cloud analytics pipeline reveal? It revealed a 'Tale of Two Cities.' When heavy storms hit, the streets empty out and taxi speeds jump by 45%. But who gets those rides?

*(Show: Q1 & Q3 Charts)*
"First, **Availability Evaporates**. Taxis naturally congregate where the money is. High-wealth neighborhoods maintain a reliable baseline of service, while taxi availability in low-wealth neighborhoods drops to near zero. They are effectively abandoned by the network.

*(Show: Q2 & Q4 Charts)*
"Second, the **Desperation Premium**. When passengers in low-wealth areas *do* manage to secure a ride, they are penalized the most by surge pricing. But the most fascinating human behavior I discovered is the 'Guilt Tip'. High-wealth passengers tip a steady 21% regardless of weather. But in low-wealth areas, tipping skyrockets to an incredible 38% during rain. Because rides are so scarce, lower-income passengers are forced to massively overcompensate drivers just to incentivize them to operate in their neighborhoods."

### Part 5: The Grand Finale (30 Seconds)
*(Show: Terminal window)*

**You:** "In conclusion, my Big Data pipeline proved that extreme weather acts as an unequal tax on urban transit, protecting wealthy areas while heavily burdening lower-income neighborhoods. 

And finally, to demonstrate best practices in cloud resource management and cost-control, I will now tear down my infrastructure."

*(Action: Type `cd infrastructure && terraform destroy -auto-approve` and hit Enter)*

**You:** "Thank you. I'll now take any questions."
