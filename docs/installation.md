# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 1GB free space
- **Optional**: Microsoft Power BI Desktop for BI integration

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ambicuity/Automated-Revenue-Forecasting-and-Reporting-System.git
cd Automated-Revenue-Forecasting-and-Reporting-System
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv revenue_forecast_env

# Activate virtual environment
# On Windows:
revenue_forecast_env\Scripts\activate
# On macOS/Linux:
source revenue_forecast_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python main.py --mode status
```

This should display the system status and confirm all components are working.

## Quick Start

### Generate Sample Data and Run Full Pipeline

```bash
python main.py --mode full
```

This will:
1. Generate sample business data
2. Process and clean the data
3. Create revenue forecasts
4. Calculate KPIs
5. Generate comprehensive reports

### Run Individual Components

```bash
# Data processing only
python main.py --mode data

# Forecasting only
python main.py --mode forecast

# KPI calculation only
python main.py --mode kpi

# Report generation only
python main.py --mode report
```

## Output Files

After running the system, you'll find:

- **Reports**: `reports/` directory
  - PDF reports
  - Excel workbooks
  - Visual dashboards
  - Power BI datasets

- **Processed Data**: `data/processed/` directory
  - Cleaned datasets
  - Forecast results
  - KPI calculations

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Ensure all packages are installed with `pip install -r requirements.txt`

2. **Memory Issues**: For large datasets, increase available memory or process data in chunks

3. **Permission Errors**: Ensure write permissions for the `data/` and `reports/` directories

4. **Plot Display Issues**: Install additional backends if running on server: `pip install matplotlib --upgrade`

### Getting Help

- Check the logs in `system_log_YYYYMMDD.log`
- Review the generated `report_index_*.md` file for output summary
- Ensure all input data follows the expected format

## Configuration

Modify `config/settings.py` to customize:
- Forecasting parameters
- KPI thresholds
- Report formatting
- File paths

## Power BI Integration

1. Install Microsoft Power BI Desktop
2. Run the system to generate Power BI datasets
3. Import the CSV files from `reports/powerbi_data/` into Power BI
4. Use the provided connection script for automated data refresh