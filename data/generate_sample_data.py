"""
Sample data generator for revenue forecasting system
Creates realistic business data for demonstration and testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

def generate_sample_data():
    """Generate sample revenue and business data"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    random.seed(42)
    
    # Date range: 3 years of historical data
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Business units
    business_units = ['Sales', 'Marketing', 'Enterprise', 'SMB', 'International']
    
    # Generate revenue data
    revenue_data = []
    
    for unit in business_units:
        base_revenue = random.uniform(100000, 500000)
        growth_rate = random.uniform(0.05, 0.20)  # 5-20% annual growth
        seasonality_factor = random.uniform(0.1, 0.3)
        
        for i, date in enumerate(date_range):
            # Base growth trend
            trend = base_revenue * (1 + growth_rate) ** (i / 12)
            
            # Seasonal component
            seasonal = seasonality_factor * np.sin(2 * np.pi * i / 12)
            
            # Random noise
            noise = np.random.normal(0, 0.1)
            
            # Calculate final revenue
            revenue = trend * (1 + seasonal + noise)
            
            # Additional business metrics
            customer_count = int(revenue / random.uniform(1000, 5000))
            avg_deal_size = revenue / customer_count if customer_count > 0 else 0
            
            revenue_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'business_unit': unit,
                'revenue': round(revenue, 2),
                'customer_count': customer_count,
                'avg_deal_size': round(avg_deal_size, 2),
                'profit_margin': round(random.uniform(0.15, 0.35), 3),
                'marketing_spend': round(revenue * random.uniform(0.05, 0.15), 2),
                'sales_team_size': random.randint(5, 25)
            })
    
    return pd.DataFrame(revenue_data)

def generate_kpi_data():
    """Generate KPI tracking data"""
    
    date_range = pd.date_range(start='2021-01-01', end='2023-12-31', freq='M')
    
    kpi_data = []
    
    for date in date_range:
        kpi_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'customer_acquisition_cost': round(random.uniform(150, 800), 2),
            'customer_lifetime_value': round(random.uniform(2000, 8000), 2),
            'churn_rate': round(random.uniform(0.02, 0.08), 3),
            'retention_rate': round(random.uniform(0.88, 0.96), 3),
            'net_promoter_score': random.randint(30, 70),
            'conversion_rate': round(random.uniform(0.12, 0.28), 3),
            'market_share': round(random.uniform(0.05, 0.15), 3)
        })
    
    return pd.DataFrame(kpi_data)

if __name__ == "__main__":
    # Create data directories
    data_dir = Path("../data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save sample data
    revenue_df = generate_sample_data()
    kpi_df = generate_kpi_data()
    
    revenue_df.to_csv(data_dir / "revenue_data.csv", index=False)
    kpi_df.to_csv(data_dir / "kpi_data.csv", index=False)
    
    print("Sample data generated successfully!")
    print(f"Revenue data: {len(revenue_df)} records")
    print(f"KPI data: {len(kpi_df)} records")
    print(f"Business units: {revenue_df['business_unit'].nunique()}")
    print(f"Date range: {revenue_df['date'].min()} to {revenue_df['date'].max()}")