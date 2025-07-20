# Python CIMIS Client - Installation and Setup Guide

Complete installation and setup guide for the Python CIMIS Client library.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [API Key Setup](#api-key-setup)
- [Quick Start Verification](#quick-start-verification)
- [Development Setup](#development-setup)
- [Troubleshooting](#troubleshooting)
- [Configuration](#configuration)

---

## System Requirements

### Python Version
- **Python 3.8 or higher**
- Tested on Python 3.8, 3.9, 3.10, 3.11, and 3.12

### Operating Systems
- Windows 7/8/10/11
- macOS 10.14+
- Linux (all major distributions)

### Dependencies
- `requests >= 2.25.0` (automatically installed)

---

## Installation Methods

### Method 1: PyPI Installation (Recommended)

Install the latest stable version from PyPI:

```bash
pip install python-CIMIS
```

### Method 2: Development Installation

For the latest development version or to contribute:

```bash
# Clone the repository
git clone https://github.com/python-cimis/python-cimis-client.git
cd python-cimis-client

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Method 3: Virtual Environment (Recommended for Projects)

Create an isolated environment for your project:

#### Using venv (Python 3.3+)
```bash
# Create virtual environment
python -m venv cimis_env

# Activate (Windows)
cimis_env\Scripts\activate

# Activate (Linux/macOS)
source cimis_env/bin/activate

# Install the library
pip install python-CIMIS
```

#### Using conda
```bash
# Create conda environment
conda create -n cimis_env python=3.11

# Activate environment
conda activate cimis_env

# Install the library
pip install python-CIMIS
```

### Method 4: Requirements File

Add to your `requirements.txt`:

```text
python-CIMIS>=1.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

---

## API Key Setup

### Step 1: Register for CIMIS API Access

1. Visit the [CIMIS REST API page](https://et.water.ca.gov/Rest/Index)
2. Click "Register for a new account" or "Sign In" if you have an existing account
3. Fill out the registration form with:
   - Your name and contact information
   - Organization (if applicable)
   - Intended use of the API
4. Agree to the terms and conditions
5. Submit the registration

### Step 2: Generate Your API Key

1. After registration approval (usually immediate), log into your account
2. Navigate to the API Key section
3. Click "Generate New Key" or "Show API Key"
4. Copy your API key (it will look like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### Step 3: Secure Your API Key

#### Option 1: Environment Variable (Recommended)

**Windows:**
```bash
# Command Prompt
set CIMIS_API_KEY=your-actual-api-key-here

# PowerShell
$env:CIMIS_API_KEY="your-actual-api-key-here"

# Permanent (add to System Environment Variables)
# Control Panel > System > Advanced System Settings > Environment Variables
```

**Linux/macOS:**
```bash
# Temporary (current session)
export CIMIS_API_KEY="your-actual-api-key-here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export CIMIS_API_KEY="your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Option 2: .env File (For Development)

Create a `.env` file in your project root:

```bash
# .env file
CIMIS_API_KEY=your-actual-api-key-here
```

**Important:** Add `.env` to your `.gitignore` to prevent committing your API key!

```bash
# .gitignore
.env
*.env
```

Use with python-dotenv:
```bash
pip install python-dotenv
```

```python
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import os
from python_cimis import CimisClient

# Now you can use the environment variable
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))
```

#### Option 3: Configuration File

Create a config file (keep it secure):

```python
# config.py
CIMIS_API_KEY = "your-actual-api-key-here"
```

```python
# main.py
from config import CIMIS_API_KEY
from python_cimis import CimisClient

client = CimisClient(app_key=CIMIS_API_KEY)
```

---

## Quick Start Verification

### Test Your Installation

Create a test script to verify everything works:

```python
#!/usr/bin/env python3
"""
Test script to verify Python CIMIS Client installation and API key.
"""

import os
from datetime import date, timedelta
from python_cimis import CimisClient

def test_installation():
    """Test the installation and API key."""
    
    print("🔧 Testing Python CIMIS Client Installation")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('CIMIS_API_KEY')
    if not api_key:
        print("❌ ERROR: CIMIS_API_KEY environment variable not set")
        print("Please set your API key as an environment variable.")
        return False
    
    print(f"✅ API key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Initialize client
    try:
        client = CimisClient(app_key=api_key)
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ ERROR initializing client: {e}")
        return False
    
    # Test API connection with stations
    try:
        print("\n🏛️  Testing station data retrieval...")
        stations = client.get_stations()
        print(f"✅ Retrieved {len(stations)} stations")
    except Exception as e:
        print(f"❌ ERROR retrieving stations: {e}")
        return False
    
    # Test weather data retrieval
    try:
        print("\n🌤️  Testing weather data retrieval...")
        end_date = date.today() - timedelta(days=2)  # 2 days ago to ensure data availability
        start_date = end_date - timedelta(days=1)    # 1 day period
        
        weather_data = client.get_daily_data(
            targets=[2],  # Five Points station
            start_date=start_date,
            end_date=end_date
        )
        
        record_count = len(weather_data.get_all_records())
        print(f"✅ Retrieved {record_count} weather records")
        
        if record_count > 0:
            sample_record = weather_data.get_all_records()[0]
            print(f"   Sample: Station {sample_record.station}, Date {sample_record.date}")
            print(f"   Data items: {len(sample_record.data_values)}")
    
    except Exception as e:
        print(f"❌ ERROR retrieving weather data: {e}")
        return False
    
    # Test CSV export
    try:
        print("\n💾 Testing CSV export...")
        csv_file = client.export_to_csv(weather_data, filename="test_export.csv")
        print(f"✅ CSV exported to: {csv_file}")
    except Exception as e:
        print(f"❌ ERROR exporting CSV: {e}")
        return False
    
    print("\n🎉 All tests passed! Your installation is working correctly.")
    print("\n📚 Next steps:")
    print("   - Check out the examples/ directory for usage examples")
    print("   - Read the API_REFERENCE.md for complete documentation")
    print("   - Visit the CIMIS website for station maps and data information")
    
    return True

if __name__ == "__main__":
    success = test_installation()
    exit(0 if success else 1)
```

Save this as `test_installation.py` and run:

```bash
python test_installation.py
```

### Expected Output

If everything is working correctly, you should see:

```
🔧 Testing Python CIMIS Client Installation
==================================================
✅ API key found: 12345678...abcd
✅ Client initialized successfully

🏛️  Testing station data retrieval...
✅ Retrieved 280 stations

🌤️  Testing weather data retrieval...
✅ Retrieved 1 weather records
   Sample: Station 2, Date 2025-07-16
   Data items: 25

💾 Testing CSV export...
✅ CSV exported to: test_export.csv

🎉 All tests passed! Your installation is working correctly.

📚 Next steps:
   - Check out the examples/ directory for usage examples
   - Read the API_REFERENCE.md for complete documentation
   - Visit the CIMIS website for station maps and data information
```

---

## Development Setup

### For Contributors and Advanced Users

#### Clone and Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/python-cimis/python-cimis-client.git
cd python-cimis-client

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev,docs]"
```

#### Development Dependencies

The development installation includes:

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **sphinx** - Documentation generation

#### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=python_cimis

# Run specific test file
pytest tests/test_client.py

# Run tests with verbose output
pytest -v
```

#### Code Quality Checks

```bash
# Format code with black
black python_cimis/ tests/ examples/

# Lint with flake8
flake8 python_cimis/ tests/

# Type check with mypy
mypy python_cimis/
```

#### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs/
make html

# View documentation
# Open docs/_build/html/index.html in your browser
```

---

## Troubleshooting

### Common Installation Issues

#### Issue 1: Permission Denied

**Error:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Option 1: Use --user flag
pip install --user python-CIMIS

# Option 2: Use virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
pip install python-CIMIS
```

#### Issue 2: Python Version Incompatibility

**Error:**
```
ERROR: python-CIMIS requires Python '>=3.8' but the running Python is 3.7.x
```

**Solution:**
Install Python 3.8 or higher:
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **macOS:** Use Homebrew: `brew install python@3.11`
- **Linux:** Use your package manager: `sudo apt install python3.11`

#### Issue 3: SSL Certificate Issues

**Error:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
```bash
# Option 1: Update certificates (macOS)
/Applications/Python\ 3.11/Install\ Certificates.command

# Option 2: Upgrade pip and certificates
pip install --upgrade pip certifi

# Option 3: For corporate networks, check with IT for proxy settings
```

### Common API Issues

#### Issue 1: Invalid API Key

**Error:**
```
CimisAuthenticationError: Invalid API key
```

**Solutions:**
1. Verify your API key is correct (check for extra spaces)
2. Ensure your CIMIS account is active
3. Regenerate your API key on the CIMIS website
4. Check environment variable is set correctly

#### Issue 2: No Data Available

**Error:**
```
No data available for the requested period
```

**Solutions:**
1. Check date range is not in the future
2. Verify station numbers exist and are active
3. Some historical data may have gaps
4. Try a different date range or station

#### Issue 3: Timeout Errors

**Error:**
```
CimisConnectionError: Request timeout
```

**Solutions:**
```python
# Increase timeout
client = CimisClient(app_key="your-key", timeout=60)

# Reduce date range for large requests
# Split large requests into smaller chunks
```

### Getting Help

#### Documentation Resources
- **API Reference:** `docs/API_REFERENCE.md`
- **Examples:** `examples/` directory
- **CIMIS Official Docs:** https://et.water.ca.gov/Rest/Index

#### Community Support
- **GitHub Issues:** Report bugs and request features
- **Discussions:** Ask questions and share experiences
- **Stack Overflow:** Tag questions with `python-cimis`

#### Professional Support
For commercial support or custom development, contact the development team.

---

## Configuration

### Advanced Configuration Options

#### Custom API Endpoint

```python
# For testing or custom CIMIS deployments
client = CimisClient(
    app_key="your-key",
    base_url="https://custom-cimis-api.example.com/api"
)
```

#### Request Configuration

```python
# Custom timeout and retry settings
import requests
from python_cimis import CimisClient

session = requests.Session()
session.timeout = 60
session.verify = True  # SSL verification

# Note: Full session customization requires library modification
```

#### Logging Configuration

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('python_cimis')
logger.setLevel(logging.DEBUG)
```

### Production Configuration

#### Environment Variables

```bash
# Required
CIMIS_API_KEY=your-production-api-key

# Optional
CIMIS_TIMEOUT=30
CIMIS_BASE_URL=https://et.water.ca.gov/api
CIMIS_LOG_LEVEL=INFO
```

#### Configuration File

```python
# config.py
import os

class Config:
    CIMIS_API_KEY = os.getenv('CIMIS_API_KEY')
    CIMIS_TIMEOUT = int(os.getenv('CIMIS_TIMEOUT', 30))
    CIMIS_BASE_URL = os.getenv('CIMIS_BASE_URL', 'https://et.water.ca.gov/api')
    
    @classmethod
    def validate(cls):
        if not cls.CIMIS_API_KEY:
            raise ValueError("CIMIS_API_KEY environment variable is required")

# main.py
from config import Config
from python_cimis import CimisClient

Config.validate()
client = CimisClient(
    app_key=Config.CIMIS_API_KEY,
    timeout=Config.CIMIS_TIMEOUT
)
```

---

## Next Steps

After successful installation:

1. **📚 Read the Documentation**
   - API Reference: `docs/API_REFERENCE.md`
   - Usage Examples: `examples/` directory

2. **🧪 Run the Examples**
   ```bash
   python examples/basic_usage.py
   python examples/real_world_use_cases.py
   ```

3. **🔧 Integrate into Your Project**
   - Start with basic usage patterns
   - Add error handling and logging
   - Consider data caching for repeated requests

4. **🚀 Build Your Application**
   - Use the library in your agricultural or climate applications
   - Combine with visualization libraries (matplotlib, plotly)
   - Integrate with data analysis tools (pandas, numpy)

Happy coding! 🌾💧📊
