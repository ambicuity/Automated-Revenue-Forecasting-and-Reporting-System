# User Manual

## Overview

The Automated Revenue Forecasting and Reporting System provides business intelligence capabilities for revenue prediction, KPI tracking, and automated report generation. This manual covers system usage, features, and best practices.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Data      │    │  Data Processing │    │  Forecasting    │
│  - Revenue      │───▶│  - Cleaning      │───▶│  - Linear Trend │
│  - KPIs         │    │  - Validation    │    │  - Seasonal     │
│  - Customers    │    │  - Enrichment    │    │  - Ensemble     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Reports       │    │  KPI Calculator  │    │  Visualizations │
│  - PDF          │◀───│  - Performance   │───▶│  - Charts       │
│  - Excel        │    │  - Alerts        │    │  - Dashboards   │
│  - Power BI     │    │  - Trends        │    │  - Plots        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Features

### 1. Revenue Forecasting
- **Linear Trend Model**: Uses historical data to predict future revenue
- **Seasonal Decomposition**: Accounts for seasonal patterns in business
- **Ensemble Method**: Combines multiple models for improved accuracy
- **Confidence Intervals**: Provides uncertainty ranges for forecasts

### 2. KPI Tracking
- **Revenue Metrics**: Growth rates, trends, and performance indicators
- **Customer Metrics**: Retention, acquisition costs, lifetime value
- **Operational Metrics**: Marketing ROI, conversion rates, team efficiency
- **Performance Alerts**: Automated identification of issues requiring attention

### 3. Automated Reporting
- **PDF Reports**: Executive summaries and detailed analysis
- **Excel Workbooks**: Interactive data with charts and formatting
- **Visual Dashboards**: Management-ready charts and graphs
- **Power BI Integration**: Ready-to-import datasets

## Using the System

### Command Line Interface

The system provides a simple command-line interface:

```bash
python main.py [options]
```

**Options:**
- `--mode full`: Run complete pipeline (default)
- `--mode data`: Data processing only
- `--mode forecast`: Revenue forecasting only
- `--mode kpi`: KPI calculation only
- `--mode report`: Report generation only
- `--mode status`: Display system status
- `--skip-data-gen`: Skip sample data generation
- `--verbose`: Enable detailed logging

### Input Data Format

#### Revenue Data (revenue_data.csv)
| Column | Type | Description |
|--------|------|-------------|
| date | Date | Month-end date (YYYY-MM-DD) |
| business_unit | String | Business unit name |
| revenue | Numeric | Monthly revenue amount |
| customer_count | Integer | Number of customers |
| marketing_spend | Numeric | Marketing expenditure |
| sales_team_size | Integer | Sales team headcount |

#### KPI Data (kpi_data.csv)
| Column | Type | Description |
|--------|------|-------------|
| date | Date | Month-end date |
| customer_acquisition_cost | Numeric | Cost to acquire new customer |
| customer_lifetime_value | Numeric | Projected customer value |
| churn_rate | Numeric | Monthly customer churn (0-1) |
| retention_rate | Numeric | Customer retention rate (0-1) |
| net_promoter_score | Integer | NPS score (0-100) |

### Output Files

#### Reports Directory Structure
```
reports/
├── revenue_report_TIMESTAMP.pdf
├── revenue_report_TIMESTAMP.xlsx
├── executive_dashboard_TIMESTAMP.png
├── report_index_TIMESTAMP.md
├── revenue_forecasts.png
├── kpi_dashboard.png
└── powerbi_data/
    ├── revenue_data.csv
    ├── kpi_metrics.csv
    └── powerbi_connection.ps1
```

#### Key Reports
1. **PDF Report**: Executive summary with key metrics and insights
2. **Excel Workbook**: Interactive data with multiple worksheets
3. **Executive Dashboard**: Visual summary of performance
4. **Power BI Datasets**: Ready for import into Power BI

### Understanding the Results

#### Revenue Forecasts
- **Linear Forecast**: Trend-based prediction
- **Seasonal Forecast**: Pattern-based prediction accounting for seasonality
- **Ensemble Forecast**: Combined prediction (recommended)
- **Confidence Intervals**: 80% and 95% uncertainty ranges

#### KPI Interpretations
- **Revenue Growth YoY**: Year-over-year growth percentage
- **Customer Health Score**: Composite metric (0-1) of customer satisfaction
- **Revenue Quality Score**: Sustainability indicator based on retention
- **CLV/CAC Ratio**: Customer lifetime value to acquisition cost ratio

#### Performance Alerts
- **High Priority**: Revenue decline, high churn, low retention
- **Medium Priority**: Below-target performance, declining margins
- **Low Priority**: Minor deviations from expected performance

## Best Practices

### Data Quality
1. **Consistent Formatting**: Ensure dates are in YYYY-MM-DD format
2. **Complete Data**: Fill missing values appropriately
3. **Data Validation**: Review data for outliers and anomalies
4. **Regular Updates**: Update data monthly for accurate forecasts

### Forecasting Accuracy
1. **Historical Data**: Minimum 24 months for reliable forecasts
2. **Seasonality**: Account for business cycles and seasonal patterns
3. **External Factors**: Consider market conditions and business changes
4. **Model Validation**: Compare forecasts with actual results regularly

### Report Usage
1. **Executive Summaries**: Use PDF reports for leadership presentations
2. **Detailed Analysis**: Use Excel workbooks for deep-dive analysis
3. **Visual Communication**: Use dashboards for stakeholder updates
4. **Power BI Integration**: For ongoing monitoring and drill-down analysis

## Configuration Options

### Forecasting Parameters (config/settings.py)
```python
FORECAST_HORIZON_MONTHS = 12    # Forecast period
MIN_HISTORICAL_PERIODS = 24     # Minimum data requirement
CONFIDENCE_INTERVALS = [0.8, 0.95]  # Confidence levels
```

### KPI Thresholds
```python
REVENUE_GROWTH_TARGET = 0.15    # 15% annual growth target
PROFIT_MARGIN_TARGET = 0.20     # 20% profit margin target
CUSTOMER_RETENTION_TARGET = 0.90 # 90% retention target
```

### Report Customization
- Company name and branding
- Color schemes for charts
- Report titles and formatting
- Power BI workspace settings

## Troubleshooting

### Common Issues
1. **No forecasts generated**: Check minimum data requirements
2. **Poor forecast accuracy**: Review data quality and seasonality
3. **Missing reports**: Verify write permissions and disk space
4. **Performance alerts**: Review thresholds in configuration

### Data Issues
1. **Negative revenue**: Check data cleaning and validation rules
2. **Missing business units**: Verify data completeness
3. **Date parsing errors**: Ensure consistent date formatting
4. **Calculation errors**: Review derived metrics logic

## Support and Maintenance

### Regular Maintenance
- Update data monthly
- Review and adjust KPI thresholds quarterly
- Validate forecast accuracy monthly
- Archive old reports as needed

### Performance Monitoring
- Monitor system logs for errors
- Track forecast accuracy over time
- Review alert frequency and relevance
- Optimize data processing for large datasets