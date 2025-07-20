# Python CIMIS Client

A comprehensive Python client library for the California Irrigation Management Information System (CIMIS) API. This library provides easy access to CIMIS weather station data, spatial data, and station information with built-in CSV export functionality.

[![PyPI version](https://badge.fury.io/py/python-CIMIS.svg)](https://badge.fury.io/py/python-CIMIS)
[![Python versions](https://img.shields.io/pypi/pyversions/python-CIMIS.svg)](https://pypi.org/project/python-CIMIS/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/python-cimis/badge/?version=latest)](https://python-cimis.readthedocs.io/en/latest/?badge=latest)

## 📚 Documentation

**📖 [Complete Documentation](https://python-cimis.readthedocs.io/)** - Detailed guides, API reference, and examples

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#-installation)
- [🔑 API Key Setup](#-api-key-setup)
- [📖 Usage Examples](#-usage-examples)
  - [Daily Weather Data](#daily-weather-data)
  - [Hourly Weather Data](#hourly-weather-data)
  - [Station Information](#station-information)
  - [CSV Export](#csv-export)
  - [Error Handling](#error-handling)
- [📊 Available Data Items](#-available-data-items)
- [🛠️ Advanced Usage](#️-advanced-usage)
- [🔧 Configuration](#-configuration)
- [📚 API Reference](#-api-reference)
- [🤝 Contributing](#-contributing)

## 🚀 Quick Start

```python
from python_cimis import CimisClient
from datetime import date

# Initialize the client with your API key
client = CimisClient(app_key="your-api-key-here")

# Get daily weather data for specific stations
weather_data = client.get_daily_data(
    targets=[2, 8, 127],  # Station numbers
    start_date="2023-01-01",
    end_date="2023-01-05"
)

# Export to CSV with all available columns
client.export_to_csv(weather_data, "weather_data.csv")

# Or get data and export in one step
weather_data = client.get_data_and_export_csv(
    targets=[2, 8, 127],
    start_date=date(2023, 1, 1),
    end_date=date(2023, 1, 5),
    filename="comprehensive_weather_data.csv"
)
```

## ✨ Features

- **🌐 Comprehensive API Coverage**: Access all CIMIS API endpoints including weather data, station information, and zip code data
- **📡 Multiple Data Sources**: Support for both Weather Station Network (WSN) and Spatial CIMIS System (SCS) data
- **🎯 Flexible Data Retrieval**: Get data by station numbers, zip codes, coordinates, or street addresses
- **📊 Built-in CSV Export**: Export all data with comprehensive column coverage by default
- **🐍 Easy to Use**: Simple, Pythonic interface with sensible defaults
- **⚠️ Error Handling**: Comprehensive exception handling with descriptive error messages
- **📝 Type Hints**: Full type hint support for better IDE integration
- **⚡ Performance**: Efficient data processing and export functionality

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install python-CIMIS
```

### From Source

```bash
git clone https://github.com/python-cimis/python-cimis-client.git
cd python-cimis-client
pip install -e .
```

## 🔑 API Key Setup

You need a CIMIS API key to use this library. 

### Get Your API Key

1. Visit the [CIMIS website](https://cimis.water.ca.gov/Default.aspx)
2. Register for a free account
3. Generate your API key from your account dashboard

### Set Up Your API Key

```python
# Option 1: Pass directly to client (not recommended for production)
client = CimisClient(app_key="your-api-key-here")

# Option 2: Use environment variable (recommended)
import os
os.environ['CIMIS_API_KEY'] = 'your-api-key-here'
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

# Option 3: Load from config file
import json
with open('config.json') as f:
    config = json.load(f)
client = CimisClient(app_key=config['cimis_api_key'])
```

## 📖 Usage Examples

### Daily Weather Data

#### 🏭 By Station Numbers

```python
from python_cimis import CimisClient
from datetime import date, timedelta

client = CimisClient(app_key="your-api-key-here")

# Get data for specific weather stations
weather_data = client.get_daily_data(
    targets=[2, 8, 127],  # Station numbers: Davis, UC Davis, Five Points
    start_date="2023-01-01",
    end_date="2023-01-31"
    # unit_of_measure defaults to "Metric"
)

print(f"Retrieved {len(weather_data.get_all_records())} records")
```

#### 📮 By Zip Codes

```python
# Get data for specific zip codes
weather_data = client.get_daily_data(
    targets=["95823", "94503", "93624"],
    start_date="2023-01-01",
    end_date="2023-01-31",
    prioritize_scs=True  # Prioritize Spatial CIMIS System data
)

# Export to CSV
client.export_to_csv(weather_data, "zip_code_weather.csv")
```

#### 🗺️ By Coordinates

```python
# Get data for specific coordinates (latitude, longitude)
weather_data = client.get_data(
    targets=[
        "lat=39.36,lng=-121.74",  # Near Yuba City
        "lat=38.22,lng=-122.82"   # Near Santa Rosa
    ],
    start_date="2023-01-01",
    end_date="2023-01-31",
    data_items=["day-asce-eto", "day-sol-rad-avg"]  # Only ETo and solar radiation
)
```

#### 🏠 By Addresses

```python
# Get data for specific addresses
weather_data = client.get_data(
    targets=[
        "addr-name=State Capitol,addr=1315 10th Street Sacramento, CA 95814",
        "addr-name=SF City Hall,addr=1 Dr Carlton B Goodlett Pl, San Francisco, CA 94102"
    ],
    start_date="2023-01-01",
    end_date="2023-01-31",
    data_items=["day-asce-eto", "day-sol-rad-avg"]
)
```

### Hourly Weather Data

```python
# Get hourly data (only available from WSN stations)
# Note: Hourly data requests should be for shorter periods due to data volume
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.strftime('%Y-%m-%d')
end_date = start_date  # Same day for hourly data

hourly_data = client.get_hourly_data(
    targets=[2, 8, 127],
    start_date=start_date,
    end_date=end_date
)

# Export hourly data (automatically uses clean column names)
client.export_to_csv(hourly_data, "hourly_weather.csv")
```

### Station Information

```python
# Get all available stations
all_stations = client.get_stations()
print(f"Total stations: {len(all_stations)}")

# Get specific station information
station = client.get_stations(station_number="2")
print(f"Station: {station[0].name} in {station[0].city}")

# Export station information to CSV
client.export_stations_to_csv(all_stations, "all_stations.csv")

# Get zip code information
station_zips = client.get_station_zip_codes()
spatial_zips = client.get_spatial_zip_codes()
```

### CSV Export

```python
# Basic export with all columns (default)
client.export_to_csv(weather_data, "complete_data.csv")

# Export with automatic filename generation
filename = client.export_to_csv(weather_data)
print(f"Data exported to: {filename}")

# Export daily and hourly data separately (recommended)
mixed_data = client.get_data(
    targets=[2, 8],
    start_date="2023-01-01",
    end_date="2023-01-02"
)
result = client.export_to_csv(mixed_data, "weather_data.csv")
# Creates: weather_data_daily.csv and weather_data_hourly.csv

# One-step data retrieval and export
client.get_data_and_export_csv(
    targets=[2, 8, 127],
    start_date="2023-01-01",
    end_date="2023-01-05",
    filename="january_weather.csv"
)
```

### Error Handling

```python
from python_cimis import (
    CimisClient, 
    CimisAPIError, 
    CimisAuthenticationError,
    CimisDataError,
    CimisConnectionError
)

client = CimisClient("your-api-key")

try:
    weather_data = client.get_daily_data(
        targets=[999999],  # Invalid station
        start_date="2023-01-01",
        end_date="2023-01-01"
    )
except CimisAuthenticationError:
    print("❌ Invalid API key or authentication failed")
except CimisConnectionError:
    print("❌ Network connection error")
except CimisDataError as e:
    print(f"❌ Data error: {e}")
except CimisAPIError as e:
    print(f"❌ API Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Custom Data Items

```python
# Specify custom data items for specific needs
temperature_only = [
    "day-air-tmp-avg", 
    "day-air-tmp-max", 
    "day-air-tmp-min"
]

eto_and_weather = [
    "day-asce-eto",
    "day-precip", 
    "day-sol-rad-avg",
    "day-wind-spd-avg",
    "day-rel-hum-avg"
]

# Get only temperature data
temp_data = client.get_daily_data(
    targets=[2, 8, 127],
    start_date="2023-01-01",
    end_date="2023-01-31",
    data_items=temperature_only
)

# Get ETo calculation inputs
eto_data = client.get_daily_data(
    targets=[2, 8, 127],
    start_date="2023-01-01",
    end_date="2023-01-31",
    data_items=eto_and_weather
)
```

## 📊 Available Data Items

### 🌅 Daily Data Items (WSN + SCS)

| Category | Data Items | Description |
|----------|------------|-------------|
| **🌡️ Temperature** | `day-air-tmp-avg`, `day-air-tmp-max`, `day-air-tmp-min` | Average, maximum, and minimum air temperature |
| **💧 Humidity** | `day-rel-hum-avg`, `day-rel-hum-max`, `day-rel-hum-min` | Relative humidity measurements |
| **🌿 Evapotranspiration** | `day-eto`, `day-asce-eto`, `day-asce-etr` | Reference evapotranspiration calculations |
| **☀️ Solar Radiation** | `day-sol-rad-avg`, `day-sol-rad-net` | Solar radiation measurements |
| **💨 Wind** | `day-wind-spd-avg`, `day-wind-run` | Wind speed and directional components |
| **🌍 Soil** | `day-soil-tmp-avg`, `day-soil-tmp-max`, `day-soil-tmp-min` | Soil temperature at various depths |
| **🌧️ Other** | `day-precip`, `day-dew-pnt`, `day-vap-pres-avg` | Precipitation, dew point, vapor pressure |

### ⏰ Hourly Data Items (WSN only)

| Category | Data Items | Description |
|----------|------------|-------------|
| **🌡️ Temperature** | `hly-air-tmp`, `hly-soil-tmp` | Hourly air and soil temperature |
| **💧 Humidity** | `hly-rel-hum` | Hourly relative humidity |
| **🌿 Evapotranspiration** | `hly-eto`, `hly-asce-eto`, `hly-asce-etr` | Hourly ET calculations |
| **☀️ Solar** | `hly-sol-rad`, `hly-net-rad` | Hourly solar radiation |
| **💨 Wind** | `hly-wind-spd`, `hly-wind-dir`, `hly-res-wind` | Hourly wind measurements |
| **🌧️ Other** | `hly-precip`, `hly-dew-pnt`, `hly-vap-pres` | Hourly precipitation and atmospheric data |

> **📝 Note**: When exporting hourly data to CSV, column names automatically have the "Hly" prefix removed for cleaner formatting (e.g., `HlyAirTmp` becomes `AirTmp_Value`).

## 🛠️ Advanced Usage

### Batch Processing Multiple Locations

```python
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def get_station_data(station_id):
    """Get data for a single station"""
    try:
        data = client.get_daily_data(
            targets=[station_id],
            start_date="2023-01-01",
            end_date="2023-01-31"
        )
        return station_id, data
    except Exception as e:
        print(f"Error for station {station_id}: {e}")
        return station_id, None

# Process multiple stations in parallel
stations = [2, 8, 127, 54, 6]
results = {}

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(get_station_data, station) for station in stations]
    for future in futures:
        station_id, data = future.result()
        if data:
            results[station_id] = data
```

### Data Analysis Integration

```python
import pandas as pd
import matplotlib.pyplot as plt

# Get weather data
weather_data = client.get_daily_data(
    targets=[2],  # Davis station
    start_date="2023-01-01",
    end_date="2023-12-31",
    data_items=["day-air-tmp-avg", "day-asce-eto", "day-precip"]
)

# Export to CSV
csv_file = client.export_to_csv(weather_data, "davis_2023.csv")

# Load into pandas for analysis
df = pd.read_csv(csv_file)
df['Date'] = pd.to_datetime(df['Date'])

# Basic analysis
print(f"Average temperature: {df['DayAirTmpAvg_Value'].mean():.1f}°C")
print(f"Total precipitation: {df['DayPrecip_Value'].sum():.1f}mm")
print(f"Total ETo: {df['DayAsceEto_Value'].sum():.1f}mm")

# Simple visualization
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['DayAirTmpAvg_Value'])
plt.title('Daily Average Temperature - Davis Station 2023')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Custom Data Validation

```python
def validate_weather_data(weather_data):
    """Validate weather data quality"""
    records = weather_data.get_all_records()
    
    issues = []
    for record in records:
        # Check for missing critical data
        if 'DayAsceEto' in record.data_values:
            eto_value = record.data_values['DayAsceEto'].value
            qc_flag = record.data_values['DayAsceEto'].qc
            
            if not eto_value or eto_value == '':
                issues.append(f"Missing ETo data for {record.date}")
            elif qc_flag and qc_flag.strip() not in [' ', '']:
                issues.append(f"Quality issue for ETo on {record.date}: {qc_flag}")
    
    return issues

# Use validation
weather_data = client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-31")
issues = validate_weather_data(weather_data)
if issues:
    print("Data quality issues found:")
    for issue in issues[:5]:  # Show first 5 issues
        print(f"  - {issue}")
```

## 🔧 Configuration

### Environment Variables

```bash
# Set your API key as an environment variable (recommended)
export CIMIS_API_KEY="your-api-key-here"

# Optional: Set default timeout
export CIMIS_TIMEOUT="30"
```

### Client Configuration

```python
# Configure client with custom settings
client = CimisClient(
    app_key="your-api-key",
    timeout=60,  # Custom timeout in seconds
    base_url="https://et.water.ca.gov/api"  # Custom base URL if needed
)

# Check client configuration
print(f"API Key configured: {'Yes' if client.app_key else 'No'}")
print(f"Timeout: {client.timeout} seconds")
```

## 📚 API Reference

### CimisClient Class

```python
from python_cimis import CimisClient

client = CimisClient(
    app_key: str,           # Your CIMIS API key (required)
    timeout: int = 30,      # Request timeout in seconds
    base_url: str = None    # Custom API base URL (optional)
)
```

### Main Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `get_daily_data()` | Get daily weather data | `WeatherData` object |
| `get_hourly_data()` | Get hourly weather data | `WeatherData` object |
| `get_data()` | Get weather data (flexible) | `WeatherData` object |
| `get_stations()` | Get station information | `List[Station]` |
| `get_station_zip_codes()` | Get WSN zip codes | `List[ZipCode]` |
| `get_spatial_zip_codes()` | Get SCS zip codes | `List[SpatialZipCode]` |
| `export_to_csv()` | Export data to CSV | `str` (filename) |
| `export_stations_to_csv()` | Export stations to CSV | `str` (filename) |
| `get_data_and_export_csv()` | Get data and export in one step | `Tuple[WeatherData, str]` |

### Method Parameters

#### get_daily_data() / get_hourly_data()

```python
client.get_daily_data(
    targets: Union[str, List[str]],           # Station numbers, zip codes, coordinates
    start_date: Union[str, date, datetime],   # Start date (YYYY-MM-DD)
    end_date: Union[str, date, datetime],     # End date (YYYY-MM-DD)
    data_items: Optional[List[str]] = None,   # Specific data items (optional)
    unit_of_measure: str = 'Metric',          # 'Metric' or 'English'
    csv: bool = False,                        # Export to CSV immediately
    filename: Optional[str] = None            # CSV filename (if csv=True)
)
```

## 🧩 Data Models

### WeatherData
Container for weather data responses with methods:
- `get_all_records()`: Get all weather records
- `get_daily_records()`: Get only daily records  
- `get_hourly_records()`: Get only hourly records

### WeatherRecord
Individual weather data record with attributes:
- `date`: Record date (YYYY-MM-DD)
- `station`: Station identifier
- `data_values`: Dictionary of data measurements
- `scope`: 'daily' or 'hourly'

### Station
Weather station information with attributes:
- `station_nbr`: Station number
- `name`: Station name
- `city`: City location
- `latitude`, `longitude`: Coordinates
- `elevation`: Station elevation

## 💡 Best Practices

### 1. API Key Security
```python
# ✅ Good: Use environment variables
import os
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

# ❌ Avoid: Hardcoding API keys
client = CimisClient(app_key="your-key-here")  # Don't do this!
```

### 2. Date Range Management
```python
# ✅ Good: Reasonable date ranges
from datetime import date, timedelta

# For daily data: up to 1 year
start_date = date.today() - timedelta(days=365)
end_date = date.today() - timedelta(days=1)

# For hourly data: keep it short (1-7 days)
start_date = date.today() - timedelta(days=1)
end_date = date.today() - timedelta(days=1)
```

### 3. Error Handling
```python
# ✅ Good: Comprehensive error handling
from python_cimis import CimisClient, CimisAPIError

try:
    weather_data = client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-31")
except CimisAPIError as e:
    print(f"API Error: {e}")
    # Handle error appropriately
```

### 4. Performance Optimization
```python
# ✅ Good: Request specific data items when possible
data_items = ["day-asce-eto", "day-precip", "day-air-tmp-avg"]
weather_data = client.get_daily_data(
    targets=[2, 8, 127],
    start_date="2023-01-01",
    end_date="2023-01-31",
    data_items=data_items  # Reduces response size
)
```

## Requirements

- **Python**: 3.8+
- **Dependencies**: 
  - requests >= 2.25.0

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Development Setup
```bash
# Clone the repository
git clone https://github.com/python-cimis/python-cimis-client.git
cd python-cimis-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black python_cimis/
flake8 python_cimis/
mypy python_cimis/
```

### Contributing Guidelines
1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✨ Make your changes
4. ✅ Add tests for new functionality
5. 🧪 Run the test suite (`pytest`)
6. 📝 Update documentation if needed
7. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
8. 📤 Push to the branch (`git push origin feature/amazing-feature`)
9. 🔄 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors

**Authors:**
- Mahipal Reddy Ramireddy
- M. A. Andrade

**Maintainer:**
- Precision Irrigation Management Lab (PRIMA)

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⚠️ Disclaimer

This library is not affiliated with the California Department of Water Resources or the CIMIS program. It is an independent client library for accessing the public CIMIS API.

## 🔗 Useful Links

- **� [Python CIMIS Documentation](https://python-cimis.readthedocs.io/)** - Complete library documentation
- **�📋 [CIMIS Website](https://cimis.water.ca.gov/)** - Official CIMIS portal
- **📖 [CIMIS API Documentation](https://et.water.ca.gov/Rest/Index)** - Official API docs
- **🏛️ [California Department of Water Resources](https://water.ca.gov/)** - DWR website
- **🐛 [Report Issues](https://github.com/Precision-Irrigation-Management-lab/Python-CIMIS/issues)** - Bug reports and feature requests
- **📦 [PyPI Package](https://pypi.org/project/python-CIMIS/)** - Package on PyPI

---

**Made with ❤️ for the California agricultural and research community**
