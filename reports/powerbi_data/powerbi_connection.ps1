
# Power BI Data Connection Script
# Use this script to connect Power BI to the generated datasets

$DataPath = "/home/runner/work/Automated-Revenue-Forecasting-and-Reporting-System/Automated-Revenue-Forecasting-and-Reporting-System/reports/powerbi_data"

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
        