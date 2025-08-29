# Automated Revenue Forecasting and Reporting System

An intelligent business intelligence system that provides automated revenue forecasting, KPI tracking, and comprehensive reporting for data-driven decision making.

## Overview

This system empowers senior business leaders with accurate revenue forecasts and key performance indicators to make informed strategic decisions. The solution combines advanced statistical modeling, automated data processing, and seamless Power BI integration for comprehensive business intelligence.

## Features

- **Revenue Forecasting**: Advanced statistical and machine learning models for accurate revenue prediction
- **KPI Dashboard**: Real-time tracking of key performance indicators
- **Automated Reporting**: Scheduled report generation and distribution
- **Power BI Integration**: Seamless integration with Microsoft Power BI
- **Data Quality Management**: Automated data validation and cleaning
- **Multi-format Export**: Support for Excel, PDF, and CSV report formats
- **Comprehensive Testing**: 17 automated tests covering all system components and data quality

## Testing

The system includes a comprehensive test suite with 17 tests covering:

- **Basic Tests**: Data files, quality, reports, and configuration
- **Data Validation**: Integrity, relationships, and statistical validity  
- **Component Tests**: Individual module functionality
- **Integration Tests**: End-to-end pipeline validation
- **Performance Tests**: Speed and resource usage benchmarks
- **Output Tests**: Report content and format validation

```bash
# Run all tests (recommended)
python test_system.py

# Run quick basic tests only
python test_system.py --mode basic

# Run specific test categories
python test_system.py --mode data
python test_system.py --mode components
python test_system.py --mode performance
```

See [Testing Guide](docs/testing_guide.md) for detailed testing documentation.

## Quick Start

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Complete System**
   ```bash
   python main.py --mode full
   ```

3. **Validate System is Working**
   ```bash
   python test_system.py
   ```
   This runs 17 comprehensive tests to ensure everything is working correctly.

4. **View Generated Reports**
   ```bash
   ls reports/
   ```

## Project Structure

```
├── data/                   # Data files and databases
├── src/                    # Source code
├── reports/               # Generated reports
├── powerbi/               # Power BI templates and configurations
├── tests/                 # Unit tests
└── docs/                  # Documentation
```

## Requirements

- Python 3.8+
- pandas, numpy, scikit-learn
- matplotlib, seaborn
- openpyxl, reportlab
- Power BI Desktop (for BI integration)

## Documentation

Detailed documentation is available in the `docs/` directory:
- [Installation Guide](docs/installation.md)
- [Testing Guide](docs/testing_guide.md)
- [User Manual](docs/user_manual.md)
- [API Reference](docs/api_reference.md)
- [Power BI Integration](docs/powerbi_integration.md)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.