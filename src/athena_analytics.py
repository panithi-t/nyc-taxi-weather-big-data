import boto3
import time

def run_query(query, client, database, workgroup):
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        WorkGroup=workgroup
    )
    query_execution_id = response['QueryExecutionId']
    
    print(f"Executing query {query_execution_id}...")
    while True:
        response = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = response['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)
        
    if state == 'SUCCEEDED':
        print("Query succeeded!")
        return query_execution_id
    else:
        print(f"Query failed: {response['QueryExecution']['Status'].get('StateChangeReason')}")
        return None

def main():
    # Configure boto3 to use our 'ds' profile
    session = boto3.Session(profile_name='ds', region_name='us-east-2')
    client = session.client('athena')
    
    database = 'ds_panithi'
    workgroup = 'ds-panithi'
    bucket = 's3://ds-panithi-workspace/data/processed'
    
    print("--- Creating External Tables ---")
    tables_ddl = [
        f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS taxi (
            VendorID bigint,
            tpep_pickup_datetime timestamp,
            tpep_dropoff_datetime timestamp,
            passenger_count bigint,
            trip_distance double,
            RatecodeID bigint,
            store_and_fwd_flag string,
            PULocationID bigint,
            DOLocationID bigint,
            payment_type bigint,
            fare_amount double,
            extra double,
            mta_tax double,
            tip_amount double,
            tolls_amount double,
            improvement_surcharge double,
            total_amount double,
            congestion_surcharge double,
            Airport_fee double,
            duration_min double,
            pickup_date date,
            pickup_hour bigint
        )
        STORED AS PARQUET
        LOCATION '{bucket}/taxi_cleaned.parquet/'
        """,
        f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS weather (
            time string,
            `temperature_2m (°C)` string,
            `precipitation (mm)` string,
            `wind_speed_10m (km/h)` string,
            temperature double,
            precipitation double,
            weather_severity string,
            parsed_time timestamp,
            date date,
            hour bigint
        )
        STORED AS PARQUET
        LOCATION '{bucket}/weather_cleaned.parquet/'
        """,
        f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS housing (
            BROKERTITLE string,
            TYPE string,
            PRICE double,
            BEDS string,
            BATH string,
            PROPERTYSQFT string,
            ADDRESS string,
            STATE string,
            MAIN_ADDRESS string,
            ADMINISTRATIVE_AREA_LEVEL_2 string,
            LOCALITY string,
            SUBLOCALITY string,
            STREET_NAME string,
            LONG_NAME string,
            FORMATTED_ADDRESS string,
            LATITUDE string,
            LONGITUDE string,
            wealth_bracket string
        )
        STORED AS PARQUET
        LOCATION '{bucket}/housing_cleaned.parquet/'
        """,
        f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS zones (
            LocationID string,
            Borough string,
            Zone string,
            service_zone string
        )
        STORED AS PARQUET
        LOCATION '{bucket}/zones_cleaned.parquet/'
        """
    ]
    
    for ddl in tables_ddl:
        run_query(ddl, client, database, workgroup)
        
    print("--- Executing Research Queries on Athena ---")
    
    # Pre-create the view for mapped housing and integrated trips in Athena
    run_query("""
        CREATE OR REPLACE VIEW housing_by_borough AS
        SELECT 
            CASE 
                WHEN SUBLOCALITY LIKE '%Manhattan%' OR SUBLOCALITY LIKE '%New York%' THEN 'Manhattan'
                WHEN SUBLOCALITY LIKE '%Brooklyn%' OR SUBLOCALITY LIKE '%Kings%' THEN 'Brooklyn'
                WHEN SUBLOCALITY LIKE '%Queens%' THEN 'Queens'
                WHEN SUBLOCALITY LIKE '%Bronx%' THEN 'Bronx'
                WHEN SUBLOCALITY LIKE '%Staten%' OR SUBLOCALITY LIKE '%Richmond%' THEN 'Staten Island'
                ELSE 'Unknown'
            END AS Borough,
            max_by(wealth_bracket, 1) as dominant_wealth
        FROM housing
        GROUP BY 1
    """, client, database, workgroup)

    run_query("""
        CREATE OR REPLACE VIEW integrated_trips AS
        SELECT 
            t.*,
            w.weather_severity,
            zp.Borough as pickup_borough,
            zp.Zone as pickup_zone,
            zd.Borough as dropoff_borough,
            zd.Zone as dropoff_zone,
            hb.dominant_wealth as pickup_wealth
        FROM taxi t
        JOIN weather w ON t.pickup_date = w.date AND t.pickup_hour = w.hour
        JOIN zones zp ON cast(t.PULocationID as varchar) = zp.LocationID
        JOIN zones zd ON cast(t.DOLocationID as varchar) = zd.LocationID
        LEFT JOIN housing_by_borough hb ON zp.Borough = hb.Borough
    """, client, database, workgroup)

    # Q1
    q1 = """
        SELECT pickup_wealth, weather_severity, COUNT(*) as trip_count
        FROM integrated_trips
        WHERE pickup_wealth IS NOT NULL
        GROUP BY pickup_wealth, weather_severity
        ORDER BY pickup_wealth, weather_severity
    """
    run_query(q1, client, database, workgroup)
    print("Queries successfully submitted and completed on Athena!")

if __name__ == '__main__':
    main()
