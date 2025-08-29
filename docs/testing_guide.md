# Testing Guide

This guide explains the comprehensive testing framework for the Automated Revenue Forecasting and Reporting System.

## Quick Start

Run the complete test suite:
```bash
python test_system.py
```

## Test Modes

The testing framework supports different modes for different needs:

### All Tests (Default)
```bash
python test_system.py --mode all
```
Runs all 17 comprehensive tests covering every aspect of the system.

### Basic Tests Only
```bash
python test_system.py --mode basic
```
Runs only the essential 4 tests for quick validation:
- Data files existence
- Basic data quality 
- Reports generated
- System configuration

### Category-Specific Tests

#### Data Validation Tests
```bash
python test_system.py --mode data
```
Tests data integrity, relationships, and statistical validity:
- Data type consistency
- Date range validation
- Cross-dataset relationships
- Statistical properties
- Business logic validation

#### Component Tests
```bash
python test_system.py --mode components
```
Tests individual system components:
- DataProcessor functionality
- RevenueForecaster functionality
- KPICalculator functionality
- ReportGenerator functionality

#### Integration Tests
```bash
python test_system.py --mode integration
```
Tests system integration and data flow:
- Full pipeline integration
- Data flow consistency
- End-to-end validation

#### Performance Tests
```bash
python test_system.py --mode performance
```
Tests system performance and robustness:
- Execution speed benchmarks
- Memory usage validation
- Error handling capabilities
- System reliability

#### Output Tests
```bash
python test_system.py --mode output
```
Tests generated outputs and reports:
- Report content validation
- Power BI dataset validation
- File format validation
- Content quality checks

## Test Categories Explained

### 1. Basic Tests
Essential tests that verify the system's fundamental functionality:
- **Data Files Existence**: Verifies all required data files are present
- **Basic Data Quality**: Checks for empty datasets, required columns, and basic validation
- **Reports Generated**: Confirms PDF, Excel, and dashboard files were created
- **System Configuration**: Validates configuration loading and required settings

### 2. Data Validation Tests
Comprehensive validation of data quality and consistency:
- **Data Integrity**: Tests data types, ranges, and basic validity rules
- **Data Relationships**: Validates consistency across related datasets
- **Statistical Validity**: Checks statistical properties and identifies anomalies

### 3. Component Functionality Tests
Tests each major system component individually:
- **DataProcessor**: Data loading and processing capabilities
- **RevenueForecaster**: Forecasting model functionality
- **KPICalculator**: KPI calculation methods
- **ReportGenerator**: Report generation capabilities

### 4. Integration Tests
Tests system-wide integration and data flow:
- **Full Pipeline Integration**: End-to-end pipeline execution
- **Data Flow Consistency**: Validates data flows correctly between components

### 5. Performance Tests
Tests system performance characteristics:
- **Performance Benchmarks**: Execution time and resource usage
- **Error Handling**: System robustness and error recovery

### 6. Output Validation Tests
Validates the quality and format of generated outputs:
- **Report Content Validation**: PDF, Excel, and image file validation
- **Power BI Dataset Validation**: CSV format and content validation

## Test Results

The testing framework provides detailed results with:
- ✓ **PASSED**: Test completed successfully
- ✗ **FAILED**: Test failed with assertion error
- ⚠ **ERROR**: Test encountered unexpected error

### Sample Output
```
============================================================
TEST RESULTS SUMMARY
============================================================
Data Files Existence.................... ✓ PASSED
Basic Data Quality...................... ✓ PASSED
Reports Generated....................... ✓ PASSED
System Configuration.................... ✓ PASSED
Data Integrity.......................... ✓ PASSED
Data Relationships...................... ✓ PASSED
Statistical Validity.................... ✓ PASSED
DataProcessor Functionality............. ✓ PASSED
Forecasting Engine Functionality........ ✓ PASSED
KPI Calculator Functionality............ ✓ PASSED
Report Generator Functionality.......... ✓ PASSED
Full Pipeline Integration............... ✓ PASSED
Data Flow Consistency................... ✓ PASSED
Performance Benchmarks.................. ✓ PASSED
Error Handling.......................... ✓ PASSED
Report Content Validation............... ✓ PASSED
Power BI Dataset Validation............. ✓ PASSED

============================================================
🎉 ALL TESTS PASSED! ✓
System is working correctly. (17/17 tests passed)
============================================================
```

## When to Run Which Tests

### Daily Development
```bash
python test_system.py --mode basic
```
Quick 30-second validation for basic functionality.

### Before Deployment
```bash
python test_system.py --mode all
```
Complete validation covering all system aspects.

### Data Issues Troubleshooting
```bash
python test_system.py --mode data
```
Comprehensive data validation to identify data quality issues.

### Performance Monitoring
```bash
python test_system.py --mode performance
```
Check system performance and identify bottlenecks.

### Integration Testing
```bash
python test_system.py --mode integration
```
Validate system components work together correctly.

## Troubleshooting

### Common Test Failures

#### Data File Missing
```
✗ FAILED: Required file missing: data/processed/processed_revenue.csv
```
**Solution**: Run the data processing pipeline first:
```bash
python main.py --mode data
```

#### Statistical Anomalies
```
✗ FAILED: Too many extreme revenue changes detected
```
**Solution**: Review your input data for outliers or run data cleaning.

#### Performance Issues
```
✗ FAILED: Data loading should be under 10 seconds, took 12.34s
```
**Solution**: Check system resources or optimize data files.

#### Component Import Errors
```
⚠ ERROR: DataProcessor import failed
```
**Solution**: Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Extending the Test Suite

To add new tests:

1. Add test function to `test_system.py`
2. Follow naming convention: `test_your_feature()`
3. Add to appropriate category in `run_tests_by_category()`
4. Include in `run_all_tests()` function

Example test function:
```python
def test_your_feature():
    """Test description"""
    print("\nTesting your feature...")
    
    # Test logic here
    assert condition, "Failure message"
    
    print("✓ Your feature works")
    print("Your feature tests passed!")
```

## Exit Codes

- **0**: All tests passed
- **1**: One or more tests failed

Use in scripts:
```bash
python test_system.py --mode all
if [ $? -eq 0 ]; then
    echo "All tests passed, proceeding with deployment"
else
    echo "Tests failed, stopping deployment"
    exit 1
fi
```