"""
Revenue Forecasting Engine
Implements various forecasting models for revenue prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
import os
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import *

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class RevenueForecaster:
    """Revenue forecasting using multiple models"""
    
    def __init__(self):
        self.processed_data_dir = PROCESSED_DATA_DIR
        self.models = {}
        self.forecasts = {}
        self.scaler = StandardScaler()
        
    def load_processed_data(self) -> pd.DataFrame:
        """Load processed revenue data"""
        try:
            file_path = self.processed_data_dir / "processed_revenue.csv"
            if not file_path.exists():
                raise FileNotFoundError(f"Processed data not found. Please run data_processor.py first.")
                
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'])
            logger.info(f"Loaded processed data: {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error loading processed data: {e}")
            raise
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepare features for forecasting models"""
        logger.info("Preparing features for forecasting...")
        
        # Create time-based features
        df = df.copy()
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['year'] = df['date'].dt.year
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        # Seasonal features
        df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
        df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Lag features
        df = df.sort_values(['business_unit', 'date'])
        df['revenue_lag1'] = df.groupby('business_unit')['revenue'].shift(1)
        df['revenue_lag3'] = df.groupby('business_unit')['revenue'].shift(3)
        df['revenue_lag12'] = df.groupby('business_unit')['revenue'].shift(12)
        
        # Fill missing values with forward fill then backward fill
        df = df.ffill().bfill()
        
        # Feature columns
        feature_cols = ['days_since_start', 'month', 'quarter', 'sin_month', 'cos_month', 
                       'customer_count', 'marketing_spend', 'sales_team_size',
                       'revenue_lag1', 'revenue_lag3']
        
        # Filter out revenue_lag12 if not enough historical data
        if 'revenue_lag12' in df.columns and not df['revenue_lag12'].isna().all():
            feature_cols.append('revenue_lag12')
        
        return df, feature_cols
    
    def linear_trend_forecast(self, df: pd.DataFrame) -> dict:
        """Linear trend forecasting model"""
        logger.info("Running linear trend forecasting...")
        
        results = {}
        
        for unit in df['business_unit'].unique():
            unit_data = df[df['business_unit'] == unit].copy()
            
            if len(unit_data) < MIN_HISTORICAL_PERIODS:
                logger.warning(f"Insufficient data for {unit}, skipping...")
                continue
            
            # Prepare features
            unit_data['time_index'] = range(len(unit_data))
            X = unit_data[['time_index']].values
            y = unit_data['revenue'].values
            
            # Split data
            split_point = int(len(X) * 0.8)
            X_train, X_test = X[:split_point], X[split_point:]
            y_train, y_test = y[:split_point], y[split_point:]
            
            # Train model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Future forecasts
            future_periods = FORECAST_HORIZON_MONTHS
            last_index = len(unit_data)
            future_X = np.array([[last_index + i] for i in range(1, future_periods + 1)])
            future_forecast = model.predict(future_X)
            
            # Generate future dates
            last_date = unit_data['date'].max()
            future_dates = pd.date_range(
                start=last_date + pd.DateOffset(months=1), 
                periods=future_periods, 
                freq='MS'
            )
            
            results[unit] = {
                'model': model,
                'metrics': {'mae': mae, 'mse': mse, 'r2': r2},
                'forecast': future_forecast,
                'forecast_dates': future_dates,
                'historical_fit': model.predict(X)
            }
            
            logger.info(f"{unit} - Linear model R²: {r2:.3f}, MAE: ${mae:,.0f}")
        
        return results
    
    def seasonal_decomposition_forecast(self, df: pd.DataFrame) -> dict:
        """Seasonal decomposition with trend forecasting"""
        logger.info("Running seasonal decomposition forecasting...")
        
        results = {}
        
        for unit in df['business_unit'].unique():
            unit_data = df[df['business_unit'] == unit].copy()
            
            if len(unit_data) < MIN_HISTORICAL_PERIODS:
                continue
            
            # Simple seasonal decomposition
            unit_data = unit_data.sort_values('date')
            unit_data['month'] = unit_data['date'].dt.month
            
            # Calculate seasonal factors
            monthly_avg = unit_data.groupby('month')['revenue'].mean()
            overall_avg = unit_data['revenue'].mean()
            seasonal_factors = monthly_avg / overall_avg
            
            # Deseasonalize data
            unit_data['seasonal_factor'] = unit_data['month'].map(seasonal_factors)
            unit_data['deseasonalized'] = unit_data['revenue'] / unit_data['seasonal_factor']
            
            # Trend forecast on deseasonalized data
            X = np.array(range(len(unit_data))).reshape(-1, 1)
            y = unit_data['deseasonalized'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Future trend predictions
            future_periods = FORECAST_HORIZON_MONTHS
            future_X = np.array(range(len(unit_data), len(unit_data) + future_periods)).reshape(-1, 1)
            future_trend = model.predict(future_X)
            
            # Generate future dates and apply seasonality
            last_date = unit_data['date'].max()
            future_dates = pd.date_range(
                start=last_date + pd.DateOffset(months=1), 
                periods=future_periods, 
                freq='MS'
            )
            
            future_months = future_dates.month
            future_seasonal = [seasonal_factors.get(month, 1.0) for month in future_months]
            future_forecast = future_trend * future_seasonal
            
            results[unit] = {
                'model': model,
                'seasonal_factors': seasonal_factors,
                'forecast': future_forecast,
                'forecast_dates': future_dates
            }
        
        return results
    
    def generate_confidence_intervals(self, forecast: np.array, historical_errors: np.array) -> dict:
        """Generate confidence intervals for forecasts"""
        std_error = np.std(historical_errors)
        
        intervals = {}
        for confidence in CONFIDENCE_INTERVALS:
            z_score = {0.8: 1.28, 0.95: 1.96}[confidence]
            margin = z_score * std_error
            
            intervals[f'{int(confidence*100)}%'] = {
                'lower': forecast - margin,
                'upper': forecast + margin
            }
        
        return intervals
    
    def create_forecast_summary(self, linear_results: dict, seasonal_results: dict) -> pd.DataFrame:
        """Create summary of all forecasts"""
        logger.info("Creating forecast summary...")
        
        summary_data = []
        
        for unit in linear_results.keys():
            if unit in seasonal_results:
                linear_forecast = linear_results[unit]['forecast']
                seasonal_forecast = seasonal_results[unit]['forecast']
                dates = linear_results[unit]['forecast_dates']
                
                # Ensemble forecast (average of both methods)
                ensemble_forecast = (linear_forecast + seasonal_forecast) / 2
                
                for i, date in enumerate(dates):
                    summary_data.append({
                        'date': date,
                        'business_unit': unit,
                        'linear_forecast': linear_forecast[i],
                        'seasonal_forecast': seasonal_forecast[i],
                        'ensemble_forecast': ensemble_forecast[i],
                        'forecast_type': 'prediction'
                    })
        
        return pd.DataFrame(summary_data)
    
    def save_forecasts(self, summary_df: pd.DataFrame):
        """Save forecast results"""
        output_path = self.processed_data_dir / 'revenue_forecasts.csv'
        summary_df.to_csv(output_path, index=False)
        logger.info(f"Forecasts saved to {output_path}")
    
    def create_forecast_plots(self, df: pd.DataFrame, forecasts_df: pd.DataFrame):
        """Create visualization of forecasts"""
        logger.info("Creating forecast visualizations...")
        
        plt.figure(figsize=(15, 10))
        
        units = df['business_unit'].unique()
        n_units = len(units)
        cols = 2
        rows = (n_units + 1) // 2
        
        for i, unit in enumerate(units, 1):
            plt.subplot(rows, cols, i)
            
            # Historical data
            unit_data = df[df['business_unit'] == unit]
            plt.plot(unit_data['date'], unit_data['revenue'], 
                    label='Historical', color='blue', linewidth=2)
            
            # Forecasts
            unit_forecasts = forecasts_df[forecasts_df['business_unit'] == unit]
            if not unit_forecasts.empty:
                plt.plot(unit_forecasts['date'], unit_forecasts['ensemble_forecast'], 
                        label='Forecast', color='red', linestyle='--', linewidth=2)
            
            plt.title(f'{unit} Revenue Forecast', fontsize=12, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Revenue ($)')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Format y-axis
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
        
        plt.tight_layout()
        
        # Save plot
        plot_path = REPORTS_DIR / 'revenue_forecasts.png'
        REPORTS_DIR.mkdir(exist_ok=True)
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"Forecast plots saved to {plot_path}")
        plt.close()
    
    def run_forecasting_pipeline(self):
        """Main forecasting pipeline"""
        logger.info("Starting revenue forecasting pipeline...")
        
        try:
            # Load data
            df = self.load_processed_data()
            
            # Prepare features
            df_features, feature_cols = self.prepare_features(df)
            
            # Run forecasting models
            linear_results = self.linear_trend_forecast(df_features)
            seasonal_results = self.seasonal_decomposition_forecast(df_features)
            
            # Create forecast summary
            forecasts_df = self.create_forecast_summary(linear_results, seasonal_results)
            
            # Save results
            self.save_forecasts(forecasts_df)
            
            # Create visualizations
            self.create_forecast_plots(df, forecasts_df)
            
            # Generate forecast summary statistics
            self._generate_forecast_summary(forecasts_df)
            
            logger.info("Revenue forecasting pipeline completed successfully!")
            return forecasts_df
            
        except Exception as e:
            logger.error(f"Forecasting pipeline failed: {e}")
            raise
    
    def _generate_forecast_summary(self, forecasts_df: pd.DataFrame):
        """Generate summary statistics for forecasts"""
        if forecasts_df.empty:
            return
            
        summary_stats = {
            'forecast_period': f"{forecasts_df['date'].min().strftime('%Y-%m')} to {forecasts_df['date'].max().strftime('%Y-%m')}",
            'total_forecast_revenue': forecasts_df['ensemble_forecast'].sum(),
            'avg_monthly_forecast': forecasts_df['ensemble_forecast'].mean(),
            'business_units_forecasted': forecasts_df['business_unit'].nunique(),
            'forecast_records': len(forecasts_df)
        }
        
        # Save summary
        summary_path = self.processed_data_dir / 'forecast_summary.txt'
        with open(summary_path, 'w') as f:
            f.write("Revenue Forecast Summary\n")
            f.write("=" * 25 + "\n\n")
            for key, value in summary_stats.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        logger.info(f"Forecast summary saved to {summary_path}")

def main():
    """Main execution function"""
    forecaster = RevenueForecaster()
    forecaster.run_forecasting_pipeline()

if __name__ == "__main__":
    main()