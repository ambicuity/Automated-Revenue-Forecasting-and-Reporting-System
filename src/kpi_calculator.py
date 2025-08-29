"""
KPI Calculator and Tracker
Calculates and tracks key performance indicators
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import *

# Setup logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class KPICalculator:
    """Calculate and track key performance indicators"""
    
    def __init__(self):
        self.processed_data_dir = PROCESSED_DATA_DIR
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)
        
    def load_data(self) -> tuple:
        """Load processed revenue and KPI data"""
        try:
            # Load revenue data
            revenue_path = self.processed_data_dir / "processed_revenue.csv"
            revenue_df = pd.read_csv(revenue_path)
            revenue_df['date'] = pd.to_datetime(revenue_df['date'])
            
            # Load KPI data
            kpi_path = self.processed_data_dir / "processed_kpi.csv"
            kpi_df = pd.read_csv(kpi_path)
            kpi_df['date'] = pd.to_datetime(kpi_df['date'])
            
            logger.info(f"Loaded revenue data: {len(revenue_df)} records")
            logger.info(f"Loaded KPI data: {len(kpi_df)} records")
            
            return revenue_df, kpi_df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def calculate_revenue_kpis(self, revenue_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate revenue-related KPIs"""
        logger.info("Calculating revenue KPIs...")
        
        # Group by date for overall metrics
        monthly_metrics = revenue_df.groupby('date').agg({
            'revenue': 'sum',
            'customer_count': 'sum',
            'marketing_spend': 'sum',
            'profit_margin': 'mean',
            'sales_team_size': 'sum'
        }).reset_index()
        
        # Calculate KPIs
        kpis = monthly_metrics.copy()
        
        # Revenue growth metrics
        kpis['revenue_mom_growth'] = kpis['revenue'].pct_change()
        kpis['revenue_yoy_growth'] = kpis['revenue'].pct_change(periods=12)
        kpis['revenue_3m_avg'] = kpis['revenue'].rolling(window=3).mean()
        kpis['revenue_12m_avg'] = kpis['revenue'].rolling(window=12).mean()
        
        # Customer metrics
        kpis['customer_mom_growth'] = kpis['customer_count'].pct_change()
        kpis['revenue_per_customer'] = kpis['revenue'] / kpis['customer_count']
        kpis['customers_per_salesperson'] = kpis['customer_count'] / kpis['sales_team_size']
        
        # Marketing metrics
        kpis['marketing_roi'] = kpis['revenue'] / kpis['marketing_spend']
        kpis['marketing_spend_ratio'] = kpis['marketing_spend'] / kpis['revenue']
        
        # Performance indicators
        kpis['revenue_target_achievement'] = kpis['revenue_yoy_growth'] / REVENUE_GROWTH_TARGET
        kpis['profit_margin_vs_target'] = kpis['profit_margin'] / PROFIT_MARGIN_TARGET
        
        return kpis
    
    def calculate_business_unit_kpis(self, revenue_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate KPIs by business unit"""
        logger.info("Calculating business unit KPIs...")
        
        unit_kpis = []
        
        for unit in revenue_df['business_unit'].unique():
            unit_data = revenue_df[revenue_df['business_unit'] == unit].copy()
            unit_data = unit_data.sort_values('date')
            
            # Calculate unit-specific metrics
            latest_month = unit_data.iloc[-1]
            previous_month = unit_data.iloc[-2] if len(unit_data) > 1 else unit_data.iloc[-1]
            same_month_last_year = unit_data[unit_data['date'] <= 
                                           latest_month['date'] - timedelta(days=300)]
            
            if not same_month_last_year.empty:
                same_month_last_year = same_month_last_year.iloc[-1]
            else:
                same_month_last_year = latest_month
            
            # KPI calculations
            unit_kpis.append({
                'business_unit': unit,
                'latest_month': latest_month['date'],
                'current_revenue': latest_month['revenue'],
                'previous_month_revenue': previous_month['revenue'],
                'mom_growth': (latest_month['revenue'] - previous_month['revenue']) / previous_month['revenue'],
                'yoy_growth': (latest_month['revenue'] - same_month_last_year['revenue']) / same_month_last_year['revenue'],
                'ytd_revenue': unit_data[unit_data['date'].dt.year == latest_month['date'].year]['revenue'].sum(),
                'avg_monthly_revenue': unit_data['revenue'].mean(),
                'revenue_volatility': unit_data['revenue'].std() / unit_data['revenue'].mean(),
                'customer_count': latest_month['customer_count'],
                'revenue_per_customer': latest_month['revenue'] / latest_month['customer_count'] if latest_month['customer_count'] > 0 else 0,
                'profit_margin': latest_month['profit_margin'],
                'marketing_roi': latest_month['revenue'] / latest_month['marketing_spend'] if latest_month['marketing_spend'] > 0 else 0
            })
        
        return pd.DataFrame(unit_kpis)
    
    def calculate_advanced_kpis(self, revenue_df: pd.DataFrame, kpi_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate advanced KPIs combining multiple data sources"""
        logger.info("Calculating advanced KPIs...")
        
        # Merge datasets on date
        merged_df = pd.merge(
            revenue_df.groupby('date').agg({
                'revenue': 'sum',
                'customer_count': 'sum',
                'marketing_spend': 'sum'
            }).reset_index(),
            kpi_df,
            on='date',
            how='outer'
        ).ffill()
        
        # Calculate advanced metrics
        advanced_kpis = merged_df.copy()
        
        # Customer lifetime metrics
        advanced_kpis['clv_to_cac_ratio'] = (
            advanced_kpis['customer_lifetime_value'] / 
            advanced_kpis['customer_acquisition_cost']
        )
        
        # Market efficiency metrics
        advanced_kpis['market_penetration'] = advanced_kpis['customer_count'] * advanced_kpis['market_share']
        
        # Customer health metrics
        advanced_kpis['customer_health_score'] = (
            advanced_kpis['retention_rate'] * 0.4 +
            advanced_kpis['net_promoter_score'] / 100 * 0.3 +
            advanced_kpis['conversion_rate'] * 0.3
        )
        
        # Revenue quality metrics
        advanced_kpis['revenue_quality_score'] = (
            advanced_kpis['retention_rate'] * 0.5 +
            (1 - advanced_kpis['churn_rate']) * 0.5
        )
        
        return advanced_kpis
    
    def identify_performance_alerts(self, unit_kpis: pd.DataFrame, advanced_kpis: pd.DataFrame) -> list:
        """Identify performance issues requiring attention"""
        logger.info("Identifying performance alerts...")
        
        alerts = []
        
        # Revenue growth alerts
        for _, unit in unit_kpis.iterrows():
            if unit['yoy_growth'] < 0:
                alerts.append({
                    'type': 'Revenue Decline',
                    'business_unit': unit['business_unit'],
                    'message': f"YoY revenue decline of {unit['yoy_growth']:.1%}",
                    'severity': 'High'
                })
            
            if unit['mom_growth'] < -0.1:  # 10% decline
                alerts.append({
                    'type': 'Monthly Revenue Drop',
                    'business_unit': unit['business_unit'],
                    'message': f"MoM revenue decline of {unit['mom_growth']:.1%}",
                    'severity': 'Medium'
                })
            
            if unit['profit_margin'] < PROFIT_MARGIN_TARGET:
                alerts.append({
                    'type': 'Low Profit Margin',
                    'business_unit': unit['business_unit'],
                    'message': f"Profit margin {unit['profit_margin']:.1%} below target {PROFIT_MARGIN_TARGET:.1%}",
                    'severity': 'Medium'
                })
        
        # Customer metrics alerts
        latest_advanced = advanced_kpis.iloc[-1]
        
        if latest_advanced['retention_rate'] < CUSTOMER_RETENTION_TARGET:
            alerts.append({
                'type': 'Low Retention Rate',
                'business_unit': 'All',
                'message': f"Retention rate {latest_advanced['retention_rate']:.1%} below target {CUSTOMER_RETENTION_TARGET:.1%}",
                'severity': 'High'
            })
        
        if latest_advanced['churn_rate'] > 0.05:  # 5% monthly churn
            alerts.append({
                'type': 'High Churn Rate',
                'business_unit': 'All',
                'message': f"Churn rate {latest_advanced['churn_rate']:.1%} exceeds 5%",
                'severity': 'High'
            })
        
        if latest_advanced['clv_to_cac_ratio'] < 3:  # Industry standard
            alerts.append({
                'type': 'Low CLV/CAC Ratio',
                'business_unit': 'All',
                'message': f"CLV/CAC ratio {latest_advanced['clv_to_cac_ratio']:.1f} below recommended 3:1",
                'severity': 'Medium'
            })
        
        logger.info(f"Identified {len(alerts)} performance alerts")
        return alerts
    
    def create_kpi_dashboard_data(self, monthly_kpis: pd.DataFrame, unit_kpis: pd.DataFrame, 
                                 advanced_kpis: pd.DataFrame, alerts: list) -> dict:
        """Create comprehensive KPI dashboard data"""
        logger.info("Creating KPI dashboard data...")
        
        latest_month = monthly_kpis.iloc[-1]
        
        dashboard_data = {
            'summary_metrics': {
                'total_revenue': latest_month['revenue'],
                'revenue_growth_yoy': latest_month['revenue_yoy_growth'],
                'revenue_growth_mom': latest_month['revenue_mom_growth'],
                'total_customers': latest_month['customer_count'],
                'revenue_per_customer': latest_month['revenue_per_customer'],
                'profit_margin': latest_month['profit_margin'],
                'marketing_roi': latest_month['marketing_roi']
            },
            'unit_performance': unit_kpis.to_dict('records'),
            'trending_metrics': {
                'revenue_trend': monthly_kpis[['date', 'revenue']].tail(12).to_dict('records'),
                'customer_trend': monthly_kpis[['date', 'customer_count']].tail(12).to_dict('records'),
                'margin_trend': monthly_kpis[['date', 'profit_margin']].tail(12).to_dict('records')
            },
            'advanced_metrics': {
                'customer_health': advanced_kpis['customer_health_score'].iloc[-1],
                'revenue_quality': advanced_kpis['revenue_quality_score'].iloc[-1],
                'clv_cac_ratio': advanced_kpis['clv_to_cac_ratio'].iloc[-1],
                'nps_score': advanced_kpis['net_promoter_score'].iloc[-1]
            },
            'alerts': alerts
        }
        
        return dashboard_data
    
    def create_kpi_visualizations(self, monthly_kpis: pd.DataFrame, unit_kpis: pd.DataFrame):
        """Create KPI visualization charts"""
        logger.info("Creating KPI visualizations...")
        
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Key Performance Indicators Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Revenue trend
        ax1 = axes[0, 0]
        ax1.plot(monthly_kpis['date'], monthly_kpis['revenue'] / 1000, linewidth=2, color='blue')
        ax1.set_title('Monthly Revenue Trend', fontweight='bold')
        ax1.set_ylabel('Revenue ($000s)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. YoY Growth
        ax2 = axes[0, 1]
        growth_data = monthly_kpis[monthly_kpis['revenue_yoy_growth'].notna()]
        colors = ['green' if x >= 0 else 'red' for x in growth_data['revenue_yoy_growth']]
        ax2.bar(range(len(growth_data)), growth_data['revenue_yoy_growth'] * 100, color=colors)
        ax2.set_title('Year-over-Year Revenue Growth', fontweight='bold')
        ax2.set_ylabel('Growth Rate (%)')
        ax2.axhline(y=REVENUE_GROWTH_TARGET * 100, color='orange', linestyle='--', label='Target')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Customer metrics
        ax3 = axes[0, 2]
        ax3.plot(monthly_kpis['date'], monthly_kpis['customer_count'], linewidth=2, color='purple')
        ax3.set_title('Customer Count Trend', fontweight='bold')
        ax3.set_ylabel('Number of Customers')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Business unit revenue comparison
        ax4 = axes[1, 0]
        unit_revenues = unit_kpis['current_revenue'] / 1000
        ax4.bar(unit_kpis['business_unit'], unit_revenues, color='skyblue')
        ax4.set_title('Current Month Revenue by Unit', fontweight='bold')
        ax4.set_ylabel('Revenue ($000s)')
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Profit margin trend
        ax5 = axes[1, 1]
        ax5.plot(monthly_kpis['date'], monthly_kpis['profit_margin'] * 100, linewidth=2, color='green')
        ax5.axhline(y=PROFIT_MARGIN_TARGET * 100, color='red', linestyle='--', label='Target')
        ax5.set_title('Profit Margin Trend', fontweight='bold')
        ax5.set_ylabel('Profit Margin (%)')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.tick_params(axis='x', rotation=45)
        
        # 6. Marketing ROI
        ax6 = axes[1, 2]
        ax6.plot(monthly_kpis['date'], monthly_kpis['marketing_roi'], linewidth=2, color='orange')
        ax6.set_title('Marketing ROI Trend', fontweight='bold')
        ax6.set_ylabel('ROI Ratio')
        ax6.grid(True, alpha=0.3)
        ax6.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save the plot
        plot_path = self.reports_dir / 'kpi_dashboard.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        logger.info(f"KPI dashboard saved to {plot_path}")
        plt.close()
    
    def save_kpi_results(self, monthly_kpis: pd.DataFrame, unit_kpis: pd.DataFrame, 
                        advanced_kpis: pd.DataFrame, dashboard_data: dict, alerts: list):
        """Save all KPI results"""
        # Save dataframes
        monthly_kpis.to_csv(self.processed_data_dir / 'monthly_kpis.csv', index=False)
        unit_kpis.to_csv(self.processed_data_dir / 'unit_kpis.csv', index=False)
        advanced_kpis.to_csv(self.processed_data_dir / 'advanced_kpis.csv', index=False)
        
        # Save alerts
        alerts_df = pd.DataFrame(alerts)
        alerts_df.to_csv(self.processed_data_dir / 'performance_alerts.csv', index=False)
        
        # Save dashboard summary
        summary_path = self.processed_data_dir / 'kpi_summary.txt'
        with open(summary_path, 'w') as f:
            f.write("KPI Dashboard Summary\n")
            f.write("=" * 20 + "\n\n")
            
            f.write("Summary Metrics:\n")
            for key, value in dashboard_data['summary_metrics'].items():
                if isinstance(value, float):
                    if 'growth' in key or 'margin' in key:
                        f.write(f"  {key.replace('_', ' ').title()}: {value:.1%}\n")
                    elif 'revenue' in key or 'customer' in key:
                        f.write(f"  {key.replace('_', ' ').title()}: {value:,.0f}\n")
                    else:
                        f.write(f"  {key.replace('_', ' ').title()}: {value:.2f}\n")
                else:
                    f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
            
            f.write(f"\nPerformance Alerts: {len(alerts)} issues identified\n")
            for alert in alerts[:5]:  # Show top 5 alerts
                f.write(f"  - {alert['type']}: {alert['message']}\n")
        
        logger.info(f"KPI results saved to {self.processed_data_dir}")
    
    def run_kpi_pipeline(self):
        """Main KPI calculation pipeline"""
        logger.info("Starting KPI calculation pipeline...")
        
        try:
            # Load data
            revenue_df, kpi_df = self.load_data()
            
            # Calculate KPIs
            monthly_kpis = self.calculate_revenue_kpis(revenue_df)
            unit_kpis = self.calculate_business_unit_kpis(revenue_df)
            advanced_kpis = self.calculate_advanced_kpis(revenue_df, kpi_df)
            
            # Identify alerts
            alerts = self.identify_performance_alerts(unit_kpis, advanced_kpis)
            
            # Create dashboard data
            dashboard_data = self.create_kpi_dashboard_data(monthly_kpis, unit_kpis, advanced_kpis, alerts)
            
            # Create visualizations
            self.create_kpi_visualizations(monthly_kpis, unit_kpis)
            
            # Save results
            self.save_kpi_results(monthly_kpis, unit_kpis, advanced_kpis, dashboard_data, alerts)
            
            logger.info("KPI calculation pipeline completed successfully!")
            return dashboard_data
            
        except Exception as e:
            logger.error(f"KPI pipeline failed: {e}")
            raise

def main():
    """Main execution function"""
    calculator = KPICalculator()
    calculator.run_kpi_pipeline()

if __name__ == "__main__":
    main()