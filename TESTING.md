# Quick Testing Reference

## How to Run Tests

### Option 1: Comprehensive Test Suite (Recommended)
```bash
python test_system.py
```
**What it does**: Runs all 17 comprehensive tests (takes ~3-5 seconds)
**When to use**: Before deployment, after major changes, for complete system validation

### Option 2: Quick Basic Tests
```bash
python test_system.py --mode basic
```
**What it does**: Runs only 4 essential tests (takes ~1 second)
**When to use**: During development, quick health checks

### Option 3: Convenience Script
```bash
python run_tests.py basic
```
**What it does**: Same as option 2 but with timing and prettier output
**When to use**: When you want a nicer testing experience

### Option 4: Pytest Integration
```bash
python -m pytest test_pytest.py -v
```
**What it does**: Runs all tests through pytest framework
**When to use**: In CI/CD pipelines, automated testing

## Test Categories

| Command | Tests | Purpose |
|---------|-------|---------|
| `--mode data` | 3 tests | Data quality and integrity |
| `--mode components` | 4 tests | Individual module functionality |
| `--mode integration` | 2 tests | End-to-end pipeline validation |
| `--mode performance` | 2 tests | Speed and robustness |
| `--mode output` | 2 tests | Report quality validation |

## Exit Codes
- **0**: All tests passed ✅
- **1**: One or more tests failed ❌

## Common Usage Patterns

### Daily Development
```bash
python test_system.py --mode basic
```

### Before Git Commit
```bash
python run_tests.py all
```

### CI/CD Pipeline
```bash
python -m pytest test_pytest.py
if [ $? -eq 0 ]; then
    echo "Deploy ready"
else
    echo "Tests failed - blocking deployment"
    exit 1
fi
```

### Troubleshooting Data Issues
```bash
python test_system.py --mode data
```

### Performance Monitoring
```bash
python test_system.py --mode performance
```

## Sample Output
```
🎉 ALL TESTS PASSED! ✓
System is working correctly. (17/17 tests passed)
```

## Need Help?
- See [Testing Guide](docs/testing_guide.md) for detailed documentation
- Run `python test_system.py --help` for all options
- Run `python run_tests.py --help-modes` for convenience script options