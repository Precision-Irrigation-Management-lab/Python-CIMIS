Data Models
===========

Data model classes for weather data, stations, and related objects.

.. currentmodule:: python_cimis.models

WeatherData
-----------

Container for weather data API responses.

.. autoclass:: WeatherData
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   # Get all records
   all_records = weather_data.get_all_records()
   print(f"Total records: {len(all_records)}")

   # Get records for specific station
   station_2_records = weather_data.get_records_by_station("2")
   print(f"Station 2 records: {len(station_2_records)}")

   # Process records
   for record in all_records:
       print(f"Date: {record.date}, Station: {record.station}")
       
       # Access temperature data
       temp_data = record.data_values.get('day-air-tmp-avg')
       if temp_data and temp_data.value:
           print(f"  Temperature: {temp_data.value}°{temp_data.unit}")

WeatherProvider
---------------

Represents a data provider (WSN or SCS).

.. autoclass:: WeatherProvider
   :members:
   :undoc-members:
   :show-inheritance:

WeatherRecord
-------------

Individual weather data record.

.. autoclass:: WeatherRecord
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   for record in weather_data.get_all_records():
       print(f"Date: {record.date}")
       print(f"Station: {record.station}")
       print(f"Julian day: {record.julian}")
       
       # Check if this is hourly data
       if hasattr(record, 'hour') and record.hour:
           print(f"Hour: {record.hour}")
       
       # Access data values
       for key, value in record.data_values.items():
           if value.value:  # Only show non-empty values
               print(f"  {key}: {value.value} {value.unit} (QC: {value.qc})")

DataValue
---------

Individual data point with quality control information.

.. autoclass:: DataValue
   :members:
   :undoc-members:
   :show-inheritance:

Quality Control Flags
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Check data quality
   temp_data = record.data_values.get('day-air-tmp-avg')
   
   if temp_data.qc == ' ':  # Space character
       print("Measured or calculated value")
   elif temp_data.qc == 'Y':
       print("Missing data replaced with estimated value")
   elif temp_data.qc == 'M':
       print("Missing data not replaced")

Station
-------

Weather station information.

.. autoclass:: Station
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   stations = client.get_stations()
   
   for station in stations:
       print(f"Station {station.station_nbr}: {station.name}")
       print(f"  Location: {station.city}, {station.county}")
       print(f"  Active: {station.is_active}")
       print(f"  ETo Station: {station.is_eto_station}")
       print(f"  Elevation: {station.elevation}")
       print(f"  Connected: {station.connect_date}")
       
       if station.disconnect_date:
           print(f"  Disconnected: {station.disconnect_date}")

Station Filtering
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find active stations
   active_stations = [s for s in stations if s.is_active]
   
   # Find ETo stations
   eto_stations = [s for s in stations if s.is_eto_station]
   
   # Find stations in specific county
   fresno_stations = [s for s in stations if s.county.lower() == 'fresno']
   
   # Find stations by elevation
   high_elevation = [s for s in stations if float(s.elevation) > 1000]

ZipCode
-------

WSN station zip code information.

.. autoclass:: ZipCode
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   zip_codes = client.get_station_zip_codes()
   
   for zip_code in zip_codes:
       print(f"Zip: {zip_code.zip_code} -> Station: {zip_code.station_nbr}")
   
   # Find station for specific zip code
   target_zip = "95823"
   matching_stations = [zc.station_nbr for zc in zip_codes if zc.zip_code == target_zip]

SpatialZipCode
--------------

Spatial CIMIS System zip code information.

.. autoclass:: SpatialZipCode
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   spatial_zips = client.get_spatial_zip_codes()
   
   for zip_code in spatial_zips:
       print(f"Zip: {zip_code.zip_code}")
       print(f"  City: {zip_code.city}")
       print(f"  County: {zip_code.county}")
   
   # Find zip codes in specific county
   sac_county_zips = [sz for sz in spatial_zips if sz.county.lower() == 'sacramento']

Data Access Patterns
--------------------

Accessing Weather Values
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def extract_temperature_data(weather_data):
       """Extract temperature data from weather records."""
       temperatures = []
       
       for record in weather_data.get_all_records():
           temp_data = record.data_values.get('day-air-tmp-avg')
           
           if temp_data and temp_data.value and temp_data.qc != 'M':
               temperatures.append({
                   'date': record.date,
                   'station': record.station,
                   'temperature': float(temp_data.value),
                   'unit': temp_data.unit,
                   'quality': temp_data.qc
               })
       
       return temperatures

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_data_quality(weather_data, max_missing_percent=10):
       """Validate data quality in weather records."""
       total_values = 0
       missing_values = 0
       estimated_values = 0
       
       for record in weather_data.get_all_records():
           for key, value in record.data_values.items():
               total_values += 1
               
               if value.qc == 'M':
                   missing_values += 1
               elif value.qc == 'Y':
                   estimated_values += 1
       
       missing_percent = (missing_values / total_values) * 100
       estimated_percent = (estimated_values / total_values) * 100
       
       quality_report = {
           'total_values': total_values,
           'missing_count': missing_values,
           'missing_percent': missing_percent,
           'estimated_count': estimated_values,
           'estimated_percent': estimated_percent,
           'quality_acceptable': missing_percent <= max_missing_percent
       }
       
       return quality_report

Converting to Other Formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def weather_data_to_dict(weather_data):
       """Convert weather data to dictionary format."""
       result = []
       
       for record in weather_data.get_all_records():
           record_dict = {
               'date': record.date,
               'station': record.station,
               'julian': record.julian,
               'data': {}
           }
           
           # Add hour for hourly data
           if hasattr(record, 'hour') and record.hour:
               record_dict['hour'] = record.hour
           
           # Add all data values
           for key, value in record.data_values.items():
               record_dict['data'][key] = {
                   'value': value.value,
                   'qc': value.qc,
                   'unit': value.unit
               }
           
           result.append(record_dict)
       
       return result

   def weather_data_to_json(weather_data, filename=None):
       """Convert weather data to JSON format."""
       import json
       
       data_dict = weather_data_to_dict(weather_data)
       
       if filename:
           with open(filename, 'w') as f:
               json.dump(data_dict, f, indent=2)
           return filename
       else:
           return json.dumps(data_dict, indent=2)

Data Processing Helpers
-----------------------

Statistical Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculate_statistics(weather_data, data_item):
       """Calculate basic statistics for a data item."""
       values = []
       
       for record in weather_data.get_all_records():
           data_value = record.data_values.get(data_item)
           
           if data_value and data_value.value and data_value.qc != 'M':
               try:
                   values.append(float(data_value.value))
               except ValueError:
                   continue
       
       if not values:
           return None
       
       return {
           'count': len(values),
           'mean': sum(values) / len(values),
           'min': min(values),
           'max': max(values),
           'range': max(values) - min(values)
       }

   # Usage
   temp_stats = calculate_statistics(weather_data, 'day-air-tmp-avg')
   eto_stats = calculate_statistics(weather_data, 'day-eto')

Time Series Processing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_time_series(weather_data, data_items):
       """Create time series data for specified items."""
       from datetime import datetime
       
       time_series = {}
       
       for item in data_items:
           time_series[item] = {
               'dates': [],
               'values': [],
               'units': None
           }
       
       for record in weather_data.get_all_records():
           record_date = datetime.strptime(record.date, '%Y-%m-%d').date()
           
           for item in data_items:
               data_value = record.data_values.get(item)
               
               if data_value and data_value.value and data_value.qc != 'M':
                   try:
                       value = float(data_value.value)
                       time_series[item]['dates'].append(record_date)
                       time_series[item]['values'].append(value)
                       
                       if not time_series[item]['units']:
                           time_series[item]['units'] = data_value.unit
                           
                   except ValueError:
                       continue
       
       return time_series
