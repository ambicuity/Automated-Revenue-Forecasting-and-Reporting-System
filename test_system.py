"""
Simple test suite for the Revenue Forecasting and Reporting System
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_data_files_exist():
    """Test that required data files exist"""
    base_dir = Path(__file__).parent
    required_files = [
        'data/raw/revenue_data.csv',
        'data/raw/kpi_data.csv',
        'data/processed/processed_revenue.csv',
        'data/processed/monthly_kpis.csv',
        'data/processed/revenue_forecasts.csv'
    ]
    
    print("Testing data file existence...")
    for file_path in required_files:
        full_path = base_dir / file_path
        assert full_path.exists(), f"Required file missing: {file_path}"
        print(f"✓ {file_path}")
    
    print("All data files exist!")

def test_data_quality():
    """Test basic data quality"""
    base_dir = Path(__file__).parent
    
    print("\nTesting data quality...")
    
    # Test revenue data
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    assert len(revenue_df) > 0, "Revenue data is empty"
    assert 'revenue' in revenue_df.columns, "Revenue column missing"
    assert 'business_unit' in revenue_df.columns, "Business unit column missing"
    assert revenue_df['revenue'].min() >= 0, "Negative revenue values found"
    print("✓ Revenue data quality")
    
    # Test forecasts
    forecast_df = pd.read_csv(base_dir / 'data/processed/revenue_forecasts.csv')
    assert len(forecast_df) > 0, "Forecast data is empty"
    assert 'ensemble_forecast' in forecast_df.columns, "Ensemble forecast missing"
    print("✓ Forecast data quality")
    
    print("All data quality checks passed!")

def test_reports_generated():
    """Test that reports were generated"""
    base_dir = Path(__file__).parent
    reports_dir = base_dir / 'reports'
    
    print("\nTesting report generation...")
    
    # Check for key report files
    report_files = list(reports_dir.glob('*.pdf'))
    assert len(report_files) > 0, "No PDF reports found"
    print(f"✓ Found {len(report_files)} PDF report(s)")
    
    excel_files = list(reports_dir.glob('*.xlsx'))
    assert len(excel_files) > 0, "No Excel reports found"
    print(f"✓ Found {len(excel_files)} Excel report(s)")
    
    dashboard_files = list(reports_dir.glob('*dashboard*.png'))
    assert len(dashboard_files) > 0, "No dashboard visualizations found"
    print(f"✓ Found {len(dashboard_files)} dashboard(s)")
    
    # Check Power BI data
    powerbi_dir = reports_dir / 'powerbi_data'
    if powerbi_dir.exists():
        powerbi_files = list(powerbi_dir.glob('*.csv'))
        print(f"✓ Found {len(powerbi_files)} Power BI dataset(s)")
    
    print("All report generation checks passed!")

def test_system_configuration():
    """Test system configuration"""
    print("\nTesting system configuration...")
    
    try:
        import config.settings as settings
        assert settings.FORECAST_HORIZON_MONTHS > 0, "Invalid forecast horizon"
        assert settings.REVENUE_GROWTH_TARGET > 0, "Invalid growth target"
        print("✓ Configuration loaded successfully")
    except ImportError:
        print("✗ Configuration import failed")
        raise
    
    print("Configuration tests passed!")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AUTOMATED REVENUE FORECASTING SYSTEM - TEST SUITE")
    print("=" * 60)
    
    try:
        test_data_files_exist()
        test_data_quality()
        test_reports_generated()
        test_system_configuration()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("System is working correctly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)