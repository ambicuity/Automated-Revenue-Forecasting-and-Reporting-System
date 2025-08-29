#!/usr/bin/env python3
"""
Quick Test Runner
Convenient script to run tests with common configurations
"""

import subprocess
import sys
import time
from pathlib import Path

def run_test(mode="all", show_help=False):
    """Run tests with specified mode"""
    
    if show_help:
        print("Available test modes:")
        print("  all         - Run all comprehensive tests (default)")
        print("  basic       - Run only basic tests (quick)")
        print("  data        - Run data validation tests")
        print("  components  - Run component functionality tests") 
        print("  integration - Run integration tests")
        print("  performance - Run performance tests")
        print("  output      - Run output validation tests")
        return
    
    script_dir = Path(__file__).parent
    test_script = script_dir / "test_system.py"
    
    print(f"🧪 Running {mode} tests...")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        if mode == "all":
            result = subprocess.run([sys.executable, str(test_script)], 
                                  cwd=script_dir, check=False)
        else:
            result = subprocess.run([sys.executable, str(test_script), "--mode", mode], 
                                  cwd=script_dir, check=False)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 50)
        
        if result.returncode == 0:
            print(f"✅ Tests completed successfully in {duration:.1f}s")
        else:
            print(f"❌ Tests failed after {duration:.1f}s")
            print("Check output above for details.")
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Quick test runner for Revenue Forecasting System')
    parser.add_argument('mode', nargs='?', default='all', 
                       choices=['all', 'basic', 'data', 'components', 'integration', 'performance', 'output'],
                       help='Test mode to run (default: all)')
    parser.add_argument('--help-modes', action='store_true',
                       help='Show available test modes')
    
    args = parser.parse_args()
    
    if args.help_modes:
        run_test(show_help=True)
        sys.exit(0)
    
    success = run_test(args.mode)
    sys.exit(0 if success else 1)