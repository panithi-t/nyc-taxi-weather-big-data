from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, expr
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("NYC_Taxi_Weather_Analytics") \
        .getOrCreate()

def main():
    spark = create_spark_session()
    
    # Ensure results directory exists
    os.makedirs("/home/jovyan/work/results", exist_ok=True)
    
    print("Loading processed datasets...")
    taxi_df = spark.read.parquet("data/processed/taxi_cleaned.parquet")
    weather_df = spark.read.parquet("data/processed/weather_cleaned.parquet")
    housing_df = spark.read.parquet("data/processed/housing_cleaned.parquet")
    zones_df = spark.read.parquet("data/processed/zones_cleaned.parquet")
    
    # Standardize housing boroughs for joining
    housing_mapped = housing_df.withColumn("Borough", 
        when(col("SUBLOCALITY").contains("Manhattan") | col("SUBLOCALITY").contains("New York"), "Manhattan")
        .when(col("SUBLOCALITY").contains("Brooklyn") | col("SUBLOCALITY").contains("Kings"), "Brooklyn")
        .when(col("SUBLOCALITY").contains("Queens"), "Queens")
        .when(col("SUBLOCALITY").contains("Bronx"), "Bronx")
        .when(col("SUBLOCALITY").contains("Staten") | col("SUBLOCALITY").contains("Richmond"), "Staten Island")
        .otherwise("Unknown")
    )
    
    # Create temp views for Spark SQL
    taxi_df.createOrReplaceTempView("taxi")
    weather_df.createOrReplaceTempView("weather")
    housing_mapped.createOrReplaceTempView("housing")
    zones_df.createOrReplaceTempView("zones")
    
    # --- Create Integrated Master View ---
    # We aggregate housing data by borough to get median wealth and dominant property types
    spark.sql("""
        CREATE OR REPLACE TEMP VIEW housing_by_borough AS
        SELECT 
            Borough, 
            mode(wealth_bracket) as dominant_wealth,
            percentile_approx(PRICE, 0.5) as median_price
        FROM housing
        WHERE Borough != 'Unknown'
        GROUP BY Borough
    """)
    
    spark.sql("""
        CREATE OR REPLACE TEMP VIEW integrated_trips AS
        SELECT 
            t.*,
            w.temperature,
            w.precipitation,
            w.weather_severity,
            zp.Borough as pickup_borough,
            zp.Zone as pickup_zone,
            zd.Borough as dropoff_borough,
            zd.Zone as dropoff_zone,
            hb.dominant_wealth as pickup_wealth
        FROM taxi t
        JOIN weather w 
            ON t.pickup_date = w.date AND t.pickup_hour = w.hour
        JOIN zones zp 
            ON t.PULocationID = zp.LocationID
        JOIN zones zd 
            ON t.DOLocationID = zd.LocationID
        LEFT JOIN housing_by_borough hb 
            ON zp.Borough = hb.Borough
    """)
    
    # 1. Weather Resilience by Wealth
    print("Executing Q1: Weather Resilience by Wealth...")
    q1 = spark.sql("""
        SELECT 
            pickup_wealth, 
            weather_severity, 
            COUNT(*) as trip_count
        FROM integrated_trips
        WHERE pickup_wealth IS NOT NULL
        GROUP BY pickup_wealth, weather_severity
        ORDER BY pickup_wealth, weather_severity
    """)
    q1.toPandas().to_csv("results/q1_resilience.csv", index=False)
    
    # 2. The "Luxury Tip" Weather Effect
    print("Executing Q2: Luxury Tip Effect...")
    q2 = spark.sql("""
        SELECT 
            pickup_wealth,
            weather_severity,
            ROUND(AVG(tip_amount / NULLIF(fare_amount, 0)) * 100, 2) as avg_tip_percentage
        FROM integrated_trips
        WHERE pickup_wealth IS NOT NULL AND fare_amount > 0
        GROUP BY pickup_wealth, weather_severity
        ORDER BY pickup_wealth, weather_severity
    """)
    q2.toPandas().to_csv("results/q2_tips.csv", index=False)
    
    # 3. Property Type & Airport Travel (simplified to Borough Wealth vs Airport)
    print("Executing Q3: Airport Travel during Weather...")
    q3 = spark.sql("""
        SELECT 
            pickup_wealth,
            weather_severity,
            COUNT(*) as airport_trips
        FROM integrated_trips
        WHERE dropoff_zone LIKE '%Airport%' OR dropoff_zone = 'JFK Airport' OR dropoff_zone = 'LaGuardia Airport'
        GROUP BY pickup_wealth, weather_severity
        ORDER BY pickup_wealth, weather_severity
    """)
    q3.toPandas().to_csv("results/q3_airports.csv", index=False)
    
    # 4. Pricing Surge Tolerance (Cost per minute by weather and wealth)
    print("Executing Q4: Pricing Surge Tolerance...")
    q4 = spark.sql("""
        SELECT 
            pickup_wealth,
            weather_severity,
            ROUND(AVG(fare_amount / duration_min), 2) as avg_fare_per_minute,
            ROUND(AVG(duration_min), 2) as avg_duration_min
        FROM integrated_trips
        WHERE pickup_wealth IS NOT NULL AND duration_min > 0
        GROUP BY pickup_wealth, weather_severity
        ORDER BY pickup_wealth, weather_severity
    """)
    q4.toPandas().to_csv("results/q4_pricing_surge.csv", index=False)
    
    # 5. General Operations (Duration and Speed)
    print("Executing Q5: General Operations...")
    q5 = spark.sql("""
        SELECT 
            weather_severity,
            COUNT(*) as total_trips,
            ROUND(AVG(duration_min), 2) as avg_duration_min,
            ROUND(AVG(trip_distance / (duration_min / 60)), 2) as avg_speed_mph
        FROM integrated_trips
        WHERE duration_min > 0
        GROUP BY weather_severity
        ORDER BY weather_severity
    """)
    q5.toPandas().to_csv("results/q5_general_ops.csv", index=False)
    
    print("Analytics completed. Results saved to results/")
    spark.stop()

if __name__ == "__main__":
    main()
