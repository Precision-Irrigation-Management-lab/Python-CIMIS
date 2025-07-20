Utilities
=========

Utility functions and helper classes for the Python CIMIS Client.

.. currentmodule:: python_cimis.utils

FilenameGenerator
-----------------

Utility class for generating intelligent CSV filenames.

.. autoclass:: FilenameGenerator
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.utils import FilenameGenerator

   # Generate filename from weather data
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   filename = FilenameGenerator.generate(weather_data)
   print(filename)  # Output: "Station2_FivePoints_20230601_to_20230607.csv"

   # Multiple stations
   weather_data = client.get_daily_data(targets=[2, 8, 127], start_date="2023-06-01", end_date="2023-06-07")
   filename = FilenameGenerator.generate(weather_data)
   print(filename)  # Output: "MultiStation_20230601_to_20230607.csv"

Filename Patterns
~~~~~~~~~~~~~~~~~

The ``FilenameGenerator`` creates filenames using these patterns:

**Single Station:**
``Station{number}_{name}_{start_date}_to_{end_date}.csv``

**Multiple Stations:**
``MultiStation_{start_date}_to_{end_date}.csv``

**Date Format:**
``YYYYMMDD`` (e.g., ``20230601``)

Examples:

.. code-block:: text

   Station2_FivePoints_20230601_to_20230607.csv
   Station127_Fresno_20230101_to_20231231.csv
   MultiStation_20230601_to_20230607.csv

Helper Functions
----------------

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_date_range(start_date, end_date, max_days=365):
       """Validate date range for API requests."""
       from datetime import datetime, timedelta
       
       # Convert strings to date objects if needed
       if isinstance(start_date, str):
           start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
       if isinstance(end_date, str):
           end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
       
       # Validate range
       if start_date > end_date:
           raise ValueError("Start date must be before end date")
       
       date_diff = (end_date - start_date).days
       if date_diff > max_days:
           raise ValueError(f"Date range too large: {date_diff} days (max: {max_days})")
       
       return True

   def validate_targets(targets):
       """Validate target list for API requests."""
       if not targets:
           raise ValueError("At least one target must be specified")
       
       valid_targets = []
       for target in targets:
           if isinstance(target, int):
               # Station number
               if target < 1 or target > 999:
                   raise ValueError(f"Invalid station number: {target}")
               valid_targets.append(str(target))
           elif isinstance(target, str):
               # Zip code, coordinates, or address
               valid_targets.append(target)
           else:
               raise ValueError(f"Invalid target type: {type(target)}")
       
       return valid_targets

Data Conversion
~~~~~~~~~~~~~~~

.. code-block:: python

   def convert_units(value, from_unit, to_unit):
       """Convert between different units."""
       conversions = {
           # Temperature conversions
           ('C', 'F'): lambda x: x * 9/5 + 32,
           ('F', 'C'): lambda x: (x - 32) * 5/9,
           
           # Length conversions
           ('mm', 'in'): lambda x: x * 0.0393701,
           ('in', 'mm'): lambda x: x * 25.4,
           ('m', 'ft'): lambda x: x * 3.28084,
           ('ft', 'm'): lambda x: x * 0.3048,
           
           # Speed conversions
           ('m/s', 'mph'): lambda x: x * 2.23694,
           ('mph', 'm/s'): lambda x: x * 0.44704,
           ('km/h', 'mph'): lambda x: x * 0.621371,
           ('mph', 'km/h'): lambda x: x * 1.60934,
       }
       
       conversion_key = (from_unit, to_unit)
       if conversion_key in conversions:
           return conversions[conversion_key](float(value))
       else:
           raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")

   def celsius_to_fahrenheit(celsius):
       """Convert Celsius to Fahrenheit."""
       return celsius * 9/5 + 32

   def fahrenheit_to_celsius(fahrenheit):
       """Convert Fahrenheit to Celsius."""
       return (fahrenheit - 32) * 5/9

   def mm_to_inches(mm):
       """Convert millimeters to inches."""
       return mm * 0.0393701

   def inches_to_mm(inches):
       """Convert inches to millimeters."""
       return inches * 25.4

Data Processing
~~~~~~~~~~~~~~~

.. code-block:: python

   def extract_data_item(weather_data, data_item, include_qc=False):
       """Extract a specific data item from weather data."""
       extracted_data = []
       
       for record in weather_data.get_all_records():
           data_value = record.data_values.get(data_item)
           
           if data_value and data_value.value:
               entry = {
                   'date': record.date,
                   'station': record.station,
                   'value': data_value.value,
                   'unit': data_value.unit
               }
               
               if include_qc:
                   entry['qc'] = data_value.qc
               
               extracted_data.append(entry)
       
       return extracted_data

   def aggregate_by_station(weather_data, aggregation_func='mean'):
       """Aggregate weather data by station."""
       from collections import defaultdict
       
       station_data = defaultdict(list)
       
       # Group data by station
       for record in weather_data.get_all_records():
           station_data[record.station].append(record)
       
       aggregated = {}
       
       for station, records in station_data.items():
           aggregated[station] = {
               'record_count': len(records),
               'date_range': {
                   'start': min(r.date for r in records),
                   'end': max(r.date for r in records)
               },
               'data_items': {}
           }
           
           # Aggregate each data item
           data_items = set()
           for record in records:
               data_items.update(record.data_values.keys())
           
           for item in data_items:
               values = []
               for record in records:
                   data_value = record.data_values.get(item)
                   if data_value and data_value.value and data_value.qc != 'M':
                       try:
                           values.append(float(data_value.value))
                       except ValueError:
                           continue
               
               if values:
                   if aggregation_func == 'mean':
                       result = sum(values) / len(values)
                   elif aggregation_func == 'sum':
                       result = sum(values)
                   elif aggregation_func == 'min':
                       result = min(values)
                   elif aggregation_func == 'max':
                       result = max(values)
                   else:
                       result = values
                   
                   aggregated[station]['data_items'][item] = {
                       'value': result,
                       'count': len(values),
                       'unit': records[0].data_values[item].unit if records[0].data_values.get(item) else None
                   }
       
       return aggregated

Cache Management
~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   import pickle
   import json
   from datetime import datetime, timedelta

   class CacheManager:
       """Simple cache manager for CIMIS data."""
       
       def __init__(self, cache_dir="cimis_cache", max_age_hours=24):
           self.cache_dir = cache_dir
           self.max_age_hours = max_age_hours
           os.makedirs(cache_dir, exist_ok=True)
       
       def _get_cache_path(self, cache_key, format='pickle'):
           """Get the cache file path."""
           extension = 'pkl' if format == 'pickle' else 'json'
           return os.path.join(self.cache_dir, f"{cache_key}.{extension}")
       
       def _generate_key(self, **params):
           """Generate cache key from parameters."""
           sorted_params = sorted(params.items())
           key_parts = []
           for k, v in sorted_params:
               if isinstance(v, list):
                   v = '_'.join(str(x) for x in sorted(v))
               key_parts.append(f"{k}_{v}")
           return '_'.join(key_parts)
       
       def get(self, **params):
           """Get cached data."""
           cache_key = self._generate_key(**params)
           cache_path = self._get_cache_path(cache_key)
           
           if os.path.exists(cache_path):
               # Check if cache is still fresh
               file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
               if datetime.now() - file_time < timedelta(hours=self.max_age_hours):
                   try:
                       with open(cache_path, 'rb') as f:
                           return pickle.load(f)
                   except Exception:
                       # Remove corrupted cache file
                       os.remove(cache_path)
           
           return None
       
       def set(self, data, **params):
           """Set cached data."""
           cache_key = self._generate_key(**params)
           cache_path = self._get_cache_path(cache_key)
           
           try:
               with open(cache_path, 'wb') as f:
                   pickle.dump(data, f)
           except Exception as e:
               print(f"Warning: Could not cache data: {e}")
       
       def clear_expired(self):
           """Clear expired cache files."""
           if not os.path.exists(self.cache_dir):
               return
           
           cutoff_time = datetime.now() - timedelta(hours=self.max_age_hours)
           
           for filename in os.listdir(self.cache_dir):
               file_path = os.path.join(self.cache_dir, filename)
               file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
               
               if file_time < cutoff_time:
                   try:
                       os.remove(file_path)
                   except Exception:
                       pass
       
       def clear_all(self):
           """Clear all cache files."""
           if not os.path.exists(self.cache_dir):
               return
           
           for filename in os.listdir(self.cache_dir):
               file_path = os.path.join(self.cache_dir, filename)
               try:
                   os.remove(file_path)
               except Exception:
                   pass

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   import os
   from typing import Dict, Any, Optional

   class ConfigManager:
       """Configuration manager for CIMIS client settings."""
       
       def __init__(self, config_file: str = "cimis_config.json"):
           self.config_file = config_file
           self.config = self._load_config()
       
       def _load_config(self) -> Dict[str, Any]:
           """Load configuration from file."""
           if os.path.exists(self.config_file):
               try:
                   with open(self.config_file, 'r') as f:
                       return json.load(f)
               except Exception:
                   pass
           
           # Return default configuration
           return {
               'api_key': os.getenv('CIMIS_API_KEY'),
               'timeout': 30,
               'max_retries': 3,
               'cache_enabled': True,
               'cache_max_age_hours': 24,
               'default_unit_of_measure': 'M',
               'default_prioritize_scs': False
           }
       
       def save_config(self):
           """Save configuration to file."""
           try:
               with open(self.config_file, 'w') as f:
                   json.dump(self.config, f, indent=2)
           except Exception as e:
               print(f"Warning: Could not save configuration: {e}")
       
       def get(self, key: str, default: Any = None) -> Any:
           """Get configuration value."""
           return self.config.get(key, default)
       
       def set(self, key: str, value: Any):
           """Set configuration value."""
           self.config[key] = value
       
       def update(self, **kwargs):
           """Update multiple configuration values."""
           self.config.update(kwargs)

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date, timedelta
   from typing import List, Generator, Tuple
   import time

   def split_date_range(start_date: date, end_date: date, chunk_days: int = 30) -> Generator[Tuple[date, date], None, None]:
       """Split a date range into smaller chunks."""
       current_date = start_date
       
       while current_date <= end_date:
           chunk_end = min(current_date + timedelta(days=chunk_days), end_date)
           yield current_date, chunk_end
           current_date = chunk_end + timedelta(days=1)

   def split_target_list(targets: List, batch_size: int = 10) -> Generator[List, None, None]:
       """Split a target list into smaller batches."""
       for i in range(0, len(targets), batch_size):
           yield targets[i:i + batch_size]

   def batch_process_with_rate_limit(
       client, 
       targets: List,
       start_date: date,
       end_date: date,
       batch_size: int = 10,
       chunk_days: int = 30,
       delay_seconds: float = 1.0
   ):
       """Process large requests in batches with rate limiting."""
       all_records = []
       
       # Split targets into batches
       for target_batch in split_target_list(targets, batch_size):
           # Split date range into chunks
           for chunk_start, chunk_end in split_date_range(start_date, end_date, chunk_days):
               try:
                   weather_data = client.get_daily_data(
                       targets=target_batch,
                       start_date=chunk_start,
                       end_date=chunk_end
                   )
                   
                   all_records.extend(weather_data.get_all_records())
                   
                   # Rate limiting
                   time.sleep(delay_seconds)
                   
               except Exception as e:
                   print(f"Error processing batch {target_batch} for {chunk_start} to {chunk_end}: {e}")
                   continue
       
       return all_records

Quality Control
~~~~~~~~~~~~~~~

.. code-block:: python

   def assess_data_quality(weather_data, quality_threshold=0.8):
       """Assess the quality of weather data."""
       total_points = 0
       good_points = 0
       missing_points = 0
       estimated_points = 0
       
       quality_by_item = {}
       
       for record in weather_data.get_all_records():
           for item, value in record.data_values.items():
               total_points += 1
               
               if item not in quality_by_item:
                   quality_by_item[item] = {'total': 0, 'good': 0, 'missing': 0, 'estimated': 0}
               
               quality_by_item[item]['total'] += 1
               
               if value.qc == ' ':  # Good data
                   good_points += 1
                   quality_by_item[item]['good'] += 1
               elif value.qc == 'M':  # Missing
                   missing_points += 1
                   quality_by_item[item]['missing'] += 1
               elif value.qc == 'Y':  # Estimated
                   estimated_points += 1
                   quality_by_item[item]['estimated'] += 1
       
       overall_quality = good_points / total_points if total_points > 0 else 0
       
       # Calculate quality percentage for each data item
       for item in quality_by_item:
           item_total = quality_by_item[item]['total']
           quality_by_item[item]['quality_percentage'] = (
               quality_by_item[item]['good'] / item_total * 100 if item_total > 0 else 0
           )
       
       quality_report = {
           'overall_quality_percentage': overall_quality * 100,
           'meets_threshold': overall_quality >= quality_threshold,
           'total_data_points': total_points,
           'good_data_points': good_points,
           'missing_data_points': missing_points,
           'estimated_data_points': estimated_points,
           'quality_by_item': quality_by_item
       }
       
       return quality_report

   def filter_by_quality(weather_data, min_quality='good'):
       """Filter weather data by quality level."""
       quality_levels = {
           'good': [' '],           # Only measured/calculated
           'acceptable': [' ', 'Y'], # Measured/calculated + estimated
           'all': [' ', 'Y', 'M']   # Include missing data
       }
       
       allowed_qc_flags = quality_levels.get(min_quality, [' '])
       
       filtered_records = []
       
       for record in weather_data.get_all_records():
           # Check if record has any data meeting quality criteria
           has_good_data = False
           
           for item, value in record.data_values.items():
               if value.qc in allowed_qc_flags and value.value:
                   has_good_data = True
                   break
           
           if has_good_data:
               filtered_records.append(record)
       
       return filtered_records

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from contextlib import contextmanager

   @contextmanager
   def measure_time(operation_name="Operation"):
       """Context manager to measure execution time."""
       start_time = time.time()
       try:
           yield
       finally:
           end_time = time.time()
           duration = end_time - start_time
           print(f"{operation_name} took {duration:.2f} seconds")

   def benchmark_api_call(client, **kwargs):
       """Benchmark an API call."""
       with measure_time("API call"):
           result = client.get_daily_data(**kwargs)
       
       record_count = len(result.get_all_records())
       print(f"Retrieved {record_count} records")
       
       return result

Usage Examples
--------------

Complete Utility Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis import CimisClient
   from python_cimis.utils import FilenameGenerator
   import os

   # Initialize client with configuration
   config = ConfigManager()
   client = CimisClient(
       app_key=config.get('api_key'),
       timeout=config.get('timeout', 30)
   )

   # Setup caching
   cache = CacheManager(max_age_hours=config.get('cache_max_age_hours', 24))

   # Get data with caching
   cache_params = {
       'targets': [2, 8],
       'start_date': '2023-06-01',
       'end_date': '2023-06-07'
   }

   weather_data = cache.get(**cache_params)
   if not weather_data:
       print("Cache miss - fetching from API")
       with measure_time("Data retrieval"):
           weather_data = client.get_daily_data(**cache_params)
       cache.set(weather_data, **cache_params)
   else:
       print("Cache hit - using cached data")

   # Assess data quality
   quality_report = assess_data_quality(weather_data)
   print(f"Data quality: {quality_report['overall_quality_percentage']:.1f}%")

   # Generate filename and export
   filename = FilenameGenerator.generate(weather_data)
   csv_file = client.export_to_csv(weather_data, filename=filename)
   print(f"Exported to: {csv_file}")

This utilities module provides essential helper functions for working efficiently with the Python CIMIS Client library.
