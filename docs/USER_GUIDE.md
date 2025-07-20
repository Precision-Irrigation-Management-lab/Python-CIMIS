# Python CIMIS Client - User Guide

Comprehensive user guide for the Python CIMIS Client library with practical examples and best practices.

## Table of Contents

- [Introduction](#introduction)
- [Understanding CIMIS Data](#understanding-cimis-data)
- [Basic Usage Patterns](#basic-usage-patterns)
- [Advanced Features](#advanced-features)
- [Data Processing](#data-processing)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Integration Examples](#integration-examples)

---

## Introduction

The Python CIMIS Client library provides easy access to California's Irrigation Management Information System (CIMIS) data. This guide will help you understand how to effectively use the library for various agricultural, irrigation, and climate analysis tasks.

### What is CIMIS?

CIMIS is a program managed by the California Department of Water Resources (DWR) that provides weather data and evapotranspiration (ET) estimates to assist with irrigation scheduling and water management decisions.

### Data Sources

CIMIS provides data from two main sources:

1. **Weather Station Network (WSN)**: Physical weather stations throughout California
2. **Spatial CIMIS System (SCS)**: Grid-based interpolated data covering areas without stations

---

## Understanding CIMIS Data

### Data Types Available

#### Daily Data
Available from both WSN and SCS sources:

- **Temperature**: Average, maximum, minimum air temperature
- **Humidity**: Average, maximum, minimum relative humidity  
- **Evapotranspiration**: Reference ET (ETo), ASCE standardized ET
- **Solar Radiation**: Average daily solar radiation
- **Wind**: Average speed, direction components, wind run
- **Soil Temperature**: Average, maximum, minimum (WSN only)
- **Precipitation**: Daily rainfall totals
- **Other**: Dew point, vapor pressure

#### Hourly Data
Available from WSN stations only:

- **Temperature**: Hourly air and soil temperature
- **Humidity**: Hourly relative humidity
- **ET**: Hourly reference evapotranspiration
- **Solar**: Hourly solar and net radiation
- **Wind**: Hourly speed and direction
- **Other**: Hourly precipitation, dew point, vapor pressure

### Data Quality

CIMIS data includes quality control (QC) flags:

- **" " (space)**: Measured or calculated value
- **"Y"**: Missing data replaced with estimated value
- **"M"**: Missing data not replaced

Always check QC flags when processing data for critical applications.

---

## Basic Usage Patterns

### 1. Simple Data Retrieval

```python
from python_cimis import CimisClient
from datetime import date, timedelta
import os

# Initialize client
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

# Get recent daily data
end_date = date.today() - timedelta(days=1)  # Yesterday
start_date = end_date - timedelta(days=6)    # Week ago

weather_data = client.get_daily_data(
    targets=[2],  # Five Points station
    start_date=start_date,
    end_date=end_date
)

print(f"Retrieved {len(weather_data.get_all_records())} records")
```

### 2. Multiple Location Types

```python
# Mix different target types in one request
weather_data = client.get_daily_data(
    targets=[
        2,                                      # Station number
        "95823",                               # Zip code
        "lat=38.5816,lng=-121.4944"            # Coordinates
    ],
    start_date="2023-06-01",
    end_date="2023-06-07"
)
```

### 3. Specific Data Items

```python
# Request only specific weather variables
weather_data = client.get_daily_data(
    targets=[2, 8, 127],
    start_date="2023-06-01",
    end_date="2023-06-30",
    data_items=[
        "day-air-tmp-avg",    # Average temperature
        "day-eto",            # Reference ET
        "day-precip",         # Precipitation
        "day-rel-hum-avg"     # Average humidity
    ]
)
```

### 4. CSV Export

```python
# Export with auto-generated filename
csv_file = client.export_to_csv(weather_data)
print(f"Exported to: {csv_file}")

# Export with custom filename
client.export_to_csv(weather_data, filename="irrigation_data_june_2023.csv")
```

---

## Advanced Features

### 1. Error Handling

```python
from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError

def robust_data_request(client, targets, start_date, end_date, max_retries=3):
    """Request data with comprehensive error handling."""
    
    for attempt in range(max_retries):
        try:
            return client.get_daily_data(targets, start_date, end_date)
            
        except CimisAuthenticationError:
            print("Invalid API key - check your credentials")
            break
            
        except CimisConnectionError as e:
            print(f"Connection error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                print("Max retries reached")
                break
                
        except CimisAPIError as e:
            print(f"API error: {e.message}")
            if e.error_code == "NO_DATA":
                print("No data available for this period")
            break
            
    return None
```

### 2. Data Validation

```python
def validate_weather_data(weather_data, expected_days=None):
    """Validate retrieved weather data."""
    
    all_records = weather_data.get_all_records()
    
    # Check if any data was returned
    if not all_records:
        print("Warning: No data records found")
        return False
    
    # Check expected number of days
    if expected_days and len(all_records) < expected_days:
        print(f"Warning: Expected {expected_days} records, got {len(all_records)}")
    
    # Check for missing data
    records_with_missing_data = 0
    for record in all_records:
        for key, value in record.data_values.items():
            if value.qc == "M":  # Missing data
                records_with_missing_data += 1
                break
    
    if records_with_missing_data > 0:
        percentage = (records_with_missing_data / len(all_records)) * 100
        print(f"Warning: {records_with_missing_data} records ({percentage:.1f}%) have missing data")
    
    print(f"Validation complete: {len(all_records)} records, {records_with_missing_data} with missing data")
    return True

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
validate_weather_data(weather_data, expected_days=7)
```

### 3. Station Discovery

```python
def find_stations_by_criteria(client, county=None, active_only=True, eto_only=False):
    """Find stations matching specific criteria."""
    
    all_stations = client.get_stations()
    filtered_stations = []
    
    for station in all_stations:
        # Apply filters
        if active_only and not station.is_active:
            continue
        
        if eto_only and not station.is_eto_station:
            continue
            
        if county and county.lower() not in station.county.lower():
            continue
            
        filtered_stations.append(station)
    
    return filtered_stations

# Find active ETo stations in Fresno County
fresno_stations = find_stations_by_criteria(
    client, 
    county="Fresno", 
    active_only=True, 
    eto_only=True
)

for station in fresno_stations:
    print(f"Station {station.station_nbr}: {station.name} ({station.city})")
```

### 4. Batch Processing

```python
def process_stations_in_batches(client, station_list, start_date, end_date, batch_size=10):
    """Process large station lists in batches to avoid API limits."""
    
    all_data = []
    
    for i in range(0, len(station_list), batch_size):
        batch = station_list[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}: stations {batch}")
        
        try:
            batch_data = client.get_daily_data(
                targets=batch,
                start_date=start_date,
                end_date=end_date
            )
            all_data.append(batch_data)
            
        except Exception as e:
            print(f"Error processing batch {batch}: {e}")
            
        # Rate limiting - be respectful to the API
        time.sleep(1)
    
    return all_data

# Process 50 stations in batches of 10
stations = list(range(1, 51))
batch_results = process_stations_in_batches(
    client, stations, "2023-06-01", "2023-06-07"
)
```

---

## Data Processing

### 1. Temperature Analysis

```python
def analyze_temperature_data(weather_data):
    """Analyze temperature patterns from weather data."""
    
    temperatures = {
        'avg': [],
        'max': [],
        'min': [],
        'dates': []
    }
    
    for record in weather_data.get_all_records():
        temperatures['dates'].append(record.date)
        
        # Extract temperature values
        avg_temp = record.data_values.get('day-air-tmp-avg')
        max_temp = record.data_values.get('day-air-tmp-max')
        min_temp = record.data_values.get('day-air-tmp-min')
        
        temperatures['avg'].append(float(avg_temp.value) if avg_temp and avg_temp.value else None)
        temperatures['max'].append(float(max_temp.value) if max_temp and max_temp.value else None)
        temperatures['min'].append(float(min_temp.value) if min_temp and min_temp.value else None)
    
    # Calculate statistics
    valid_avg_temps = [t for t in temperatures['avg'] if t is not None]
    if valid_avg_temps:
        stats = {
            'mean_temp': sum(valid_avg_temps) / len(valid_avg_temps),
            'max_temp': max(temperatures['max']) if any(temperatures['max']) else None,
            'min_temp': min(temperatures['min']) if any(temperatures['min']) else None,
            'temp_range': max(valid_avg_temps) - min(valid_avg_temps)
        }
        return temperatures, stats
    
    return temperatures, {}

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-30")
temp_data, temp_stats = analyze_temperature_data(weather_data)

print(f"Mean temperature: {temp_stats['mean_temp']:.1f}°F")
print(f"Temperature range: {temp_stats['temp_range']:.1f}°F")
```

### 2. Irrigation Scheduling

```python
def calculate_irrigation_needs(weather_data, crop_coefficient=1.0, irrigation_efficiency=0.85):
    """Calculate irrigation needs based on ET and precipitation."""
    
    total_eto = 0
    total_precip = 0
    irrigation_events = []
    
    for record in weather_data.get_all_records():
        date = record.date
        
        # Get ETo and precipitation
        eto_data = record.data_values.get('day-eto')
        precip_data = record.data_values.get('day-precip')
        
        eto = float(eto_data.value) if eto_data and eto_data.value else 0
        precip = float(precip_data.value) if precip_data and precip_data.value else 0
        
        # Calculate crop water use
        crop_et = eto * crop_coefficient
        
        # Calculate net irrigation need
        net_irrigation = max(0, crop_et - precip)
        gross_irrigation = net_irrigation / irrigation_efficiency if net_irrigation > 0 else 0
        
        if gross_irrigation > 0:
            irrigation_events.append({
                'date': date,
                'eto': eto,
                'precip': precip,
                'crop_et': crop_et,
                'net_irrigation': net_irrigation,
                'gross_irrigation': gross_irrigation
            })
        
        total_eto += eto
        total_precip += precip
    
    total_crop_et = total_eto * crop_coefficient
    total_irrigation_need = max(0, total_crop_et - total_precip)
    
    return {
        'total_eto': total_eto,
        'total_precip': total_precip,
        'total_crop_et': total_crop_et,
        'total_irrigation_need': total_irrigation_need,
        'irrigation_events': irrigation_events
    }

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-30")
irrigation_analysis = calculate_irrigation_needs(weather_data, crop_coefficient=1.2)

print(f"Total irrigation needed: {irrigation_analysis['total_irrigation_need']:.2f} inches")
print(f"Number of irrigation events: {len(irrigation_analysis['irrigation_events'])}")
```

### 3. Growing Degree Days (GDD)

```python
def calculate_gdd(weather_data, base_temp=50, max_temp=86):
    """Calculate Growing Degree Days."""
    
    gdd_daily = []
    cumulative_gdd = 0
    
    for record in weather_data.get_all_records():
        # Get daily temperatures
        max_temp_data = record.data_values.get('day-air-tmp-max')
        min_temp_data = record.data_values.get('day-air-tmp-min')
        
        if max_temp_data and min_temp_data and max_temp_data.value and min_temp_data.value:
            daily_max = min(float(max_temp_data.value), max_temp)  # Cap maximum
            daily_min = max(float(min_temp_data.value), base_temp)  # Floor minimum
            
            # Calculate GDD for this day
            daily_gdd = max(0, ((daily_max + daily_min) / 2) - base_temp)
            cumulative_gdd += daily_gdd
            
            gdd_daily.append({
                'date': record.date,
                'daily_gdd': daily_gdd,
                'cumulative_gdd': cumulative_gdd,
                'max_temp': float(max_temp_data.value),
                'min_temp': float(min_temp_data.value)
            })
    
    return gdd_daily

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-04-01", end_date="2023-09-30")
gdd_data = calculate_gdd(weather_data, base_temp=50)

if gdd_data:
    final_gdd = gdd_data[-1]['cumulative_gdd']
    print(f"Total Growing Degree Days: {final_gdd:.1f}")
```

---

## Best Practices

### 1. API Usage Guidelines

```python
# Good practices for API usage
class CimisClientWrapper:
    def __init__(self, api_key, timeout=30):
        self.client = CimisClient(app_key=api_key, timeout=timeout)
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum seconds between requests
    
    def rate_limited_request(self, method, *args, **kwargs):
        """Make rate-limited API requests."""
        import time
        
        # Ensure minimum time between requests
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        result = getattr(self.client, method)(*args, **kwargs)
        self.last_request_time = time.time()
        
        return result
    
    def get_daily_data(self, *args, **kwargs):
        return self.rate_limited_request('get_daily_data', *args, **kwargs)
```

### 2. Data Caching

```python
import pickle
import os
from datetime import datetime

class CimisDataCache:
    def __init__(self, cache_dir="cimis_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, targets, start_date, end_date, data_items=None):
        """Generate cache key for request parameters."""
        key_parts = [
            str(sorted(targets)),
            str(start_date),
            str(end_date),
            str(sorted(data_items)) if data_items else "all"
        ]
        return "_".join(key_parts).replace("/", "-").replace(":", "-")
    
    def get_cached_data(self, cache_key, max_age_hours=24):
        """Retrieve cached data if it exists and is recent."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            # Check file age
            file_age = datetime.now().timestamp() - os.path.getmtime(cache_file)
            if file_age < max_age_hours * 3600:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
        
        return None
    
    def cache_data(self, cache_key, data):
        """Cache weather data."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

# Usage with caching
def get_cached_weather_data(client, targets, start_date, end_date, data_items=None):
    cache = CimisDataCache()
    cache_key = cache.get_cache_key(targets, start_date, end_date, data_items)
    
    # Try to get from cache first
    cached_data = cache.get_cached_data(cache_key)
    if cached_data:
        print("Using cached data")
        return cached_data
    
    # Fetch fresh data
    print("Fetching fresh data from API")
    weather_data = client.get_daily_data(
        targets=targets,
        start_date=start_date,
        end_date=end_date,
        data_items=data_items
    )
    
    # Cache the data
    cache.cache_data(cache_key, weather_data)
    return weather_data
```

### 3. Configuration Management

```python
import json
import os

class CimisConfig:
    def __init__(self, config_file="cimis_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or environment."""
        default_config = {
            "api_key": os.getenv('CIMIS_API_KEY'),
            "timeout": 30,
            "default_stations": [2, 8, 127],
            "default_data_items": [
                "day-air-tmp-avg", "day-eto", "day-precip", "day-rel-hum-avg"
            ],
            "csv_export_dir": "exports",
            "cache_enabled": True,
            "cache_max_age_hours": 24
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                file_config = json.load(f)
                default_config.update(file_config)
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)

# Usage
config = CimisConfig()
client = CimisClient(app_key=config.get('api_key'), timeout=config.get('timeout'))
```

---

## Common Use Cases

### 1. Agricultural Decision Support

```python
def agricultural_advisory(client, station_id, crop_type="tomato"):
    """Generate agricultural advisory based on recent weather."""
    
    # Get last 7 days of data
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=6)
    
    weather_data = client.get_daily_data(
        targets=[station_id],
        start_date=start_date,
        end_date=end_date
    )
    
    # Analyze conditions
    temps = []
    humidity = []
    precip_total = 0
    eto_total = 0
    
    for record in weather_data.get_all_records():
        temp_data = record.data_values.get('day-air-tmp-avg')
        humid_data = record.data_values.get('day-rel-hum-avg')
        precip_data = record.data_values.get('day-precip')
        eto_data = record.data_values.get('day-eto')
        
        if temp_data and temp_data.value:
            temps.append(float(temp_data.value))
        if humid_data and humid_data.value:
            humidity.append(float(humid_data.value))
        if precip_data and precip_data.value:
            precip_total += float(precip_data.value)
        if eto_data and eto_data.value:
            eto_total += float(eto_data.value)
    
    # Generate advisory
    advisory = {
        'period': f"{start_date} to {end_date}",
        'avg_temp': sum(temps) / len(temps) if temps else 0,
        'avg_humidity': sum(humidity) / len(humidity) if humidity else 0,
        'total_precip': precip_total,
        'total_eto': eto_total,
        'recommendations': []
    }
    
    # Add recommendations based on conditions
    if advisory['avg_temp'] > 90:
        advisory['recommendations'].append("High temperatures detected - increase irrigation frequency")
    
    if advisory['avg_humidity'] > 80:
        advisory['recommendations'].append("High humidity - monitor for fungal diseases")
    
    if advisory['total_precip'] < 0.5 and advisory['total_eto'] > 1.0:
        advisory['recommendations'].append("Dry conditions - consider supplemental irrigation")
    
    return advisory
```

### 2. Water Management Dashboard

```python
def water_management_summary(client, region_stations, period_days=30):
    """Generate water management summary for a region."""
    
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=period_days - 1)
    
    # Get data for all stations in region
    weather_data = client.get_daily_data(
        targets=region_stations,
        start_date=start_date,
        end_date=end_date
    )
    
    # Aggregate data by station
    station_summaries = {}
    
    for provider in weather_data.providers:
        for record in provider.records:
            station = record.station
            
            if station not in station_summaries:
                station_summaries[station] = {
                    'eto_total': 0,
                    'precip_total': 0,
                    'days_with_data': 0,
                    'temp_sum': 0,
                    'temp_count': 0
                }
            
            summary = station_summaries[station]
            summary['days_with_data'] += 1
            
            # Accumulate ETo and precipitation
            eto_data = record.data_values.get('day-eto')
            precip_data = record.data_values.get('day-precip')
            temp_data = record.data_values.get('day-air-tmp-avg')
            
            if eto_data and eto_data.value:
                summary['eto_total'] += float(eto_data.value)
            
            if precip_data and precip_data.value:
                summary['precip_total'] += float(precip_data.value)
                
            if temp_data and temp_data.value:
                summary['temp_sum'] += float(temp_data.value)
                summary['temp_count'] += 1
    
    # Calculate regional averages
    region_summary = {
        'period': f"{start_date} to {end_date}",
        'stations': len(station_summaries),
        'avg_eto': 0,
        'avg_precip': 0,
        'avg_temp': 0,
        'water_deficit': 0
    }
    
    if station_summaries:
        total_eto = sum(s['eto_total'] for s in station_summaries.values())
        total_precip = sum(s['precip_total'] for s in station_summaries.values())
        total_temp = sum(s['temp_sum'] for s in station_summaries.values())
        total_temp_count = sum(s['temp_count'] for s in station_summaries.values())
        
        region_summary['avg_eto'] = total_eto / len(station_summaries)
        region_summary['avg_precip'] = total_precip / len(station_summaries)
        region_summary['avg_temp'] = total_temp / total_temp_count if total_temp_count > 0 else 0
        region_summary['water_deficit'] = region_summary['avg_eto'] - region_summary['avg_precip']
    
    return region_summary, station_summaries
```

---

## Integration Examples

### 1. Pandas Integration

```python
import pandas as pd

def weather_data_to_dataframe(weather_data):
    """Convert CIMIS weather data to pandas DataFrame."""
    
    records = []
    
    for record in weather_data.get_all_records():
        row = {
            'date': pd.to_datetime(record.date),
            'station': record.station,
            'julian': record.julian
        }
        
        # Add all data values
        for key, value in record.data_values.items():
            row[f"{key}_value"] = float(value.value) if value.value else None
            row[f"{key}_qc"] = value.qc
            row[f"{key}_unit"] = value.unit
        
        records.append(row)
    
    df = pd.DataFrame(records)
    df.set_index('date', inplace=True)
    return df

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-30")
df = weather_data_to_dataframe(weather_data)

# Pandas analysis
print(df['day-air-tmp-avg_value'].describe())
print(f"Correlation between temp and humidity: {df['day-air-tmp-avg_value'].corr(df['day-rel-hum-avg_value']):.3f}")
```

### 2. Visualization with Matplotlib

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_temperature_and_eto(weather_data, title="Temperature and ETo"):
    """Create a dual-axis plot of temperature and ETo."""
    
    dates = []
    temps = []
    etos = []
    
    for record in weather_data.get_all_records():
        dates.append(pd.to_datetime(record.date))
        
        temp_data = record.data_values.get('day-air-tmp-avg')
        eto_data = record.data_values.get('day-eto')
        
        temps.append(float(temp_data.value) if temp_data and temp_data.value else None)
        etos.append(float(eto_data.value) if eto_data and eto_data.value else None)
    
    # Create figure with dual y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Temperature plot
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°F)', color=color)
    ax1.plot(dates, temps, color=color, linewidth=2, label='Avg Temperature')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # ETo plot on second y-axis
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Reference ET (inches)', color=color)
    ax2.plot(dates, etos, color=color, linewidth=2, label='Reference ET')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Usage
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-30")
plot_temperature_and_eto(weather_data, "Five Points Station - June 2023")
```

### 3. Database Integration

```python
import sqlite3
from contextlib import contextmanager

class CimisDatabase:
    def __init__(self, db_path="cimis_data.db"):
        self.db_path = db_path
        self.create_tables()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def create_tables(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    station TEXT,
                    data_item TEXT,
                    value REAL,
                    qc TEXT,
                    unit TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_date_station 
                ON weather_data(date, station)
            ''')
    
    def store_weather_data(self, weather_data):
        """Store weather data in database."""
        with self.get_connection() as conn:
            for record in weather_data.get_all_records():
                for key, value in record.data_values.items():
                    conn.execute('''
                        INSERT OR REPLACE INTO weather_data 
                        (date, station, data_item, value, qc, unit)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        record.date,
                        record.station,
                        key,
                        float(value.value) if value.value else None,
                        value.qc,
                        value.unit
                    ))
            conn.commit()
    
    def get_station_data(self, station, start_date, end_date):
        """Retrieve data for a station from database."""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT date, data_item, value, qc, unit
                FROM weather_data
                WHERE station = ? AND date BETWEEN ? AND ?
                ORDER BY date, data_item
            ''', (station, start_date, end_date))
            
            return cursor.fetchall()

# Usage
db = CimisDatabase()
weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
db.store_weather_data(weather_data)

# Retrieve from database
stored_data = db.get_station_data("2", "2023-06-01", "2023-06-07")
print(f"Retrieved {len(stored_data)} data points from database")
```

---

This user guide provides comprehensive examples and patterns for effectively using the Python CIMIS Client library. For more specific use cases or advanced integrations, refer to the API Reference documentation and the examples directory.
