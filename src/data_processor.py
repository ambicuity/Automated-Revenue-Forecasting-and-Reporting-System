"""
Data Processing Module
Handles data loading, cleaning, validation, and preprocessing
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
import os

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import *

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles all data processing operations"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        self.processed_data_dir = PROCESSED_DATA_DIR
        self.processed_data_dir.mkdir(exist_ok=True)
        
    def load_revenue_data(self) -> pd.DataFrame:
        """Load and validate revenue data"""
        try:
            file_path = self.raw_data_dir / "revenue_data.csv"
            if not file_path.exists():
                raise FileNotFoundError(f"Revenue data file not found: {file_path}")
                
            df = pd.read_csv(file_path)
            logger.info(f"Loaded revenue data: {len(df)} records")
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            return self._validate_data(df, 'revenue')
            
        except Exception as e:
            logger.error(f"Error loading revenue data: {e}")
            raise
    
    def load_kpi_data(self) -> pd.DataFrame:
        """Load and validate KPI data"""
        try:
            file_path = self.raw_data_dir / "kpi_data.csv"
            if not file_path.exists():
                raise FileNotFoundError(f"KPI data file not found: {file_path}")
                
            df = pd.read_csv(file_path)
            logger.info(f"Loaded KPI data: {len(df)} records")
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading KPI data: {e}")
            raise
    
    def _validate_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Validate data based on predefined rules"""
        logger.info(f"Validating {data_type} data...")
        
        original_count = len(df)
        
        # Remove records with missing revenue or negative revenue
        if 'revenue' in df.columns:
            df = df[df['revenue'].notna() & (df['revenue'] >= 0)]
            
        # Remove records with missing dates
        df = df[df['date'].notna()]
        
        # Remove records with missing business units
        if 'business_unit' in df.columns:
            df = df[df['business_unit'].notna()]
            
        cleaned_count = len(df)
        if original_count != cleaned_count:
            logger.warning(f"Removed {original_count - cleaned_count} invalid records")
            
        return df
    
    def calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate additional business metrics"""
        logger.info("Calculating derived metrics...")
        
        # Sort by date and business unit
        df = df.sort_values(['business_unit', 'date'])
        
        # Calculate month-over-month growth
        df['revenue_mom_growth'] = df.groupby('business_unit')['revenue'].pct_change()
        
        # Calculate year-over-year growth
        df['revenue_yoy_growth'] = df.groupby('business_unit')['revenue'].pct_change(periods=12)
        
        # Calculate rolling 3-month average
        df['revenue_3m_avg'] = df.groupby('business_unit')['revenue'].rolling(window=3).mean().values
        
        # Calculate rolling 12-month sum
        df['revenue_12m_sum'] = df.groupby('business_unit')['revenue'].rolling(window=12).sum().values
        
        # Customer metrics
        if 'customer_count' in df.columns:
            df['customer_mom_growth'] = df.groupby('business_unit')['customer_count'].pct_change()
            df['revenue_per_customer'] = df['revenue'] / df['customer_count']
        
        return df
    
    def aggregate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create aggregated views of the data"""
        logger.info("Creating aggregated data views...")
        
        # Monthly aggregation across all business units
        monthly_agg = df.groupby('date').agg({
            'revenue': 'sum',
            'customer_count': 'sum',
            'marketing_spend': 'sum',
            'profit_margin': 'mean',
            'sales_team_size': 'sum'
        }).reset_index()
        
        monthly_agg['business_unit'] = 'Total'
        
        return monthly_agg
    
    def save_processed_data(self, df: pd.DataFrame, filename: str):
        """Save processed data to CSV"""
        output_path = self.processed_data_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")
    
    def process_all_data(self):
        """Main processing pipeline"""
        logger.info("Starting data processing pipeline...")
        
        try:
            # Load raw data
            revenue_df = self.load_revenue_data()
            kpi_df = self.load_kpi_data()
            
            # Process revenue data
            processed_revenue = self.calculate_derived_metrics(revenue_df)
            aggregated_data = self.aggregate_data(processed_revenue)
            
            # Save processed data
            self.save_processed_data(processed_revenue, 'processed_revenue.csv')
            self.save_processed_data(aggregated_data, 'aggregated_revenue.csv')
            self.save_processed_data(kpi_df, 'processed_kpi.csv')
            
            # Generate summary statistics
            self._generate_data_summary(processed_revenue, kpi_df)
            
            logger.info("Data processing pipeline completed successfully!")
            return processed_revenue, aggregated_data, kpi_df
            
        except Exception as e:
            logger.error(f"Data processing pipeline failed: {e}")
            raise
    
    def _generate_data_summary(self, revenue_df: pd.DataFrame, kpi_df: pd.DataFrame):
        """Generate and save data summary statistics"""
        summary = {
            'data_summary': {
                'revenue_records': len(revenue_df),
                'kpi_records': len(kpi_df),
                'business_units': revenue_df['business_unit'].nunique(),
                'date_range': {
                    'start': revenue_df['date'].min().strftime('%Y-%m-%d'),
                    'end': revenue_df['date'].max().strftime('%Y-%m-%d')
                },
                'total_revenue': revenue_df['revenue'].sum(),
                'avg_monthly_revenue': revenue_df['revenue'].mean(),
                'revenue_growth_rate': revenue_df['revenue_yoy_growth'].mean()
            }
        }
        
        # Save summary as JSON-like format
        summary_path = self.processed_data_dir / 'data_summary.txt'
        with open(summary_path, 'w') as f:
            for key, value in summary['data_summary'].items():
                f.write(f"{key}: {value}\n")
        
        logger.info(f"Data summary saved to {summary_path}")

def main():
    """Main execution function"""
    processor = DataProcessor()
    processor.process_all_data()

if __name__ == "__main__":
    main()