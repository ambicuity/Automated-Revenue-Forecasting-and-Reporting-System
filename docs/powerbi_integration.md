# Power BI Integration Guide

This guide provides comprehensive instructions for integrating the Automated Revenue Forecasting and Reporting System with Microsoft Power BI.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Data Integration](#data-integration)
- [Dashboard Setup](#dashboard-setup)
- [Automated Data Refresh](#automated-data-refresh)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The system provides seamless integration with Power BI through:
- Automated dataset generation in Power BI-compatible formats
- Pre-configured connection scripts
- Ready-to-use data models
- Real-time dashboard templates

### Key Benefits

- **Automated Data Pipeline**: No manual data export/import needed
- **Real-time Updates**: Fresh data with each system run
- **Rich Visualizations**: Advanced charts and KPI dashboards
- **Interactive Reports**: Drill-down capabilities and filtering
- **Executive Dashboards**: High-level views for leadership

## Prerequisites

### System Requirements

1. **Microsoft Power BI Desktop** (latest version)
   - Download from [Microsoft Power BI](https://powerbi.microsoft.com/)
   - Business license recommended for full features

2. **System Setup**
   - Automated Revenue Forecasting System installed and working
   - Generated reports in `reports/powerbi_data/` directory

3. **Optional Requirements**
   - Power BI Pro license (for sharing and collaboration)
   - Power BI Gateway (for automated refresh from on-premise data)

### Verify Prerequisites

```bash
# Run the system to generate Power BI data
python main.py --mode full

# Check that Power BI data files are created
ls reports/powerbi_data/
```

Expected files:
- `revenue_data.csv`
- `kpi_metrics.csv`
- `unit_performance.csv`
- `revenue_forecasts.csv`
- `performance_alerts.csv`
- `powerbi_connection.ps1`

## Quick Start

### Step 1: Generate Data

Run the forecasting system to create fresh Power BI datasets:

```bash
python main.py --mode full
```

This creates all necessary CSV files in the `reports/powerbi_data/` directory.

### Step 2: Open Power BI Desktop

1. Launch Microsoft Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to your project's `reports/powerbi_data/` folder

### Step 3: Import Core Dataset

Start with the main revenue data:

1. Select `revenue_data.csv`
2. Click "Load"
3. Review the data preview
4. Click "Transform Data" if needed, or "Load" to proceed

### Step 4: Add Related Tables

Import additional datasets:

1. Click "Get Data" → "Text/CSV" again
2. Load each file:
   - `kpi_metrics.csv`
   - `unit_performance.csv` 
   - `revenue_forecasts.csv`
   - `performance_alerts.csv`

### Step 5: Create Relationships

Power BI should auto-detect relationships, but verify:

1. Go to "Model" view
2. Ensure relationships exist between tables (typically on Date fields)
3. Create missing relationships by dragging between date columns

### Step 6: Build Your First Dashboard

1. Go to "Report" view
2. Add a basic revenue chart:
   - Drag `Date` to X-axis
   - Drag `Total Revenue` to Y-axis
   - Select "Line Chart" visualization

## Data Integration

### Dataset Structure

The system generates five main datasets:

#### 1. Revenue Data (`revenue_data.csv`)
Primary business data with revenue metrics.

| Column | Description | Type |
|--------|-------------|------|
| Date | Month-end date | Date |
| Business Unit | Business unit name | Text |
| Revenue | Monthly revenue | Currency |
| Customer Count | Number of customers | Number |
| Marketing Spend | Marketing expenditure | Currency |
| Sales Team Size | Sales headcount | Number |

#### 2. KPI Metrics (`kpi_metrics.csv`)
Key performance indicators by month.

| Column | Description | Type |
|--------|-------------|------|
| Date | Month-end date | Date |
| Total Revenue | Monthly total revenue | Currency |
| Revenue Growth Mom | Month-over-month growth | Percentage |
| Revenue Growth Yoy | Year-over-year growth | Percentage |
| Avg Revenue Per Unit | Average revenue per unit | Currency |

#### 3. Unit Performance (`unit_performance.csv`)
Performance metrics by business unit.

| Column | Description | Type |
|--------|-------------|------|
| Business Unit | Unit name | Text |
| Unit Revenue | Unit total revenue | Currency |
| Unit Growth Rate | Unit growth rate | Percentage |
| Market Share | Unit market share | Percentage |
| Performance Score | Overall performance score | Number |

#### 4. Revenue Forecasts (`revenue_forecasts.csv`)
Forecasted revenue with confidence intervals.

| Column | Description | Type |
|--------|-------------|------|
| Date | Future month date | Date |
| Linear Forecast | Linear trend forecast | Currency |
| Seasonal Forecast | Seasonal adjusted forecast | Currency |
| Ensemble Forecast | Combined forecast | Currency |
| Confidence Lower | Lower confidence bound | Currency |
| Confidence Upper | Upper confidence bound | Currency |

#### 5. Performance Alerts (`performance_alerts.csv`)
Automated performance alerts and warnings.

| Column | Description | Type |
|--------|-------------|------|
| Date | Alert date | Date |
| Alert Type | Type of alert | Text |
| Description | Alert description | Text |
| Severity | Alert severity | Text |
| Business Unit | Affected unit | Text |
| Metric Value | Related metric value | Number |

### Data Relationships

Recommended relationship model:

```
Revenue Data (1) ←→ (*) KPI Metrics [Date]
Revenue Data (1) ←→ (*) Revenue Forecasts [Date]
Revenue Data (1) ←→ (*) Performance Alerts [Date, Business Unit]
Unit Performance (1) ←→ (*) Revenue Data [Business Unit]
```

### Data Types Configuration

Ensure correct data types in Power BI:

```powerquery
// Power Query M formula for date formatting
= Table.TransformColumnTypes(
    Source,
    {
        {"Date", type date},
        {"Revenue", Currency.Type},
        {"Revenue Growth Mom", Percentage.Type},
        {"Revenue Growth Yoy", Percentage.Type}
    }
)
```

## Dashboard Setup

### Executive Dashboard Template

Create a comprehensive executive dashboard with these visuals:

#### 1. Revenue Trend Line Chart
- **X-Axis**: Date (Date hierarchy)
- **Y-Axis**: Total Revenue
- **Legend**: Business Unit (optional)
- **Filters**: Date range, Business Unit

#### 2. Revenue Growth KPI Cards
Create KPI cards for:
- Monthly Growth Rate
- Yearly Growth Rate  
- Total Revenue (current month)

#### 3. Business Unit Performance Table
- **Columns**: Business Unit, Unit Revenue, Growth Rate, Market Share
- **Conditional Formatting**: Color-code growth rates

#### 4. Forecast vs Actual Chart
- **X-Axis**: Date
- **Y-Axis**: Revenue (multiple measures)
- **Lines**: Actual Revenue, Ensemble Forecast, Confidence Bounds

#### 5. Performance Alerts Table
- **Columns**: Date, Alert Type, Description, Severity
- **Filters**: Severity level, Date range

#### 6. Unit Breakdown Pie/Donut Chart
- **Values**: Unit Revenue
- **Legend**: Business Unit
- **Tooltips**: Market Share, Growth Rate

### Dashboard Layout Recommendations

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Executive Dashboard                           │
├──────────────────┬──────────────────┬──────────────────┬─────────────┤
│   Monthly Growth │   Yearly Growth  │  Current Revenue │   Forecast  │
│      KPI Card    │     KPI Card     │     KPI Card     │  KPI Card   │
├──────────────────┴──────────────────┴──────────────────┴─────────────┤
│                     Revenue Trend Line Chart                         │
├──────────────────────────────────────┬───────────────────────────────┤
│        Business Unit Performance     │     Unit Revenue Breakdown    │
│              Table                   │         Pie Chart             │
├──────────────────────────────────────┴───────────────────────────────┤
│                  Forecast vs Actual Chart                           │
├─────────────────────────────────────────────────────────────────────┤
│                     Performance Alerts                             │
└─────────────────────────────────────────────────────────────────────┘
```

### Color Scheme and Formatting

Use the system's color scheme for consistency:

```javascript
// Power BI Color Palette
Primary Blue:    #1f77b4
Secondary Orange: #ff7f0e  
Success Green:   #2ca02c
Warning Yellow:  #d62728
Info Purple:     #9467bd
```

Apply conditional formatting:
- **Green**: Positive growth rates
- **Red**: Negative growth rates  
- **Amber**: Performance alerts

## Automated Data Refresh

### Using PowerShell Script

The system generates a PowerShell script for automated data loading:

1. **Locate the script**: `reports/powerbi_data/powerbi_connection.ps1`
2. **Review the script content**:

```powershell
# Power BI Data Connection Script
$DataPath = "C:\path\to\your\project\reports\powerbi_data"

# Revenue Data
$RevenueData = Import-Csv "$DataPath/revenue_data.csv"

# KPI Metrics  
$KPIData = Import-Csv "$DataPath/kpi_metrics.csv"

# Unit Performance
$UnitData = Import-Csv "$DataPath/unit_performance.csv"

# Forecasts
$ForecastData = Import-Csv "$DataPath/revenue_forecasts.csv"

# Alerts
$AlertData = Import-Csv "$DataPath/performance_alerts.csv"

Write-Host "Data loaded successfully for Power BI import"
```

### Setting Up Scheduled Refresh

#### Option 1: Local Scheduled Refresh

1. **Create batch script** (`refresh_powerbi.bat`):

```batch
@echo off
cd /d "C:\path\to\your\project"
python main.py --mode full
powershell -ExecutionPolicy Bypass -File "reports\powerbi_data\powerbi_connection.ps1"
echo Power BI data refresh completed at %date% %time%
```

2. **Schedule with Windows Task Scheduler**:
   - Open Task Scheduler
   - Create Basic Task
   - Set trigger (daily, weekly, etc.)
   - Set action to run `refresh_powerbi.bat`

#### Option 2: Power BI Gateway Integration

For enterprise setups:

1. **Install Power BI Gateway** on your data source machine
2. **Configure data source** in Power BI Service
3. **Set up refresh schedule** in Power BI Service

### Python Integration Script

For advanced automation, use this Python script:

```python
# powerbi_refresh.py
import subprocess
import os
from pathlib import Path
import logging

def refresh_powerbi_data():
    """Run system and prepare Power BI data"""
    try:
        # Run the main system
        result = subprocess.run(['python', 'main.py', '--mode', 'full'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info("System run completed successfully")
            
            # Check if Power BI files exist
            powerbi_dir = Path('reports/powerbi_data')
            required_files = [
                'revenue_data.csv',
                'kpi_metrics.csv', 
                'unit_performance.csv',
                'revenue_forecasts.csv',
                'performance_alerts.csv'
            ]
            
            for file in required_files:
                if not (powerbi_dir / file).exists():
                    raise FileNotFoundError(f"Required file missing: {file}")
            
            logging.info("All Power BI data files generated successfully")
            return True
            
        else:
            logging.error(f"System run failed: {result.stderr}")
            return False
            
    except Exception as e:
        logging.error(f"Error refreshing Power BI data: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    refresh_powerbi_data()
```

## Advanced Configuration

### Custom Measures in Power BI

Add these DAX measures for advanced analytics:

#### Revenue Growth Rate
```dax
Revenue Growth Rate = 
VAR CurrentRevenue = SUM('Revenue Data'[Revenue])
VAR PreviousRevenue = 
    CALCULATE(
        SUM('Revenue Data'[Revenue]),
        DATEADD('Revenue Data'[Date], -1, MONTH)
    )
RETURN
IF(
    ISBLANK(PreviousRevenue) || PreviousRevenue = 0,
    BLANK(),
    (CurrentRevenue - PreviousRevenue) / PreviousRevenue
)
```

#### Forecast Accuracy
```dax
Forecast Accuracy = 
VAR ActualRevenue = SUM('Revenue Data'[Revenue])
VAR ForecastRevenue = SUM('Revenue Forecasts'[Ensemble Forecast])
RETURN
IF(
    ISBLANK(ActualRevenue) || ISBLANK(ForecastRevenue),
    BLANK(),
    1 - ABS(ActualRevenue - ForecastRevenue) / ActualRevenue
)
```

#### Performance Score
```dax
Performance Score = 
VAR RevenueScore = 
    IF(
        [Revenue Growth Rate] > 0.15, 100,
        IF([Revenue Growth Rate] > 0.10, 80, 
        IF([Revenue Growth Rate] > 0.05, 60, 40))
    )
VAR AlertCount = COUNTROWS('Performance Alerts')
VAR AlertPenalty = AlertCount * 10
RETURN
MAX(0, RevenueScore - AlertPenalty)
```

### Power BI Service Configuration

For Power BI Service (cloud) deployment:

1. **Publish Report**:
   - File → Publish → Publish to Power BI
   - Select workspace
   - Choose refresh settings

2. **Configure Gateway** (if using on-premise data):
   - Install Power BI Gateway
   - Configure data source connections
   - Set up refresh schedule

3. **Set Up Row-Level Security** (if needed):
   - Create security roles
   - Define DAX filters
   - Assign users to roles

### API Integration

For advanced users, integrate with Power BI REST API:

```python
# powerbi_api.py
import requests
import json
from pathlib import Path

class PowerBIAPI:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()
    
    def get_access_token(self):
        """Get access token for Power BI API"""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': 'https://analysis.windows.net/powerbi/api'
        }
        
        response = requests.post(url, data=data)
        return response.json()['access_token']
    
    def refresh_dataset(self, workspace_id, dataset_id):
        """Trigger dataset refresh"""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers)
        return response.status_code == 202
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Data source error" in Power BI
**Solutions:**
1. Check file paths in connection script
2. Ensure CSV files are not locked by other applications
3. Verify file permissions

#### Issue: Incorrect data types
**Solutions:**
1. Use Power Query to transform data types
2. Check date format consistency
3. Ensure numeric fields don't contain text

#### Issue: Missing relationships between tables
**Solutions:**
1. Verify common columns exist (typically Date fields)
2. Check data consistency between tables
3. Manually create relationships in Model view

#### Issue: Slow dashboard performance
**Solutions:**
1. Reduce data volume using filters
2. Use aggregated tables for large datasets
3. Optimize DAX measures
4. Consider DirectQuery for very large datasets

#### Issue: Refresh failures
**Solutions:**
1. Check file accessibility
2. Verify Python system runs successfully
3. Ensure all required files are generated
4. Check Windows Task Scheduler configuration

### Data Quality Checks

Before importing to Power BI, verify:

```python
# data_quality_check.py
import pandas as pd
from pathlib import Path

def check_powerbi_data_quality():
    """Verify Power BI data quality"""
    powerbi_dir = Path('reports/powerbi_data')
    
    checks = {
        'revenue_data.csv': {
            'required_columns': ['Date', 'Business Unit', 'Revenue'],
            'date_column': 'Date',
            'numeric_columns': ['Revenue', 'Customer Count']
        },
        'kpi_metrics.csv': {
            'required_columns': ['Date', 'Total Revenue'],
            'date_column': 'Date', 
            'numeric_columns': ['Total Revenue', 'Revenue Growth Mom']
        }
    }
    
    for filename, config in checks.items():
        filepath = powerbi_dir / filename
        if not filepath.exists():
            print(f"❌ Missing file: {filename}")
            continue
            
        df = pd.read_csv(filepath)
        
        # Check required columns
        missing_columns = set(config['required_columns']) - set(df.columns)
        if missing_columns:
            print(f"❌ {filename}: Missing columns {missing_columns}")
        else:
            print(f"✅ {filename}: All required columns present")
        
        # Check date column
        if config['date_column'] in df.columns:
            try:
                pd.to_datetime(df[config['date_column']])
                print(f"✅ {filename}: Date column format valid")
            except:
                print(f"❌ {filename}: Invalid date format")
        
        # Check for null values in key columns
        null_counts = df[config['required_columns']].isnull().sum()
        if null_counts.sum() > 0:
            print(f"⚠️  {filename}: Null values found: {null_counts.to_dict()}")
        else:
            print(f"✅ {filename}: No null values in key columns")

if __name__ == "__main__":
    check_powerbi_data_quality()
```

### Support and Resources

- **Power BI Community**: [https://community.powerbi.com/](https://community.powerbi.com/)
- **Microsoft Documentation**: [https://docs.microsoft.com/power-bi/](https://docs.microsoft.com/power-bi/)
- **DAX Reference**: [https://docs.microsoft.com/dax/](https://docs.microsoft.com/dax/)

### Getting Help

1. **Check Logs**: Review `system_log_YYYYMMDD.log` for system errors
2. **Verify Data Files**: Ensure all CSV files are generated correctly
3. **Test Connection**: Use the PowerShell script to verify data loading
4. **Community Support**: Post questions in Power BI community forums

## Best Practices

### Performance Optimization
- Use incremental refresh for large historical datasets
- Implement proper data modeling with star schema
- Minimize calculated columns, prefer measures
- Use DirectQuery for real-time data requirements

### Security Considerations
- Implement row-level security for sensitive data
- Use Power BI Gateway for secure on-premise connections
- Regular access reviews and permission audits
- Encrypt sensitive data connections

### Maintenance Schedule
- **Daily**: Automated data refresh
- **Weekly**: Dashboard performance review
- **Monthly**: User access audit
- **Quarterly**: Update Power BI templates and measures

By following this guide, you'll have a robust Power BI integration that provides real-time insights into your revenue forecasting and business performance.