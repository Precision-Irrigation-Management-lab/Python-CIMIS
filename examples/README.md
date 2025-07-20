# Python CIMIS Client - Examples

This directory contains comprehensive examples demonstrating how to use the Python CIMIS Client library for various agricultural, irrigation, and climate analysis tasks.

## 📁 Example Files

### 🌤️ [basic_usage.py](basic_usage.py)
**Start here for new users!**

Demonstrates fundamental features:
- Getting daily weather data for stations
- Retrieving data by zip code and coordinates  
- Station information lookup
- Basic CSV export
- Hourly data retrieval
- Error handling basics

**Run it:**
```bash
python examples/basic_usage.py
```

### 🔬 [advanced_usage.py](advanced_usage.py)
**For users ready to explore advanced features**

Advanced patterns and techniques:
- Multiple target types in single requests
- Specific data item selection
- Metric vs English units
- Complex error handling strategies
- Data filtering and processing
- Organized CSV export patterns
- Connection timeout handling

**Run it:**
```bash
python examples/advanced_usage.py
```

### 🌾 [real_world_use_cases.py](real_world_use_cases.py)
**Practical agricultural and irrigation applications**

Real-world scenarios:
- Irrigation scheduling calculations
- Crop water use analysis across growing seasons
- Weather monitoring dashboards
- Frost protection alert systems
- Climate trend analysis and comparisons

**Run it:**
```bash
python examples/real_world_use_cases.py
```

### 📊 [data_analysis.py](data_analysis.py)
**Statistical and analytical techniques**

Data science applications:
- Statistical analysis (mean, median, correlation)
- Time series analysis and trend detection
- Comparative location analysis
- Growing Degree Days (GDD) calculations
- Water stress analysis and recommendations

**Run it:**
```bash
python examples/data_analysis.py
```

## 🚀 Quick Start

1. **Get your CIMIS API Key:**
   - Visit https://et.water.ca.gov/Rest/Index
   - Register for a free account
   - Generate your API key

2. **Set your API key as environment variable (recommended):**
   ```bash
   # Windows
   set CIMIS_API_KEY=your-actual-api-key-here
   
   # Linux/Mac
   export CIMIS_API_KEY=your-actual-api-key-here
   ```

3. **Run any example:**
   ```bash
   cd "Python-CIMIS-Client"
   python examples/basic_usage.py
   ```

## 📋 Example Scenarios by Use Case

### 🌾 **Agricultural Management**
- **Irrigation Scheduling**: `real_world_use_cases.py` → `irrigation_scheduling_example()`
- **Crop Water Use**: `real_world_use_cases.py` → `crop_water_use_analysis()`
- **Growing Degree Days**: `data_analysis.py` → `growing_degree_days()`

### 🌡️ **Weather Monitoring**
- **Multi-Location Dashboard**: `real_world_use_cases.py` → `weather_monitoring_dashboard()`
- **Statistical Analysis**: `data_analysis.py` → `statistical_analysis()`
- **Time Series Trends**: `data_analysis.py` → `time_series_analysis()`

### ❄️ **Risk Management**
- **Frost Protection**: `real_world_use_cases.py` → `frost_protection_alert()`
- **Water Stress Monitoring**: `data_analysis.py` → `water_stress_analysis()`

### 📈 **Climate Research**
- **Long-term Trends**: `real_world_use_cases.py` → `climate_trend_analysis()`
- **Regional Comparisons**: `data_analysis.py` → `comparative_analysis()`

## 🎯 Data Retrieval Patterns

### By Location Type
```python
# Station numbers
client.get_daily_data(targets=[2, 8, 12])

# Zip codes  
client.get_daily_data(targets=["95823", "94503"])

# Coordinates
client.get_daily_data(targets=["lat=38.5816,lng=-121.4944"])

# Mixed targets
client.get_daily_data(targets=[2, "95823", "lat=38.5816,lng=-121.4944"])
```

### By Data Type
```python
# All available data (default)
client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-07")

# Specific data items only
client.get_daily_data(
    targets=[2], 
    start_date="2023-01-01", 
    end_date="2023-01-07",
    data_items=["day-air-tmp-avg", "day-eto", "day-precip"]
)

# Hourly data (WSN stations only)
client.get_hourly_data(targets=[2], start_date="2023-01-01", end_date="2023-01-01")
```

### By Time Period
```python
from datetime import date, timedelta

# Recent data
yesterday = date.today() - timedelta(days=1)
week_ago = yesterday - timedelta(days=6)
client.get_daily_data(targets=[2], start_date=week_ago, end_date=yesterday)

# Specific dates
client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-30")

# Growing season
client.get_daily_data(targets=[2], start_date="2023-04-01", end_date="2023-09-30")
```

## 💾 CSV Export Examples

### Automatic Filename Generation
```python
# Generates filename based on stations and dates
csv_file = client.export_to_csv(weather_data)
# Result: "Station2_FivePoints_20230101_to_20230107.csv"
```

### Custom Filenames
```python
# Custom filename
client.export_to_csv(weather_data, filename="my_weather_data.csv")

# Organized by date
date_str = f"weather_data_{start_date}_{end_date}.csv"
client.export_to_csv(weather_data, filename=date_str)

# Station-specific exports
for provider in weather_data.providers:
    station_file = f"station_{provider.records[0].station}_data.csv"
    single_station_data = create_single_provider_data(provider)
    client.export_to_csv(single_station_data, filename=station_file)
```

## ⚠️ Error Handling Patterns

### Robust Error Handling
```python
from python_cimis.exceptions import CimisAPIError, CimisConnectionError

try:
    weather_data = client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-07")
except CimisAPIError as e:
    print(f"API Error: {e} (Code: {e.error_code})")
except CimisConnectionError as e:
    print(f"Connection Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Data Validation
```python
# Check for data availability
all_records = weather_data.get_all_records()
if not all_records:
    print("No data available for the requested period")

# Check specific stations
station_2_data = weather_data.get_records_by_station("2")
if len(station_2_data) < expected_days:
    print("Incomplete data for station 2")
```

## 🔧 Configuration Tips

### Environment Variables
```bash
# Required
CIMIS_API_KEY=your-api-key-here

# Optional
CIMIS_BASE_URL=https://et.water.ca.gov/api  # Custom API endpoint
CIMIS_TIMEOUT=30                            # Request timeout in seconds
```

### Client Configuration
```python
# Basic client
client = CimisClient(app_key="your-key")

# Custom timeout
client = CimisClient(app_key="your-key", timeout=60)

# Environment variable (recommended)
import os
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))
```

## 📊 Data Processing Examples

### Temperature Analysis
```python
# Extract temperature data
temperatures = []
for record in weather_data.get_all_records():
    temp_data = record.data_values.get('day-air-tmp-avg')
    if temp_data and temp_data.value:
        temperatures.append(float(temp_data.value))

# Calculate statistics
avg_temp = sum(temperatures) / len(temperatures)
max_temp = max(temperatures)
min_temp = min(temperatures)
```

### ETo Calculations
```python
# Calculate irrigation needs
total_eto = 0
total_precip = 0

for record in weather_data.get_all_records():
    eto_data = record.data_values.get('day-eto')
    precip_data = record.data_values.get('day-precip')
    
    if eto_data and eto_data.value:
        total_eto += float(eto_data.value)
    
    if precip_data and precip_data.value:
        total_precip += float(precip_data.value)

irrigation_need = total_eto - total_precip
```

## 🎨 Visualization Integration

While the examples use text-based output, you can easily integrate with visualization libraries:

### Matplotlib Example
```python
import matplotlib.pyplot as plt

# Get data
weather_data = client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-31")

# Extract for plotting
dates = []
temperatures = []
for record in weather_data.get_all_records():
    dates.append(record.date)
    temp_data = record.data_values.get('day-air-tmp-avg')
    if temp_data and temp_data.value:
        temperatures.append(float(temp_data.value))

# Plot
plt.figure(figsize=(12, 6))
plt.plot(dates, temperatures)
plt.title('Daily Average Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Pandas Integration
```python
import pandas as pd

# Convert to DataFrame
data_rows = []
for record in weather_data.get_all_records():
    row = {'date': record.date, 'station': record.station}
    for key, value in record.data_values.items():
        row[key] = float(value.value) if value.value else None
    data_rows.append(row)

df = pd.DataFrame(data_rows)
print(df.describe())
```

## 🆘 Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**
   - Check your API key is correct
   - Ensure no extra spaces or characters
   - Verify key is active on CIMIS website

2. **"No data available" Results**
   - Check date range is not in the future
   - Verify station numbers exist
   - Some historical data may have gaps

3. **Timeout Errors**
   - Increase timeout: `CimisClient(app_key="key", timeout=60)`
   - Reduce date range for large requests
   - Check internet connection

4. **Large CSV Files**
   - Limit date ranges for exports
   - Use specific data items instead of all
   - Consider splitting by station

### Getting Help

- Check the main README.md for library documentation
- Review test files for additional usage patterns
- Visit CIMIS API documentation: https://et.water.ca.gov/Rest/Index
- Report issues on the project repository

## 🚀 Next Steps

After running these examples:

1. **Adapt for your needs**: Modify the examples for your specific locations and requirements
2. **Combine techniques**: Mix patterns from different examples
3. **Add automation**: Set up scheduled runs for regular monitoring
4. **Integrate visualization**: Add charts and graphs to your analysis
5. **Build applications**: Use these patterns in larger agricultural management systems

Happy coding! 🌾💧📊
