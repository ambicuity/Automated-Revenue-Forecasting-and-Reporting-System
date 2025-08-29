# API Reference

This document provides comprehensive API documentation for the Automated Revenue Forecasting and Reporting System.

## Table of Contents

- [System Orchestrator](#system-orchestrator)
- [Data Processing](#data-processing)
- [Forecasting Engine](#forecasting-engine)
- [KPI Calculator](#kpi-calculator)
- [Report Generator](#report-generator)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

## System Orchestrator

### SystemOrchestrator

Main orchestration class that coordinates all system components.

```python
from main import SystemOrchestrator

orchestrator = SystemOrchestrator()
```

#### Methods

##### `run_full_pipeline()`
Executes the complete revenue forecasting and reporting pipeline.

**Returns:** `None`

**Example:**
```python
orchestrator.run_full_pipeline()
```

##### `run_data_processing()`
Runs only the data processing component.

**Returns:** `None`

##### `run_forecasting()`
Runs only the forecasting component.

**Returns:** `None`

##### `run_kpi_calculation()`
Runs only the KPI calculation component.

**Returns:** `None`

##### `run_report_generation()`
Runs only the report generation component.

**Returns:** `None`

##### `get_system_status()`
Returns current system status and health check.

**Returns:** `dict` - System status information

## Data Processing

### DataProcessor

Handles data loading, validation, cleaning, and preprocessing.

```python
from src.data_processor import DataProcessor

processor = DataProcessor()
```

#### Methods

##### `load_revenue_data()`
Loads and validates revenue data from CSV files.

**Returns:** `pandas.DataFrame` - Processed revenue data

**Raises:** 
- `FileNotFoundError` - If data files are missing
- `ValueError` - If data validation fails

**Example:**
```python
revenue_df = processor.load_revenue_data()
print(revenue_df.head())
```

##### `load_kpi_data()`
Loads and validates KPI data from CSV files.

**Returns:** `pandas.DataFrame` - Processed KPI data

##### `calculate_derived_metrics(df)`
Calculates additional metrics from base data.

**Parameters:**
- `df` (pandas.DataFrame): Input dataframe

**Returns:** `pandas.DataFrame` - DataFrame with derived metrics

**Example:**
```python
enhanced_df = processor.calculate_derived_metrics(revenue_df)
```

##### `aggregate_data(df)`
Aggregates data by business unit and time period.

**Parameters:**
- `df` (pandas.DataFrame): Input dataframe

**Returns:** `pandas.DataFrame` - Aggregated data

##### `save_processed_data(df, filename)`
Saves processed data to file.

**Parameters:**
- `df` (pandas.DataFrame): Data to save
- `filename` (str): Output filename

**Returns:** `None`

##### `process_all_data()`
Runs the complete data processing pipeline.

**Returns:** `None`

**Example:**
```python
processor.process_all_data()
```

## Forecasting Engine

### RevenueForecaster

Advanced forecasting engine with multiple algorithms.

```python
from src.forecasting_engine import RevenueForecaster

forecaster = RevenueForecaster()
```

#### Methods

##### `load_processed_data()`
Loads processed data for forecasting.

**Returns:** `pandas.DataFrame` - Processed data ready for forecasting

##### `prepare_features(df)`
Prepares features for machine learning models.

**Parameters:**
- `df` (pandas.DataFrame): Input data

**Returns:** `tuple` - (features, target) arrays

##### `linear_trend_forecast(df)`
Generates linear trend-based forecasts.

**Parameters:**
- `df` (pandas.DataFrame): Historical data

**Returns:** `dict` - Forecast results with confidence intervals

**Example:**
```python
linear_results = forecaster.linear_trend_forecast(data_df)
print(f"Next month forecast: ${linear_results['forecast'][0]:,.2f}")
```

##### `seasonal_decomposition_forecast(df)`
Generates seasonal decomposition-based forecasts.

**Parameters:**
- `df` (pandas.DataFrame): Historical data

**Returns:** `dict` - Seasonal forecast results

##### `generate_confidence_intervals(forecast, historical_errors)`
Calculates confidence intervals for forecasts.

**Parameters:**
- `forecast` (numpy.array): Forecast values
- `historical_errors` (numpy.array): Historical forecast errors

**Returns:** `dict` - Confidence interval bounds

##### `create_forecast_summary(linear_results, seasonal_results)`
Creates ensemble forecast summary.

**Parameters:**
- `linear_results` (dict): Linear forecast results
- `seasonal_results` (dict): Seasonal forecast results

**Returns:** `pandas.DataFrame` - Ensemble forecast summary

##### `save_forecasts(summary_df)`
Saves forecast results to file.

**Parameters:**
- `summary_df` (pandas.DataFrame): Forecast summary

**Returns:** `None`

##### `create_forecast_plots(df, forecasts_df)`
Creates forecast visualization plots.

**Parameters:**
- `df` (pandas.DataFrame): Historical data
- `forecasts_df` (pandas.DataFrame): Forecast data

**Returns:** `None`

##### `run_forecasting_pipeline()`
Executes complete forecasting pipeline.

**Returns:** `None`

**Example:**
```python
forecaster.run_forecasting_pipeline()
```

## KPI Calculator

### KPICalculator

Calculates key performance indicators and business metrics.

```python
from src.kpi_calculator import KPICalculator

kpi_calc = KPICalculator()
```

#### Methods

##### `load_data()`
Loads processed revenue and KPI data.

**Returns:** `tuple` - (revenue_df, kpi_df)

##### `calculate_revenue_kpis(revenue_df)`
Calculates revenue-based KPIs.

**Parameters:**
- `revenue_df` (pandas.DataFrame): Revenue data

**Returns:** `pandas.DataFrame` - Revenue KPIs by month

**Calculated KPIs:**
- Total Revenue
- Revenue Growth (MoM)
- Revenue Growth (YoY)
- Average Revenue per Unit
- Revenue Trend

**Example:**
```python
revenue_kpis = kpi_calc.calculate_revenue_kpis(revenue_df)
print(revenue_kpis[['total_revenue', 'revenue_growth_mom']].tail())
```

##### `calculate_business_unit_kpis(revenue_df)`
Calculates KPIs by business unit.

**Parameters:**
- `revenue_df` (pandas.DataFrame): Revenue data

**Returns:** `pandas.DataFrame` - KPIs by business unit

**Calculated KPIs:**
- Unit Revenue
- Unit Growth Rate
- Market Share
- Performance Score

##### `calculate_advanced_kpis(revenue_df, kpi_df)`
Calculates advanced business metrics.

**Parameters:**
- `revenue_df` (pandas.DataFrame): Revenue data
- `kpi_df` (pandas.DataFrame): Base KPI data

**Returns:** `pandas.DataFrame` - Advanced KPIs

**Calculated KPIs:**
- Customer Lifetime Value (CLV)
- Customer Acquisition Cost Ratio
- Revenue per Employee
- Profit Margin Estimates

##### `detect_performance_alerts(monthly_kpis, unit_kpis, advanced_kpis)`
Detects performance issues and generates alerts.

**Parameters:**
- `monthly_kpis` (pandas.DataFrame): Monthly KPI data
- `unit_kpis` (pandas.DataFrame): Unit KPI data
- `advanced_kpis` (pandas.DataFrame): Advanced KPI data

**Returns:** `pandas.DataFrame` - Performance alerts

**Alert Types:**
- Revenue decline
- Growth rate below target
- Performance anomalies
- Threshold violations

##### `save_kpi_data(monthly_kpis, unit_kpis, advanced_kpis, alerts)`
Saves all KPI calculations to files.

**Parameters:**
- `monthly_kpis` (pandas.DataFrame): Monthly KPIs
- `unit_kpis` (pandas.DataFrame): Unit KPIs
- `advanced_kpis` (pandas.DataFrame): Advanced KPIs
- `alerts` (pandas.DataFrame): Performance alerts

**Returns:** `None`

##### `process_all_kpis()`
Runs complete KPI calculation pipeline.

**Returns:** `None`

**Example:**
```python
kpi_calc.process_all_kpis()
```

## Report Generator

### ReportGenerator

Generates comprehensive business reports in multiple formats.

```python
from src.report_generator import ReportGenerator

generator = ReportGenerator()
```

#### Methods

##### `load_processed_data()`
Loads all processed data for reporting.

**Returns:** `dict` - Dictionary containing all data types

##### `create_executive_summary(data)`
Creates executive summary from data.

**Parameters:**
- `data` (dict): Processed data dictionary

**Returns:** `dict` - Executive summary metrics

##### `generate_pdf_report(data, summary)`
Generates comprehensive PDF report.

**Parameters:**
- `data` (dict): Processed data
- `summary` (dict): Executive summary

**Returns:** `None`

**Output:** PDF report saved to reports directory

##### `generate_excel_report(data, summary)`
Generates interactive Excel workbook.

**Parameters:**
- `data` (dict): Processed data
- `summary` (dict): Executive summary

**Returns:** `None`

**Features:**
- Multiple worksheets
- Charts and visualizations
- Formatted tables
- Executive dashboard

##### `create_powerbi_dataset(data)`
Creates Power BI compatible datasets.

**Parameters:**
- `data` (dict): Processed data

**Returns:** `None`

**Outputs:**
- CSV files for Power BI import
- PowerShell connection script
- Data mapping documentation

**Example:**
```python
generator.create_powerbi_dataset(processed_data)
```

##### `create_summary_dashboard(data, summary)`
Creates visual summary dashboard.

**Parameters:**
- `data` (dict): Processed data
- `summary` (dict): Executive summary

**Returns:** `None`

**Output:** PNG dashboard image

##### `generate_all_reports()`
Generates all report types.

**Returns:** `None`

**Example:**
```python
generator.generate_all_reports()
```

## Configuration

### Settings Module

Configuration parameters are defined in `config/settings.py`.

#### Key Configuration Variables

##### Paths
```python
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
```

##### Forecasting Parameters
```python
FORECAST_HORIZON_MONTHS = 12
CONFIDENCE_INTERVALS = [0.8, 0.95]
MIN_HISTORICAL_PERIODS = 24
```

##### KPI Thresholds
```python
REVENUE_GROWTH_TARGET = 0.15  # 15% YoY growth target
PROFIT_MARGIN_TARGET = 0.20   # 20% profit margin target
CUSTOMER_RETENTION_TARGET = 0.90  # 90% retention rate
```

##### Power BI Configuration
```python
POWERBI_WORKSPACE = "Revenue Analytics"
POWERBI_DATASET = "revenue_forecasting"
```

## Error Handling

### Common Exceptions

#### Data Processing Errors
- `FileNotFoundError`: Data files missing
- `ValueError`: Data validation failures
- `pandas.errors.EmptyDataError`: Empty datasets

#### Forecasting Errors
- `ValueError`: Insufficient historical data
- `RuntimeError`: Model convergence issues
- `IndexError`: Date range errors

#### Reporting Errors
- `PermissionError`: File write permissions
- `IOError`: Disk space or file system errors

### Error Handling Patterns

```python
try:
    processor = DataProcessor()
    processor.process_all_data()
except FileNotFoundError as e:
    logger.error(f"Data file not found: {e}")
except ValueError as e:
    logger.error(f"Data validation error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Usage Examples

### Basic Usage

```python
from main import SystemOrchestrator

# Initialize system
orchestrator = SystemOrchestrator()

# Run complete pipeline
orchestrator.run_full_pipeline()
```

### Component-wise Usage

```python
from src.data_processor import DataProcessor
from src.forecasting_engine import RevenueForecaster
from src.kpi_calculator import KPICalculator
from src.report_generator import ReportGenerator

# Data processing
processor = DataProcessor()
processor.process_all_data()

# Forecasting
forecaster = RevenueForecaster()
forecaster.run_forecasting_pipeline()

# KPI calculation
kpi_calc = KPICalculator()
kpi_calc.process_all_kpis()

# Report generation
generator = ReportGenerator()
generator.generate_all_reports()
```

### Custom Forecasting

```python
from src.forecasting_engine import RevenueForecaster

forecaster = RevenueForecaster()
data_df = forecaster.load_processed_data()

# Generate custom forecast
linear_results = forecaster.linear_trend_forecast(data_df)
seasonal_results = forecaster.seasonal_decomposition_forecast(data_df)

# Create ensemble forecast
forecast_summary = forecaster.create_forecast_summary(
    linear_results, seasonal_results
)

print(f"12-month revenue forecast: ${forecast_summary['ensemble_forecast'].sum():,.2f}")
```

### Advanced KPI Analysis

```python
from src.kpi_calculator import KPICalculator

kpi_calc = KPICalculator()
revenue_df, kpi_df = kpi_calc.load_data()

# Calculate specific KPIs
revenue_kpis = kpi_calc.calculate_revenue_kpis(revenue_df)
unit_kpis = kpi_calc.calculate_business_unit_kpis(revenue_df)
advanced_kpis = kpi_calc.calculate_advanced_kpis(revenue_df, kpi_df)

# Check for alerts
alerts = kpi_calc.detect_performance_alerts(revenue_kpis, unit_kpis, advanced_kpis)

if not alerts.empty:
    print("Performance Alerts:")
    for _, alert in alerts.iterrows():
        print(f"- {alert['alert_type']}: {alert['description']}")
```

### Power BI Integration

```python
from src.report_generator import ReportGenerator

generator = ReportGenerator()
data = generator.load_processed_data()

# Create Power BI datasets
generator.create_powerbi_dataset(data)

print("Power BI datasets created in reports/powerbi_data/")
print("Run powerbi_connection.ps1 to import data into Power BI")
```

## Command Line Interface

The system provides a command-line interface through `main.py`:

```bash
# Full pipeline
python main.py --mode full

# Individual components
python main.py --mode data      # Data processing only
python main.py --mode forecast  # Forecasting only
python main.py --mode kpi       # KPI calculation only
python main.py --mode report    # Report generation only

# System status
python main.py --mode status
```

## Data Formats

### Input Data Format

#### Revenue Data (revenue_data.csv)
```csv
date,business_unit,revenue,customer_count,marketing_spend,sales_team_size
2023-01-31,Product A,125000,1250,15000,5
2023-01-31,Product B,89000,890,12000,4
```

#### KPI Data (kpi_data.csv)
```csv
date,customer_acquisition_cost,customer_lifetime_value,churn_rate,retention_rate,net_promoter_score
2023-01-31,150.50,2500.00,0.05,0.95,75
```

### Output Data Format

#### Forecast Results
```csv
date,linear_forecast,seasonal_forecast,ensemble_forecast,confidence_lower,confidence_upper
2024-01-31,125000.00,123500.00,124250.00,118000.00,130500.00
```

#### KPI Results
```csv
date,total_revenue,revenue_growth_mom,revenue_growth_yoy,avg_revenue_per_unit
2023-12-31,1891610.00,0.18,0.22,1245.50
```

## Logging

The system uses Python's logging module with configurable levels:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Process completed successfully")
```

Log files are saved as `system_log_YYYYMMDD.log`.

## Performance Considerations

- **Memory Usage**: Large datasets are processed in chunks
- **Processing Time**: Forecasting can take 2-5 minutes for large datasets
- **File I/O**: All outputs are buffered for efficiency
- **Parallel Processing**: Components can be run independently

## Version Compatibility

- **Python**: 3.8+ required
- **Pandas**: 2.0+ recommended
- **Scikit-learn**: 1.3+ required
- **Power BI**: Desktop version supported