"""
Pytest-compatible test wrapper
Enables running the comprehensive test suite with pytest for CI/CD integration
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

# Import all test functions from test_system
from test_system import (
    test_data_files_exist,
    test_data_quality,
    test_reports_generated,
    test_system_configuration,
    test_data_integrity,
    test_data_relationships,
    test_statistical_validity,
    test_data_processor_functionality,
    test_forecasting_engine_functionality,
    test_kpi_calculator_functionality,
    test_report_generator_functionality,
    test_full_pipeline_integration,
    test_data_flow_consistency,
    test_performance_benchmarks,
    test_error_handling,
    test_report_content_validation,
    test_powerbi_dataset_validation
)

@pytest.mark.basic
class TestBasicFunctionality:
    """Basic system functionality tests"""
    
    def test_data_files_exist(self):
        """Test that required data files exist"""
        test_data_files_exist()
    
    def test_data_quality(self):
        """Test basic data quality"""
        test_data_quality()
    
    def test_reports_generated(self):
        """Test that reports were generated"""
        test_reports_generated()
    
    def test_system_configuration(self):
        """Test system configuration"""
        test_system_configuration()

@pytest.mark.data
class TestDataValidation:
    """Comprehensive data validation tests"""
    
    def test_data_integrity(self):
        """Test comprehensive data integrity and consistency"""
        test_data_integrity()
    
    def test_data_relationships(self):
        """Test relationships and consistency across datasets"""
        test_data_relationships()
    
    def test_statistical_validity(self):
        """Test statistical properties of the data"""
        test_statistical_validity()

@pytest.mark.components
class TestComponentFunctionality:
    """Component-specific functionality tests"""
    
    def test_data_processor_functionality(self):
        """Test DataProcessor component functionality"""
        test_data_processor_functionality()
    
    def test_forecasting_engine_functionality(self):
        """Test RevenueForecaster component functionality"""  
        test_forecasting_engine_functionality()
    
    def test_kpi_calculator_functionality(self):
        """Test KPICalculator component functionality"""
        test_kpi_calculator_functionality()
    
    def test_report_generator_functionality(self):
        """Test ReportGenerator component functionality"""
        test_report_generator_functionality()

@pytest.mark.integration
class TestIntegration:
    """Integration and end-to-end tests"""
    
    def test_full_pipeline_integration(self):
        """Test that the full pipeline can be executed"""
        test_full_pipeline_integration()
    
    def test_data_flow_consistency(self):
        """Test data flows correctly through the pipeline"""
        test_data_flow_consistency()

@pytest.mark.performance
class TestPerformanceAndRobustness:
    """Performance and robustness tests"""
    
    def test_performance_benchmarks(self):
        """Test system performance meets reasonable benchmarks"""
        test_performance_benchmarks()
    
    def test_error_handling(self):
        """Test system error handling and robustness"""
        test_error_handling()

@pytest.mark.output
class TestOutputValidation:
    """Output validation tests"""
    
    def test_report_content_validation(self):
        """Test that generated reports contain valid content"""
        test_report_content_validation()
    
    def test_powerbi_dataset_validation(self):
        """Test Power BI datasets are properly formatted"""
        test_powerbi_dataset_validation()