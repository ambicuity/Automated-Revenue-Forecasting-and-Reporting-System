"""
Main Orchestrator for Automated Revenue Forecasting and Reporting System
Runs the complete pipeline from data processing to report generation
"""

import logging
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from src.data_processor import DataProcessor
from src.forecasting_engine import RevenueForecaster
from src.kpi_calculator import KPICalculator
from src.report_generator import ReportGenerator
from config.settings import *

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'system_log_{datetime.now().strftime("%Y%m%d")}.log')
    ]
)
logger = logging.getLogger(__name__)

class SystemOrchestrator:
    """Orchestrates the complete revenue forecasting and reporting pipeline"""
    
    def __init__(self):
        logger.info("Initializing Revenue Forecasting and Reporting System...")
        
        # Initialize components
        self.data_processor = DataProcessor()
        self.forecaster = RevenueForecaster()
        self.kpi_calculator = KPICalculator()
        self.report_generator = ReportGenerator()
        
        # Create necessary directories
        self._setup_directories()
        
    def _setup_directories(self):
        """Ensure all necessary directories exist"""
        directories = [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, POWERBI_DIR]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info("Directory structure verified")
    
    def run_full_pipeline(self, skip_data_generation=False):
        """Run the complete analysis pipeline"""
        logger.info("="*60)
        logger.info("STARTING AUTOMATED REVENUE FORECASTING PIPELINE")
        logger.info("="*60)
        
        start_time = datetime.now()
        
        try:
            # Step 1: Generate sample data (if needed)
            if not skip_data_generation:
                logger.info("Step 1: Generating sample data...")
                self._generate_sample_data()
            else:
                logger.info("Step 1: Skipping data generation...")
            
            # Step 2: Data Processing
            logger.info("Step 2: Processing data...")
            self.data_processor.process_all_data()
            
            # Step 3: Revenue Forecasting
            logger.info("Step 3: Generating revenue forecasts...")
            self.forecaster.run_forecasting_pipeline()
            
            # Step 4: KPI Calculation
            logger.info("Step 4: Calculating KPIs...")
            self.kpi_calculator.run_kpi_pipeline()
            
            # Step 5: Report Generation
            logger.info("Step 5: Generating reports...")
            self.report_generator.generate_all_reports()
            
            # Pipeline completion
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info("="*60)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info(f"Total execution time: {duration}")
            logger.info(f"Reports available in: {REPORTS_DIR}")
            logger.info("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
    
    def _generate_sample_data(self):
        """Generate sample data if it doesn't exist"""
        import subprocess
        
        data_script = Path(__file__).parent / "data" / "generate_sample_data.py"
        if data_script.exists():
            subprocess.run([sys.executable, str(data_script)], check=True)
            logger.info("Sample data generated successfully")
        else:
            logger.warning("Sample data generation script not found")
    
    def run_data_processing_only(self):
        """Run only data processing"""
        logger.info("Running data processing pipeline only...")
        self.data_processor.process_all_data()
        logger.info("Data processing completed")
    
    def run_forecasting_only(self):
        """Run only forecasting"""
        logger.info("Running forecasting pipeline only...")
        self.forecaster.run_forecasting_pipeline()
        logger.info("Forecasting completed")
    
    def run_kpi_calculation_only(self):
        """Run only KPI calculation"""
        logger.info("Running KPI calculation only...")
        self.kpi_calculator.run_kpi_pipeline()
        logger.info("KPI calculation completed")
    
    def run_reporting_only(self):
        """Run only report generation"""
        logger.info("Running report generation only...")
        self.report_generator.generate_all_reports()
        logger.info("Report generation completed")
    
    def get_system_status(self):
        """Get current system status and data availability"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'directories': {},
            'data_files': {},
            'reports': {}
        }
        
        # Check directories
        directories = [
            ('raw_data', RAW_DATA_DIR),
            ('processed_data', PROCESSED_DATA_DIR),
            ('reports', REPORTS_DIR),
            ('powerbi', POWERBI_DIR)
        ]
        
        for name, path in directories:
            status['directories'][name] = {
                'exists': path.exists(),
                'path': str(path),
                'file_count': len(list(path.glob('*'))) if path.exists() else 0
            }
        
        # Check key data files
        key_files = [
            'revenue_data.csv',
            'kpi_data.csv',
            'processed_revenue.csv',
            'revenue_forecasts.csv',
            'monthly_kpis.csv'
        ]
        
        for filename in key_files:
            raw_path = RAW_DATA_DIR / filename
            processed_path = PROCESSED_DATA_DIR / filename
            
            status['data_files'][filename] = {
                'raw_exists': raw_path.exists(),
                'processed_exists': processed_path.exists(),
                'raw_size': raw_path.stat().st_size if raw_path.exists() else 0,
                'processed_size': processed_path.stat().st_size if processed_path.exists() else 0
            }
        
        # Check recent reports
        if REPORTS_DIR.exists():
            recent_reports = sorted(REPORTS_DIR.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)[:5]
            status['reports'] = {
                'total_reports': len(list(REPORTS_DIR.glob('*'))),
                'recent_reports': [{'name': r.name, 'size': r.stat().st_size} for r in recent_reports]
            }
        
        return status

def main():
    """Main execution function with command line interface"""
    parser = argparse.ArgumentParser(description='Automated Revenue Forecasting and Reporting System')
    parser.add_argument('--mode', choices=['full', 'data', 'forecast', 'kpi', 'report', 'status'], 
                       default='full', help='Pipeline mode to run')
    parser.add_argument('--skip-data-gen', action='store_true', 
                       help='Skip sample data generation')
    parser.add_argument('--verbose', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize orchestrator
    orchestrator = SystemOrchestrator()
    
    try:
        if args.mode == 'full':
            orchestrator.run_full_pipeline(skip_data_generation=args.skip_data_gen)
        elif args.mode == 'data':
            orchestrator.run_data_processing_only()
        elif args.mode == 'forecast':
            orchestrator.run_forecasting_only()
        elif args.mode == 'kpi':
            orchestrator.run_kpi_calculation_only()
        elif args.mode == 'report':
            orchestrator.run_reporting_only()
        elif args.mode == 'status':
            status = orchestrator.get_system_status()
            print("\n=== SYSTEM STATUS ===")
            print(f"Timestamp: {status['timestamp']}")
            print("\nDirectories:")
            for name, info in status['directories'].items():
                print(f"  {name}: {'✓' if info['exists'] else '✗'} ({info['file_count']} files)")
            print(f"\nRecent Reports: {status['reports'].get('total_reports', 0)}")
            
    except Exception as e:
        logger.error(f"System execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()