"""
Automated Revenue Forecasting and Reporting System
Main configuration module
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
POWERBI_DIR = PROJECT_ROOT / "powerbi"

# Data configuration
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_CURRENCY = "USD"

# Forecasting parameters
FORECAST_HORIZON_MONTHS = 12
CONFIDENCE_INTERVALS = [0.8, 0.95]
MIN_HISTORICAL_PERIODS = 24

# KPI thresholds
REVENUE_GROWTH_TARGET = 0.15  # 15% YoY growth target
PROFIT_MARGIN_TARGET = 0.20   # 20% profit margin target
CUSTOMER_RETENTION_TARGET = 0.90  # 90% retention rate

# Report configuration
REPORT_TITLE = "Revenue Forecasting & KPI Dashboard"
COMPANY_NAME = "Business Analytics Corp"
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"

# Power BI configuration
POWERBI_WORKSPACE = "Revenue Analytics"
POWERBI_DATASET = "revenue_forecasting"

# Email configuration (for automated reports)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Data validation rules
DATA_VALIDATION_RULES = {
    "revenue": {"min": 0, "required": True},
    "date": {"format": DEFAULT_DATE_FORMAT, "required": True},
    "business_unit": {"required": True, "type": "string"},
    "customer_count": {"min": 0, "type": "int"}
}

# Color scheme for reports
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e", 
    "success": "#2ca02c",
    "warning": "#d62728",
    "info": "#9467bd"
}