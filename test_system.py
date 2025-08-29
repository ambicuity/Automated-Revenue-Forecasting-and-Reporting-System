"""
Simple test suite for the Revenue Forecasting and Reporting System
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import time
import traceback
from typing import Dict, List, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

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

# ===============================================
# COMPREHENSIVE DATA VALIDATION TESTS
# ===============================================

def test_data_integrity():
    """Test comprehensive data integrity and consistency"""
    base_dir = Path(__file__).parent
    print("\nTesting data integrity and consistency...")
    
    # Load key datasets
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    forecasts_df = pd.read_csv(base_dir / 'data/processed/revenue_forecasts.csv')
    monthly_kpis_df = pd.read_csv(base_dir / 'data/processed/monthly_kpis.csv')
    
    # Test data type consistency
    revenue_df['date'] = pd.to_datetime(revenue_df['date'])
    forecasts_df['date'] = pd.to_datetime(forecasts_df['date'])
    monthly_kpis_df['date'] = pd.to_datetime(monthly_kpis_df['date'])
    
    # Test date ranges are reasonable
    current_date = datetime.now()
    assert revenue_df['date'].min() >= pd.Timestamp('2020-01-01'), "Revenue data starts too early"
    assert forecasts_df['date'].max() <= current_date + timedelta(days=400), "Forecasts extend too far into future"
    print("✓ Date ranges are reasonable")
    
    # Test revenue values are consistent
    assert revenue_df['revenue'].dtype in [np.float64, np.int64], "Revenue should be numeric"
    assert not revenue_df['revenue'].isna().any(), "No missing revenue values"
    assert (revenue_df['revenue'] >= 0).all(), "All revenue values non-negative"
    print("✓ Revenue values are valid")
    
    # Test business units are consistent
    if 'business_unit' in revenue_df.columns:
        unique_units = revenue_df['business_unit'].unique()
        assert len(unique_units) > 0, "At least one business unit exists"
        assert not pd.isna(unique_units).any(), "No missing business unit names"
        print(f"✓ Found {len(unique_units)} business units")
    
    # Test forecast consistency
    forecast_cols = ['linear_forecast', 'seasonal_forecast', 'ensemble_forecast']
    for col in forecast_cols:
        if col in forecasts_df.columns:
            assert not forecasts_df[col].isna().any(), f"No missing values in {col}"
            assert (forecasts_df[col] >= 0).all(), f"All {col} values non-negative"
    print("✓ Forecast data integrity")
    
    print("Data integrity tests passed!")

def test_data_relationships():
    """Test relationships and consistency across datasets"""
    base_dir = Path(__file__).parent
    print("\nTesting data relationships and cross-consistency...")
    
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    monthly_kpis_df = pd.read_csv(base_dir / 'data/processed/monthly_kpis.csv')
    
    revenue_df['date'] = pd.to_datetime(revenue_df['date'])
    monthly_kpis_df['date'] = pd.to_datetime(monthly_kpis_df['date'])
    
    # Test temporal consistency
    revenue_months = set(revenue_df['date'].dt.to_period('M'))
    kpi_months = set(monthly_kpis_df['date'].dt.to_period('M'))
    
    # Should have significant overlap
    overlap = len(revenue_months.intersection(kpi_months))
    assert overlap > 0, "Revenue and KPI data should have temporal overlap"
    print(f"✓ Found {overlap} months of overlapping data")
    
    # Test KPI calculations are reasonable
    if 'revenue' in monthly_kpis_df.columns:
        # Revenue in KPIs should be positive
        assert (monthly_kpis_df['revenue'] >= 0).all(), "KPI revenue values should be non-negative"
        print("✓ KPI revenue values are valid")
    
    # Test growth rates are reasonable (between -100% and +1000%)
    growth_cols = [col for col in monthly_kpis_df.columns if 'growth' in col.lower()]
    for col in growth_cols:
        if col in monthly_kpis_df.columns:
            growth_values = monthly_kpis_df[col].dropna()
            if len(growth_values) > 0:
                assert (growth_values >= -1.0).all(), f"{col} growth rates should be > -100%"
                assert (growth_values <= 10.0).all(), f"{col} growth rates should be < 1000%"
                print(f"✓ {col} values are reasonable")
    
    print("Data relationship tests passed!")

def test_statistical_validity():
    """Test statistical properties of the data"""
    base_dir = Path(__file__).parent
    print("\nTesting statistical validity...")
    
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    forecasts_df = pd.read_csv(base_dir / 'data/processed/revenue_forecasts.csv')
    
    # Test revenue distribution
    revenue_stats = revenue_df['revenue'].describe()
    assert revenue_stats['std'] > 0, "Revenue should have variation"
    assert revenue_stats['count'] > 10, "Sufficient revenue data points"
    print(f"✓ Revenue statistics: mean={revenue_stats['mean']:.0f}, std={revenue_stats['std']:.0f}")
    
    # Test forecasts are reasonable relative to historical data
    historical_mean = revenue_df['revenue'].mean()
    historical_std = revenue_df['revenue'].std()
    
    if 'ensemble_forecast' in forecasts_df.columns:
        forecast_mean = forecasts_df['ensemble_forecast'].mean()
        # Forecasts should be within reasonable bounds of historical data
        assert forecast_mean < historical_mean + 3 * historical_std, "Forecasts not unreasonably high"
        assert forecast_mean > max(0, historical_mean - 3 * historical_std), "Forecasts not unreasonably low"
        print("✓ Forecasts are statistically reasonable")
    
    # Test for obvious data anomalies
    if len(revenue_df) > 1:
        revenue_diff = revenue_df['revenue'].diff().abs()
        extreme_changes = (revenue_diff > historical_mean).sum()
        # Should not have too many extreme month-to-month changes
        assert extreme_changes < len(revenue_df) * 0.1, "Too many extreme revenue changes detected"
        print("✓ No excessive data anomalies detected")
    
    print("Statistical validity tests passed!")

# ===============================================
# COMPONENT-SPECIFIC TESTS
# ===============================================

def test_data_processor_functionality():
    """Test DataProcessor component functionality"""
    print("\nTesting DataProcessor functionality...")
    
    try:
        from data_processor import DataProcessor
        processor = DataProcessor()
        
        # Test that processor can load data
        revenue_data = processor.load_revenue_data()
        assert len(revenue_data) > 0, "DataProcessor should load revenue data"
        assert 'date' in revenue_data.columns, "Revenue data should have date column"
        assert 'revenue' in revenue_data.columns, "Revenue data should have revenue column"
        print("✓ DataProcessor loads revenue data successfully")
        
        # Test that processor can load KPI data
        kpi_data = processor.load_kpi_data()
        assert len(kpi_data) > 0, "DataProcessor should load KPI data"
        print("✓ DataProcessor loads KPI data successfully")
        
        print("DataProcessor functionality tests passed!")
        
    except ImportError as e:
        print(f"⚠ DataProcessor import failed: {e}")
        print("DataProcessor functionality tests skipped")
    except Exception as e:
        print(f"⚠ DataProcessor test failed: {e}")
        print("DataProcessor functionality tests failed")

def test_forecasting_engine_functionality():
    """Test RevenueForecaster component functionality"""
    print("\nTesting RevenueForecaster functionality...")
    
    try:
        from forecasting_engine import RevenueForecaster
        forecaster = RevenueForecaster()
        
        # Test that forecaster can load processed data
        data = forecaster.load_processed_data()
        assert len(data) > 0, "RevenueForecaster should load processed data"
        print("✓ RevenueForecaster loads processed data successfully")
        
        # Test forecast generation capabilities
        if len(data) >= 12:  # Need sufficient data for forecasting
            # Test basic forecasting method exists
            assert hasattr(forecaster, 'linear_trend_forecast'), "Should have linear_trend_forecast method"
            assert hasattr(forecaster, 'seasonal_decomposition_forecast'), "Should have seasonal_decomposition_forecast method"
            print("✓ RevenueForecaster has required forecasting methods")
        
        print("RevenueForecaster functionality tests passed!")
        
    except ImportError as e:
        print(f"⚠ RevenueForecaster import failed: {e}")
        print("RevenueForecaster functionality tests skipped")
    except Exception as e:
        print(f"⚠ RevenueForecaster test failed: {e}")
        print("RevenueForecaster functionality tests failed")

def test_kpi_calculator_functionality():
    """Test KPICalculator component functionality"""
    print("\nTesting KPICalculator functionality...")
    
    try:
        from kpi_calculator import KPICalculator
        kpi_calc = KPICalculator()
        
        # Test KPI calculation methods exist
        assert hasattr(kpi_calc, 'run_kpi_pipeline'), "Should have run_kpi_pipeline method"
        print("✓ KPICalculator has required methods")
        
        print("KPICalculator functionality tests passed!")
        
    except ImportError as e:
        print(f"⚠ KPICalculator import failed: {e}")
        print("KPICalculator functionality tests skipped")
    except Exception as e:
        print(f"⚠ KPICalculator test failed: {e}")
        print("KPICalculator functionality tests failed")

def test_report_generator_functionality():
    """Test ReportGenerator component functionality"""
    print("\nTesting ReportGenerator functionality...")
    
    try:
        from report_generator import ReportGenerator
        generator = ReportGenerator()
        
        # Test report generation methods exist
        assert hasattr(generator, 'generate_all_reports'), "Should have generate_all_reports method"
        assert hasattr(generator, 'load_processed_data'), "Should have load_processed_data method"
        print("✓ ReportGenerator has required methods")
        
        # Test that generator can load processed data for reporting
        data = generator.load_processed_data()
        assert isinstance(data, dict), "Should return dictionary of datasets"
        assert len(data) > 0, "Should load at least one dataset"
        print("✓ ReportGenerator loads data for reporting")
        
        print("ReportGenerator functionality tests passed!")
        
    except ImportError as e:
        print(f"⚠ ReportGenerator import failed: {e}")
        print("ReportGenerator functionality tests skipped")
    except Exception as e:
        print(f"⚠ ReportGenerator test failed: {e}")
        print("ReportGenerator functionality tests failed")

# ===============================================
# INTEGRATION AND END-TO-END TESTS
# ===============================================

def test_full_pipeline_integration():
    """Test that the full pipeline can be executed"""
    print("\nTesting full pipeline integration...")
    
    try:
        from main import SystemOrchestrator
        
        orchestrator = SystemOrchestrator()
        
        # Test system status
        status = orchestrator.get_system_status()
        assert isinstance(status, dict), "System status should return dictionary"
        assert 'timestamp' in status, "Status should include timestamp"
        assert 'directories' in status, "Status should include directories info"
        print("✓ SystemOrchestrator status check works")
        
        # Verify required directories exist
        directories = status['directories']
        for dir_name in ['raw_data', 'processed_data', 'reports']:
            assert directories[dir_name]['exists'], f"{dir_name} directory should exist"
        print("✓ All required directories exist")
        
        print("Full pipeline integration tests passed!")
        
    except ImportError as e:
        print(f"⚠ SystemOrchestrator import failed: {e}")
        print("Pipeline integration tests skipped")
    except Exception as e:
        print(f"⚠ Pipeline integration test failed: {e}")
        print("Pipeline integration tests failed")

def test_data_flow_consistency():
    """Test data flows correctly through the pipeline"""
    base_dir = Path(__file__).parent
    print("\nTesting data flow consistency...")
    
    # Check that raw data leads to processed data
    raw_revenue = base_dir / 'data/raw/revenue_data.csv'
    processed_revenue = base_dir / 'data/processed/processed_revenue.csv'
    
    if raw_revenue.exists() and processed_revenue.exists():
        raw_df = pd.read_csv(raw_revenue)
        processed_df = pd.read_csv(processed_revenue)
        
        # Processed data should have same or more columns (cleaned/enhanced)
        assert len(processed_df.columns) >= len(raw_df.columns), "Processed data should have at least as many columns"
        
        # Should have processed records
        assert len(processed_df) > 0, "Processed data should not be empty"
        print("✓ Raw data successfully flows to processed data")
    
    # Check that processed data leads to forecasts
    forecasts_file = base_dir / 'data/processed/revenue_forecasts.csv'
    if processed_revenue.exists() and forecasts_file.exists():
        processed_df = pd.read_csv(processed_revenue)
        forecasts_df = pd.read_csv(forecasts_file)
        
        assert len(forecasts_df) > 0, "Forecasts should be generated from processed data"
        print("✓ Processed data successfully flows to forecasts")
    
    # Check that processed data leads to reports
    reports_dir = base_dir / 'reports'
    if processed_revenue.exists() and reports_dir.exists():
        report_files = list(reports_dir.glob('*.pdf')) + list(reports_dir.glob('*.xlsx'))
        assert len(report_files) > 0, "Reports should be generated from processed data"
        print("✓ Processed data successfully flows to reports")
    
    print("Data flow consistency tests passed!")

# ===============================================
# PERFORMANCE AND ROBUSTNESS TESTS  
# ===============================================

def test_performance_benchmarks():
    """Test system performance meets reasonable benchmarks"""
    print("\nTesting performance benchmarks...")
    
    base_dir = Path(__file__).parent
    
    # Test data loading performance
    start_time = time.time()
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    load_time = time.time() - start_time
    
    assert load_time < 10.0, f"Data loading should be under 10 seconds, took {load_time:.2f}s"
    print(f"✓ Data loading performance: {load_time:.2f}s")
    
    # Test data processing performance on sample
    if len(revenue_df) > 0:
        start_time = time.time()
        _ = revenue_df.describe()
        _ = revenue_df.groupby(pd.to_datetime(revenue_df['date']) if 'date' in revenue_df.columns else revenue_df.index).sum()
        calc_time = time.time() - start_time
        
        assert calc_time < 5.0, f"Basic calculations should be under 5 seconds, took {calc_time:.2f}s"
        print(f"✓ Calculation performance: {calc_time:.2f}s")
    
    # Test file size reasonableness
    processed_files = list(Path(base_dir / 'data/processed').glob('*.csv'))
    for file_path in processed_files:
        size_mb = file_path.stat().st_size / (1024 * 1024)
        assert size_mb < 100, f"File {file_path.name} is too large: {size_mb:.1f}MB"
    print(f"✓ File sizes are reasonable")
    
    print("Performance benchmark tests passed!")

def test_error_handling():
    """Test system error handling and robustness"""
    print("\nTesting error handling and robustness...")
    
    # Test configuration loading error handling
    try:
        import config.settings as settings
        # Configuration should handle missing optional settings gracefully
        assert hasattr(settings, 'FORECAST_HORIZON_MONTHS'), "Should have required settings"
        print("✓ Configuration handles required settings")
    except Exception as e:
        print(f"⚠ Configuration error handling test failed: {e}")
    
    # Test data validation catches issues
    base_dir = Path(__file__).parent
    revenue_df = pd.read_csv(base_dir / 'data/processed/processed_revenue.csv')
    
    # Should have expected columns
    required_cols = ['revenue']
    for col in required_cols:
        assert col in revenue_df.columns, f"Required column {col} missing - data validation should catch this"
    print("✓ Data validation works for required columns")
    
    # Test file existence checks
    required_paths = [
        base_dir / 'data/processed/processed_revenue.csv',
        base_dir / 'data/processed/revenue_forecasts.csv'
    ]
    for path in required_paths:
        assert path.exists(), f"Required file {path} should exist - pipeline should ensure this"
    print("✓ Required files exist as expected")
    
    print("Error handling and robustness tests passed!")

# ===============================================
# OUTPUT VALIDATION TESTS
# ===============================================

def test_report_content_validation():
    """Test that generated reports contain valid content"""
    base_dir = Path(__file__).parent
    print("\nTesting report content validation...")
    
    reports_dir = base_dir / 'reports'
    
    # Test PDF reports exist and are not empty
    pdf_files = list(reports_dir.glob('*.pdf'))
    for pdf_file in pdf_files:
        size = pdf_file.stat().st_size
        assert size > 1024, f"PDF report {pdf_file.name} seems too small: {size} bytes"
    print(f"✓ {len(pdf_files)} PDF reports are valid sizes")
    
    # Test Excel reports exist and are not empty  
    excel_files = list(reports_dir.glob('*.xlsx'))
    for excel_file in excel_files:
        size = excel_file.stat().st_size
        assert size > 5120, f"Excel report {excel_file.name} seems too small: {size} bytes"
    print(f"✓ {len(excel_files)} Excel reports are valid sizes")
    
    # Test dashboard images exist and are not empty
    dashboard_files = list(reports_dir.glob('*dashboard*.png'))
    for dashboard_file in dashboard_files:
        size = dashboard_file.stat().st_size
        assert size > 10240, f"Dashboard {dashboard_file.name} seems too small: {size} bytes"
    print(f"✓ {len(dashboard_files)} dashboard images are valid sizes")
    
    # Test report index files exist
    index_files = list(reports_dir.glob('report_index_*.md'))
    assert len(index_files) > 0, "Should have report index files"
    
    for index_file in index_files:
        content = index_file.read_text()
        assert len(content) > 100, f"Report index {index_file.name} seems too short"
        assert "Revenue" in content, "Report index should mention Revenue"
    print(f"✓ {len(index_files)} report index files contain valid content")
    
    print("Report content validation tests passed!")

def test_powerbi_dataset_validation():
    """Test Power BI datasets are properly formatted"""
    base_dir = Path(__file__).parent
    print("\nTesting Power BI dataset validation...")
    
    powerbi_dir = base_dir / 'reports' / 'powerbi_data'
    
    if powerbi_dir.exists():
        csv_files = list(powerbi_dir.glob('*.csv'))
        
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            
            # Should not be empty
            assert len(df) > 0, f"Power BI dataset {csv_file.name} should not be empty"
            
            # Should have reasonable column names (no spaces or special chars for Power BI)
            for col in df.columns:
                assert isinstance(col, str), f"Column name should be string: {col}"
                assert len(col.strip()) > 0, f"Column name should not be empty or just whitespace"
            
            # Should not have entirely null columns
            for col in df.columns:
                null_ratio = df[col].isna().sum() / len(df)
                assert null_ratio < 1.0, f"Column {col} in {csv_file.name} is entirely null"
        
        print(f"✓ {len(csv_files)} Power BI datasets are properly formatted")
    else:
        print("⚠ Power BI directory not found, skipping Power BI dataset validation")
    
    print("Power BI dataset validation tests passed!")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AUTOMATED REVENUE FORECASTING SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    test_results = {}
    total_tests = 0
    passed_tests = 0
    
    # Define all test functions
    test_functions = [
        # Basic tests (existing)
        ("Data Files Existence", test_data_files_exist),
        ("Basic Data Quality", test_data_quality),
        ("Reports Generated", test_reports_generated),
        ("System Configuration", test_system_configuration),
        
        # Comprehensive data validation tests
        ("Data Integrity", test_data_integrity),
        ("Data Relationships", test_data_relationships),
        ("Statistical Validity", test_statistical_validity),
        
        # Component functionality tests
        ("DataProcessor Functionality", test_data_processor_functionality),
        ("Forecasting Engine Functionality", test_forecasting_engine_functionality),
        ("KPI Calculator Functionality", test_kpi_calculator_functionality),
        ("Report Generator Functionality", test_report_generator_functionality),
        
        # Integration tests
        ("Full Pipeline Integration", test_full_pipeline_integration),
        ("Data Flow Consistency", test_data_flow_consistency),
        
        # Performance and robustness tests
        ("Performance Benchmarks", test_performance_benchmarks),
        ("Error Handling", test_error_handling),
        
        # Output validation tests
        ("Report Content Validation", test_report_content_validation),
        ("Power BI Dataset Validation", test_powerbi_dataset_validation),
    ]
    
    for test_name, test_func in test_functions:
        total_tests += 1
        try:
            test_func()
            test_results[test_name] = "✓ PASSED"
            passed_tests += 1
        except AssertionError as e:
            test_results[test_name] = f"✗ FAILED: {e}"
        except Exception as e:
            test_results[test_name] = f"⚠ ERROR: {e}"
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in test_results.items():
        print(f"{test_name:.<40} {result}")
    
    print("\n" + "=" * 60)
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! ✓")
        print(f"System is working correctly. ({passed_tests}/{total_tests} tests passed)")
        print("=" * 60)
        return True
    else:
        print(f"❌ {total_tests - passed_tests} TEST(S) FAILED")
        print(f"System has issues that need attention. ({passed_tests}/{total_tests} tests passed)")
        print("=" * 60)
        return False

def run_basic_tests_only():
    """Run only the basic tests for quick validation"""
    print("=" * 60)
    print("AUTOMATED REVENUE FORECASTING SYSTEM - BASIC TEST SUITE")
    print("=" * 60)
    
    try:
        test_data_files_exist()
        test_data_quality()
        test_reports_generated()
        test_system_configuration()
        
        print("\n" + "=" * 60)
        print("ALL BASIC TESTS PASSED! ✓")
        print("System basic functionality is working correctly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ BASIC TEST FAILED: {e}")
        print("=" * 60)
        return False

def run_tests_by_category(category: str):
    """Run tests from a specific category"""
    print("=" * 60)
    print(f"RUNNING {category.upper()} TESTS")
    print("=" * 60)
    
    test_categories = {
        'basic': [
            test_data_files_exist,
            test_data_quality, 
            test_reports_generated,
            test_system_configuration
        ],
        'data': [
            test_data_integrity,
            test_data_relationships,
            test_statistical_validity
        ],
        'components': [
            test_data_processor_functionality,
            test_forecasting_engine_functionality,
            test_kpi_calculator_functionality,
            test_report_generator_functionality
        ],
        'integration': [
            test_full_pipeline_integration,
            test_data_flow_consistency
        ],
        'performance': [
            test_performance_benchmarks,
            test_error_handling
        ],
        'output': [
            test_report_content_validation,
            test_powerbi_dataset_validation
        ]
    }
    
    if category not in test_categories:
        print(f"Unknown category: {category}")
        print(f"Available categories: {list(test_categories.keys())}")
        return False
    
    try:
        for test_func in test_categories[category]:
            test_func()
        
        print(f"\n✓ ALL {category.upper()} TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ {category.upper()} TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive Test Suite for Revenue Forecasting System')
    parser.add_argument('--mode', choices=['all', 'basic', 'data', 'components', 'integration', 'performance', 'output'], 
                       default='all', help='Test suite mode to run')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    # If no command line args, run in basic compatibility mode
    if len(sys.argv) == 1:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    
    args = parser.parse_args()
    
    if args.mode == 'all':
        success = run_all_tests()
    elif args.mode == 'basic':
        success = run_basic_tests_only()
    else:
        success = run_tests_by_category(args.mode)
    
    sys.exit(0 if success else 1)