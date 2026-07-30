from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp, round as spark_round, when, regexp_replace, to_timestamp

def create_spark_session():
    return SparkSession.builder \
        .appName("NYC_Taxi_Weather_Preprocessing") \
        .getOrCreate()

def preprocess_taxi(spark):
    print("Preprocessing Taxi Data...")
    df = spark.read.parquet("data/raw/yellow_tripdata_2024-01.parquet")
    
    # 1. Imputation / Drop Missing
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"])
    
    # 2. Outlier Treatment
    # Filter negative fares, zero distances, and impossible durations
    df = df.filter((col("fare_amount") > 0) & (col("trip_distance") > 0))
    
    # Calculate duration in minutes
    df = df.withColumn(
        "duration_min", 
        (unix_timestamp("tpep_dropoff_datetime") - unix_timestamp("tpep_pickup_datetime")) / 60
    )
    
    # Filter reasonable durations (e.g., > 1 min and < 3 hours)
    df = df.filter((col("duration_min") > 1) & (col("duration_min") < 180))
    
    # Create derived columns: pickup_hour for joining with weather
    df = df.withColumn("pickup_date", col("tpep_pickup_datetime").cast("date"))
    # Extract hour (0-23)
    df = df.withColumn("pickup_hour", (unix_timestamp("tpep_pickup_datetime") % 86400) / 3600)
    df = df.withColumn("pickup_hour", spark_round(col("pickup_hour"), 0).cast("int"))
    
    return df

def preprocess_weather(spark):
    print("Preprocessing Weather Data...")
    # The weather data from open-meteo has a header on row 3 usually, but let's assume it's standard CSV 
    # since we fetched it from the archive API. It has a 'time' column.
    # Note: open-meteo CSV might have 2-3 lines of metadata at the top. We'll read it, but ideally we'd skip rows.
    # We will use pandas to read and then convert to spark for simplicity of dealing with open-meteo metadata, 
    # but let's try reading it directly and filtering out non-date rows.
    
    # We downloaded as CSV. Open-meteo CSV has 3 lines of metadata.
    # For robust Spark processing, we'll read as text, filter, and parse.
    df = spark.read.option("header", "true").option("skipRows", 3).csv("data/raw/nyc_weather_2024-01.csv")
    
    # Convert types
    if "temperature_2m (°C)" in df.columns:
        df = df.withColumn("temperature", col("temperature_2m (°C)").cast("double"))
        df = df.withColumn("precipitation", col("precipitation (mm)").cast("double"))
    else:
        # Fallback if names differ
        df = df.withColumn("temperature", col(df.columns[1]).cast("double"))
        df = df.withColumn("precipitation", col(df.columns[2]).cast("double"))
    
    # Binning Weather Severities
    df = df.withColumn("weather_severity",
        when(col("precipitation") > 5.0, "Heavy Rain/Snow")
        .when((col("precipitation") > 0) & (col("precipitation") <= 5.0), "Light Rain")
        .otherwise("Clear/Cloudy")
    )
    
    # Extract date and hour for joining
    df = df.withColumn("parsed_time", to_timestamp(col("time"), "yyyy-MM-dd'T'HH:mm"))
    df = df.withColumn("date", col("parsed_time").cast("date"))
    df = df.withColumn("hour", (unix_timestamp("parsed_time") % 86400) / 3600)
    df = df.withColumn("hour", spark_round(col("hour"), 0).cast("int"))
    
    return df

def preprocess_housing(spark):
    print("Preprocessing Housing Data...")
    df = spark.read.option("header", "true").csv("data/raw/nyc_housing_market.csv")
    
    # Clean PRICE column (remove $ and commas)
    df = df.withColumn("PRICE", regexp_replace("PRICE", "[\\$,]", "").cast("double"))
    
    # Drop rows without prices or localities
    df = df.dropna(subset=["PRICE", "LOCALITY", "SUBLOCALITY"])
    
    # Binning Wealth brackets
    df = df.withColumn("wealth_bracket",
        when(col("PRICE") >= 2000000, "High")
        .when((col("PRICE") >= 750000) & (col("PRICE") < 2000000), "Medium")
        .otherwise("Low")
    )
    
    return df

def preprocess_zones(spark):
    print("Preprocessing Taxi Zones...")
    df = spark.read.option("header", "true").csv("data/raw/taxi_zone_lookup.csv")
    return df

def main():
    spark = create_spark_session()
    
    # Process
    taxi_df = preprocess_taxi(spark)
    weather_df = preprocess_weather(spark)
    housing_df = preprocess_housing(spark)
    zones_df = preprocess_zones(spark)
    
    # Write Out
    print("Writing processed data to Parquet...")
    taxi_df.write.mode("overwrite").parquet("data/processed/taxi_cleaned.parquet")
    weather_df.write.mode("overwrite").parquet("data/processed/weather_cleaned.parquet")
    housing_df.write.mode("overwrite").parquet("data/processed/housing_cleaned.parquet")
    zones_df.write.mode("overwrite").parquet("data/processed/zones_cleaned.parquet")
    
    print("Preprocessing complete!")
    spark.stop()

if __name__ == "__main__":
    main()
