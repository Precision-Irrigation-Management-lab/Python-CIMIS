User Guide
==========

This comprehensive user guide covers advanced features and best practices for the Python CIMIS Client library.

.. contents:: Table of Contents
   :local:
   :depth: 2

Understanding CIMIS Data
------------------------

Data Sources
~~~~~~~~~~~~

CIMIS provides data from two main sources:

**Weather Station Network (WSN)**
   Physical weather stations throughout California providing:
   
   - Daily and hourly measurements
   - High-quality instrumentation
   - Direct measurements of meteorological parameters
   - Limited geographic coverage

**Spatial CIMIS System (SCS)**
   Grid-based interpolated data covering:
   
   - Areas without physical stations
   - Daily data only (no hourly measurements)
   - Interpolated from nearby WSN stations and satellite data
   - Statewide coverage

Data Types Available
~~~~~~~~~~~~~~~~~~~~

**Daily Data Items**
   Available from both WSN and SCS sources:

   - Temperature: Average, maximum, minimum air temperature
   - Humidity: Average, maximum, minimum relative humidity
   - Evapotranspiration: Reference ET (ETo), ASCE standardized ET
   - Solar Radiation: Average daily solar radiation
   - Wind: Average speed, direction components, wind run
   - Soil Temperature: Average, maximum, minimum (WSN only)
   - Precipitation: Daily rainfall totals
   - Other: Dew point, vapor pressure

**Hourly Data Items**
   Available from WSN stations only:

   - Temperature: Hourly air and soil temperature
   - Humidity: Hourly relative humidity
   - ET: Hourly reference evapotranspiration
   - Solar: Hourly solar and net radiation
   - Wind: Hourly speed and direction
   - Other: Hourly precipitation, dew point, vapor pressure

Quality Control
~~~~~~~~~~~~~~~

CIMIS data includes quality control (QC) flags:

- **" " (space)**: Measured or calculated value
- **"Y"**: Missing data replaced with estimated value
- **"M"**: Missing data not replaced

Always check QC flags when processing data for critical applications.

Advanced Usage Patterns
------------------------

Multiple Target Types
~~~~~~~~~~~~~~~~~~~~~~

You can mix different target types in a single request:

.. code-block:: python

   from python_cimis import CimisClient
   import os

   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

   # Mix different target types
   weather_data = client.get_daily_data(
       targets=[
           2,                                      # Station number
           "95823",                               # Zip code
           "lat=38.5816,lng=-121.4944",          # Coordinates
           "addr-name=Capitol,addr=1315 10th Street Sacramento, CA 95814"  # Address
       ],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

Error Handling and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement comprehensive error handling:

.. code-block:: python

   from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError
   import time

   def robust_data_request(client, targets, start_date, end_date, max_retries=3):
       """Request data with comprehensive error handling."""
       
       for attempt in range(max_retries):
           try:
               weather_data = client.get_daily_data(
                   targets=targets,
                   start_date=start_date,
                   end_date=end_date
               )
               return weather_data
               
           except CimisAuthenticationError as e:
               print(f"Authentication error: {e.message}")
               break  # Don't retry auth errors
               
           except CimisConnectionError as e:
               print(f"Connection error (attempt {attempt + 1}): {e.message}")
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
                   
           except CimisAPIError as e:
               print(f"API error: {e.message} (Code: {e.error_code})")
               break  # Don't retry API errors
               
       return None

Data Validation
~~~~~~~~~~~~~~~

Validate retrieved data before processing:

.. code-block:: python

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
               if value.qc == 'M':  # Missing data
                   records_with_missing_data += 1
                   break
       
       if records_with_missing_data > 0:
           percentage = (records_with_missing_data / len(all_records)) * 100
           print(f"Warning: {records_with_missing_data} records ({percentage:.1f}%) have missing data")
       
       print(f"Validation complete: {len(all_records)} records, {records_with_missing_data} with missing data")
       return True

Station Discovery
~~~~~~~~~~~~~~~~~

Find stations that meet specific criteria:

.. code-block:: python

   def find_stations_by_criteria(client, county=None, active_only=True, eto_only=False):
       """Find stations matching specific criteria."""
       
       all_stations = client.get_stations()
       filtered_stations = []
       
       for station in all_stations:
           # Apply filters
           if county and station.county.lower() != county.lower():
               continue
           if active_only and not station.is_active:
               continue
           if eto_only and not station.is_eto_station:
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

Batch Processing
~~~~~~~~~~~~~~~~

Process large station lists efficiently:

.. code-block:: python

   import time

   def process_stations_in_batches(client, station_list, start_date, end_date, batch_size=10):
       """Process large station lists in batches to avoid API limits."""
       
       all_data = []
       
       for i in range(0, len(station_list), batch_size):
           batch = station_list[i:i + batch_size]
           
           try:
               weather_data = client.get_daily_data(
                   targets=batch,
                   start_date=start_date,
                   end_date=end_date
               )
               all_data.extend(weather_data.get_all_records())
               
               # Rate limiting
               time.sleep(1)
               
           except Exception as e:
               print(f"Error processing batch {i//batch_size + 1}: {e}")
       
       return all_data

Data Processing Examples
------------------------

Temperature Analysis
~~~~~~~~~~~~~~~~~~~~

Analyze temperature patterns:

.. code-block:: python

   def analyze_temperature_data(weather_data):
       """Analyze temperature patterns from weather data."""
       
       temperatures = {
           'avg': [],
           'max': [],
           'min': [],
           'dates': []
       }
       
       for record in weather_data.get_all_records():
           # Extract temperature data
           avg_temp = record.data_values.get('day-air-tmp-avg')
           max_temp = record.data_values.get('day-air-tmp-max')
           min_temp = record.data_values.get('day-air-tmp-min')
           
           if avg_temp and avg_temp.value:
               temperatures['avg'].append(float(avg_temp.value))
               temperatures['dates'].append(record.date)
           
           if max_temp and max_temp.value:
               temperatures['max'].append(float(max_temp.value))
           
           if min_temp and min_temp.value:
               temperatures['min'].append(float(min_temp.value))
       
       # Calculate statistics
       stats = {}
       if temperatures['avg']:
           stats['mean_temp'] = sum(temperatures['avg']) / len(temperatures['avg'])
           stats['max_temp'] = max(temperatures['max']) if temperatures['max'] else None
           stats['min_temp'] = min(temperatures['min']) if temperatures['min'] else None
           stats['temp_range'] = stats['max_temp'] - stats['min_temp'] if stats['max_temp'] and stats['min_temp'] else None
       
       return temperatures, stats

Irrigation Scheduling
~~~~~~~~~~~~~~~~~~~~~

Calculate irrigation needs based on ET and precipitation:

.. code-block:: python

   def calculate_irrigation_needs(weather_data, crop_coefficient=1.0, irrigation_efficiency=0.85):
       """Calculate irrigation needs based on ET and precipitation."""
       
       irrigation_data = []
       cumulative_deficit = 0
       
       for record in weather_data.get_all_records():
           # Get ET and precipitation
           eto_data = record.data_values.get('day-eto')
           precip_data = record.data_values.get('day-precip')
           
           if not (eto_data and eto_data.value):
               continue
               
           eto = float(eto_data.value)
           precip = float(precip_data.value) if precip_data and precip_data.value else 0
           
           # Calculate crop ET
           etc = eto * crop_coefficient
           
           # Calculate water deficit/surplus
           daily_deficit = etc - precip
           cumulative_deficit += daily_deficit
           
           # Determine if irrigation is needed (threshold: 0.5 inches deficit)
           irrigation_needed = cumulative_deficit > 0.5
           irrigation_amount = cumulative_deficit / irrigation_efficiency if irrigation_needed else 0
           
           if irrigation_needed:
               cumulative_deficit = 0  # Reset after irrigation
           
           irrigation_data.append({
               'date': record.date,
               'eto': eto,
               'etc': etc,
               'precipitation': precip,
               'daily_deficit': daily_deficit,
               'cumulative_deficit': cumulative_deficit,
               'irrigation_needed': irrigation_needed,
               'irrigation_amount': irrigation_amount
           })
       
       # Calculate summary statistics
       summary = {
           'total_eto': sum(d['eto'] for d in irrigation_data),
           'total_etc': sum(d['etc'] for d in irrigation_data),
           'total_precipitation': sum(d['precipitation'] for d in irrigation_data),
           'total_irrigation_need': sum(d['irrigation_amount'] for d in irrigation_data),
           'irrigation_events': [d for d in irrigation_data if d['irrigation_needed']]
       }
       
       return {
           'daily_data': irrigation_data,
           'summary': summary
       }

Growing Degree Days (GDD)
~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate Growing Degree Days for crop development:

.. code-block:: python

   def calculate_gdd(weather_data, base_temp=50, max_temp=86):
       """Calculate Growing Degree Days."""
       
       gdd_data = []
       cumulative_gdd = 0
       
       for record in weather_data.get_all_records():
           # Get temperature data
           max_temp_data = record.data_values.get('day-air-tmp-max')
           min_temp_data = record.data_values.get('day-air-tmp-min')
           
           if not (max_temp_data and max_temp_data.value and 
                   min_temp_data and min_temp_data.value):
               continue
           
           daily_max = float(max_temp_data.value)
           daily_min = float(min_temp_data.value)
           
           # Apply maximum temperature cap
           daily_max = min(daily_max, max_temp)
           daily_min = max(daily_min, base_temp)
           
           # Calculate daily GDD
           daily_gdd = max(0, (daily_max + daily_min) / 2 - base_temp)
           cumulative_gdd += daily_gdd
           
           gdd_data.append({
               'date': record.date,
               'daily_gdd': daily_gdd,
               'cumulative_gdd': cumulative_gdd,
               'max_temp': daily_max,
               'min_temp': daily_min
           })
       
       return gdd_data

Best Practices
--------------

API Usage Guidelines
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Good practices for API usage
   class CimisClientWrapper:
       def __init__(self, api_key, timeout=30):
           self.client = CimisClient(app_key=api_key, timeout=timeout)
           self.last_request_time = 0
           self.min_request_interval = 1  # seconds
       
       def rate_limited_request(self, request_func, *args, **kwargs):
           """Apply rate limiting to requests."""
           current_time = time.time()
           time_since_last = current_time - self.last_request_time
           
           if time_since_last < self.min_request_interval:
               time.sleep(self.min_request_interval - time_since_last)
           
           try:
               result = request_func(*args, **kwargs)
               self.last_request_time = time.time()
               return result
           except Exception as e:
               print(f"Request failed: {e}")
               raise

Data Caching
~~~~~~~~~~~~

Implement caching for better performance:

.. code-block:: python

   import pickle
   import os
   from datetime import datetime

   class CimisDataCache:
       def __init__(self, cache_dir="cimis_cache"):
           self.cache_dir = cache_dir
           os.makedirs(cache_dir, exist_ok=True)
       
       def _get_cache_key(self, targets, start_date, end_date, data_items=None):
           """Generate cache key from request parameters."""
           targets_str = "_".join(str(t) for t in sorted(targets))
           items_str = "_".join(sorted(data_items or []))
           return f"{targets_str}_{start_date}_{end_date}_{items_str}"
       
       def get(self, targets, start_date, end_date, data_items=None, max_age_hours=24):
           """Get cached data if available and fresh."""
           cache_key = self._get_cache_key(targets, start_date, end_date, data_items)
           cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
           
           if os.path.exists(cache_file):
               # Check if cache is still fresh
               file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
               if file_age.total_seconds() < max_age_hours * 3600:
                   with open(cache_file, 'rb') as f:
                       return pickle.load(f)
           
           return None
       
       def set(self, weather_data, targets, start_date, end_date, data_items=None):
           """Cache weather data."""
           cache_key = self._get_cache_key(targets, start_date, end_date, data_items)
           cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
           
           with open(cache_file, 'wb') as f:
               pickle.dump(weather_data, f)

Integration Examples
--------------------

Pandas Integration
~~~~~~~~~~~~~~~~~~

Convert CIMIS data to pandas DataFrame:

.. code-block:: python

   import pandas as pd

   def weather_data_to_dataframe(weather_data):
       """Convert CIMIS weather data to pandas DataFrame."""
       
       rows = []
       
       for record in weather_data.get_all_records():
           row = {
               'date': record.date,
               'station': record.station,
               'julian': record.julian
           }
           
           # Add all data values
           for key, value in record.data_values.items():
               row[f"{key}_value"] = value.value
               row[f"{key}_qc"] = value.qc
               row[f"{key}_unit"] = value.unit
           
           rows.append(row)
       
       df = pd.DataFrame(rows)
       df['date'] = pd.to_datetime(df['date'])
       return df

Database Integration
~~~~~~~~~~~~~~~~~~~~

Store data in SQLite database:

.. code-block:: python

   import sqlite3
   from contextlib import contextmanager

   class CimisDatabase:
       def __init__(self, db_path="cimis_data.db"):
           self.db_path = db_path
           self._create_tables()
       
       @contextmanager
       def get_connection(self):
           conn = sqlite3.connect(self.db_path)
           try:
               yield conn
           finally:
               conn.close()
       
       def _create_tables(self):
           """Create database tables."""
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS weather_data (
                       id INTEGER PRIMARY KEY,
                       date TEXT,
                       station TEXT,
                       data_item TEXT,
                       value TEXT,
                       qc TEXT,
                       unit TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
               ''')
               conn.commit()
       
       def store_weather_data(self, weather_data):
           """Store weather data in database."""
           with self.get_connection() as conn:
               for record in weather_data.get_all_records():
                   for key, value in record.data_values.items():
                       conn.execute('''
                           INSERT INTO weather_data (date, station, data_item, value, qc, unit)
                           VALUES (?, ?, ?, ?, ?, ?)
                       ''', (record.date, record.station, key, value.value, value.qc, value.unit))
               conn.commit()

Common Use Cases
----------------

Agricultural Decision Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate agricultural advisories:

.. code-block:: python

   def agricultural_advisory(client, station_id, crop_type="tomato"):
       """Generate agricultural advisory based on recent weather."""
       
       end_date = date.today() - timedelta(days=1)
       start_date = end_date - timedelta(days=7)
       
       weather_data = client.get_daily_data(
           targets=[station_id],
           start_date=start_date,
           end_date=end_date
       )
       
       # Analyze recent conditions
       temp_data, temp_stats = analyze_temperature_data(weather_data)
       gdd_data = calculate_gdd(weather_data)
       irrigation_analysis = calculate_irrigation_needs(weather_data, crop_coefficient=1.2)
       
       advisory = {
           'station': station_id,
           'period': f"{start_date} to {end_date}",
           'average_temperature': temp_stats.get('mean_temp'),
           'temperature_range': temp_stats.get('temp_range'),
           'growing_degree_days': gdd_data[-1]['cumulative_gdd'] if gdd_data else 0,
           'irrigation_recommended': len(irrigation_analysis['summary']['irrigation_events']) > 0,
           'irrigation_amount': irrigation_analysis['summary']['total_irrigation_need']
       }
       
       return advisory

This user guide provides comprehensive examples for effectively using the Python CIMIS Client library. For complete API documentation, see the :doc:`api_reference`.
