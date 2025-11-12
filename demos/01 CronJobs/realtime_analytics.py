#!/usr/bin/env python3
"""
Real-time Analytics Demo for CronJob
Simulates live data processing with time series analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import logging
import json
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_sensor_data():
    """Generate synthetic sensor data with trends and noise"""
    np.random.seed(int(datetime.now().timestamp()))
    
    # Create time series with trend, seasonality, and noise
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(60, 0, -1)]
    
    # Base trend (slowly increasing)
    trend = np.linspace(0, 2, 60)
    
    # Daily seasonality (simulated as hourly pattern)
    seasonality = 3 * np.sin(2 * np.pi * np.arange(60) / 12)
    
    # Random noise
    noise = np.random.normal(0, 0.5, 60)
    
    # Combine components
    values = 50 + trend + seasonality + noise
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'value': values,
        'sensor_id': np.random.choice(['sensor_A', 'sensor_B', 'sensor_C'], 60)
    })

def analyze_trends(df):
    """Perform real-time analytics"""
    results = {
        'processing_time': datetime.now().isoformat(),
        'total_readings': len(df),
        'current_value': df['value'].iloc[-1],
        'rolling_avg_10min': df['value'].tail(10).mean(),
        'trend_direction': 'increasing' if df['value'].iloc[-1] > df['value'].iloc[-10] else 'decreasing',
        'anomalies': len(df[df['value'] > df['value'].mean() + 2 * df['value'].std()])
    }
    
    # Detect recent spike
    recent_values = df['value'].tail(5)
    if max(recent_values) > df['value'].mean() + 3 * df['value'].std():
        results['alert'] = 'SPIKE_DETECTED'
    
    return results

def create_analytics_plot(df, results, output_path):
    """Create a comprehensive analytics dashboard"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Time series plot
    ax1.plot(df['timestamp'], df['value'], label='Sensor Readings', alpha=0.7)
    ax1.axhline(y=results['rolling_avg_10min'], color='r', linestyle='--', label='10-min Avg')
    ax1.set_title('Real-time Sensor Data')
    ax1.set_ylabel('Value')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # Distribution plot
    ax2.hist(df['value'], bins=20, alpha=0.7, edgecolor='black')
    ax2.axvline(x=results['current_value'], color='r', linestyle='--', label='Current Value')
    ax2.set_title('Value Distribution')
    ax2.set_xlabel('Value')
    ax2.legend()
    
    # Sensor comparison
    sensor_means = df.groupby('sensor_id')['value'].mean()
    ax3.bar(sensor_means.index, sensor_means.values, alpha=0.7)
    ax3.set_title('Average Values by Sensor')
    ax3.set_ylabel('Average Value')
    
    # Status indicators
    status_text = f"""
    Analytics Summary:
    • Current Value: {results['current_value']:.2f}
    • Trend: {results['trend_direction']}
    • Rolling Avg: {results['rolling_avg_10min']:.2f}
    • Anomalies: {results['anomalies']}
    • Alert: {results.get('alert', 'None')}
    """
    ax4.text(0.1, 0.5, status_text, fontsize=12, verticalalignment='center')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    """Main analytics pipeline"""
    try:
        logger.info("🚀 Starting real-time analytics pipeline")
        
        # Generate synthetic data
        df = generate_sensor_data()
        logger.info(f"📊 Generated {len(df)} data points")
        
        # Perform analytics
        results = analyze_trends(df)
        logger.info(f"📈 Analysis complete: {results}")
        
        # Create visualization
        output_dir = "/shared-data"
        os.makedirs(output_dir, exist_ok=True)
        
        plot_path = f"{output_dir}/analytics_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        create_analytics_plot(df, results, plot_path)
        logger.info(f"🖼️  Dashboard saved: {plot_path}")
        
        # Save results
        results_path = f"{output_dir}/latest_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Update summary file
        summary_path = f"{output_dir}/processing_summary.log"
        with open(summary_path, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Processed {len(df)} records - Status: SUCCESS\n")
        
        logger.info("✅ Analytics pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Error in analytics pipeline: {e}")
        # Log failure
        summary_path = "/shared-data/processing_summary.log"
        with open(summary_path, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - ERROR: {str(e)}\n")
        raise

if __name__ == "__main__":
    main()
