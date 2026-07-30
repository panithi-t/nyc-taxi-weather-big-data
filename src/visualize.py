import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    # Setup styling: using a Blue-to-Teal gradient ("mako" or "crest")
    sns.set_theme(style="whitegrid", palette="crest")
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 16, 'axes.labelsize': 14})
    
    os.makedirs('visualizations', exist_ok=True)
    
    # Q1: Resilience (Trip Count)
    try:
        df1 = pd.read_csv('results/q1_resilience.csv').dropna()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df1, x='pickup_wealth', y='trip_count', hue='weather_severity', order=['High', 'Medium', 'Low'], hue_order=['Clear/Cloudy', 'Light Rain', 'Heavy Rain/Snow'])
        plt.title('Q1: Trip Volume by Wealth Area and Weather Severity')
        plt.xlabel('Neighborhood Wealth Bracket')
        plt.ylabel('Total Trips')
        plt.yscale('log') # Log scale because High volume is massive
        plt.tight_layout()
        plt.savefig('visualizations/q1_resilience.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"Failed to generate Q1: {e}")
        
    # Q2: Tips
    try:
        df2 = pd.read_csv('results/q2_tips.csv').dropna()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df2, x='pickup_wealth', y='avg_tip_percentage', hue='weather_severity', order=['High', 'Medium', 'Low'], hue_order=['Clear/Cloudy', 'Light Rain', 'Heavy Rain/Snow'])
        plt.title('Q2: Average Tip Percentage by Wealth and Weather')
        plt.xlabel('Neighborhood Wealth Bracket')
        plt.ylabel('Average Tip (%)')
        plt.tight_layout()
        plt.savefig('visualizations/q2_tips.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"Failed to generate Q2: {e}")
        
    # Q3: Airports
    try:
        df3 = pd.read_csv('results/q3_airports.csv').dropna()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df3, x='pickup_wealth', y='airport_trips', hue='weather_severity', order=['High', 'Medium', 'Low'], hue_order=['Clear/Cloudy', 'Light Rain', 'Heavy Rain/Snow'])
        plt.title('Q3: Airport Trips by Origin Wealth and Weather')
        plt.xlabel('Origin Neighborhood Wealth Bracket')
        plt.ylabel('Airport Trips')
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig('visualizations/q3_airports.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"Failed to generate Q3: {e}")

    # Q4: Pricing Surge
    try:
        df4 = pd.read_csv('results/q4_pricing_surge.csv').dropna()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df4, x='pickup_wealth', y='avg_fare_per_minute', hue='weather_severity', order=['High', 'Medium', 'Low'], hue_order=['Clear/Cloudy', 'Light Rain', 'Heavy Rain/Snow'])
        plt.title('Q4: Average Fare Per Minute by Wealth and Weather')
        plt.xlabel('Neighborhood Wealth Bracket')
        plt.ylabel('Fare per Minute ($)')
        plt.tight_layout()
        plt.savefig('visualizations/q4_pricing_surge.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"Failed to generate Q4: {e}")
        
    # Q5: General Ops
    try:
        df5 = pd.read_csv('results/q5_general_ops.csv').dropna()
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        weather_order = ['Clear/Cloudy', 'Light Rain', 'Heavy Rain/Snow']
        
        ax2 = ax1.twinx()
        sns.barplot(data=df5, x='weather_severity', y='total_trips', ax=ax1, color='#45B39D', alpha=0.7, order=weather_order) # Teal
        sns.lineplot(data=df5, x='weather_severity', y='avg_speed_mph', ax=ax2, color='#154360', marker='o', linewidth=2.5, err_style=None) # Dark Blue
        
        ax1.set_xlabel('Weather Severity')
        ax1.set_ylabel('Total Trips', color='#45B39D')
        ax2.set_ylabel('Average Speed (MPH)', color='#154360')
        plt.title('Q5: Overall System Operations vs Weather')
        plt.tight_layout()
        plt.savefig('visualizations/q5_general_ops.png', dpi=300)
        plt.close()
    except Exception as e:
        print(f"Failed to generate Q5: {e}")
        
    print("Visualizations successfully saved to visualizations/ directory.")

if __name__ == '__main__':
    create_visualizations()
