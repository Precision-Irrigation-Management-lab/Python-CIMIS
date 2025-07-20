API Reference
=============

Complete API reference for the Python CIMIS Client library.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------

The Python CIMIS Client provides a comprehensive interface to the California Irrigation Management Information System (CIMIS) API. The library is organized into several modules:

- :doc:`client` - Main client class for API interactions
- :doc:`models` - Data models for weather data and stations
- :doc:`exceptions` - Custom exception classes
- :doc:`utils` - Utility functions and helpers

Quick Reference
---------------

**Main Classes:**

.. code-block:: python

   from python_cimis import CimisClient
   from python_cimis.models import WeatherData, Station
   from python_cimis.exceptions import CimisAPIError

**Common Usage Pattern:**

.. code-block:: python

   client = CimisClient(app_key="your-api-key")
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   csv_file = client.export_to_csv(weather_data)

Module Documentation
--------------------

.. toctree::
   :maxdepth: 2

   client
   models
   exceptions
   utils

Type Hints
----------

The library provides comprehensive type hints for better IDE integration:

.. code-block:: python

   from typing import List, Optional, Union
   from datetime import date
   from python_cimis import CimisClient, WeatherData, Station

   def process_weather_data(
       client: CimisClient,
       stations: List[int],
       start: date,
       end: date
   ) -> Optional[str]:
       """Example function with type hints."""
       weather_data: WeatherData = client.get_daily_data(
           targets=stations,
           start_date=start,
           end_date=end
       )
       return client.export_to_csv(weather_data)

Constants
---------

Data Items
~~~~~~~~~~

**Daily Data Items:**

.. code-block:: python

   DAILY_DATA_ITEMS = [
       "day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min",
       "day-dew-pnt", "day-eto", "day-asce-eto", "day-precip",
       "day-rel-hum-avg", "day-rel-hum-max", "day-rel-hum-min",
       "day-sol-rad-avg", "day-vap-pres-avg", "day-vap-pres-max",
       "day-wind-spd-avg", "day-wind-run", "day-soil-tmp-avg",
       "day-soil-tmp-max", "day-soil-tmp-min"
   ]

**Hourly Data Items:**

.. code-block:: python

   HOURLY_DATA_ITEMS = [
       "hly-air-tmp", "hly-dew-pnt", "hly-eto", "hly-net-rad",
       "hly-asce-eto", "hly-asce-etr", "hly-precip", "hly-rel-hum",
       "hly-res-wind-dir", "hly-res-wind-spd", "hly-soil-tmp",
       "hly-sol-rad", "hly-vap-pres", "hly-wind-dir", "hly-wind-spd"
   ]

Unit Types
~~~~~~~~~~

- ``"M"`` - Metric units (default)
- ``"E"`` - English units

Provider Types
~~~~~~~~~~~~~~

- ``"WSN"`` - Weather Station Network
- ``"SCS"`` - Spatial CIMIS System

Quality Control Flags
~~~~~~~~~~~~~~~~~~~~~

- ``" "`` (space) - Measured or calculated value
- ``"Y"`` - Missing data replaced with estimated value  
- ``"M"`` - Missing data not replaced

Performance Considerations
--------------------------

Request Limits
~~~~~~~~~~~~~~

- **Daily data**: Recommend limiting to 1-2 months per request
- **Hourly data**: Recommend limiting to 7-14 days per request
- **Large date ranges**: Should be split into smaller chunks

CSV Export
~~~~~~~~~~

- Large datasets may take time to process
- Consider filtering data items for faster exports
- Auto-generated filenames prevent overwriting

Error Handling Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always wrap API calls in try-catch blocks:

.. code-block:: python

   from python_cimis.exceptions import CimisConnectionError, CimisAPIError
   import time

   def robust_request(client, *args, **kwargs):
       """Request with retry logic."""
       max_retries = 3
       
       for attempt in range(max_retries):
           try:
               return client.get_daily_data(*args, **kwargs)
           except CimisConnectionError:
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Exponential backoff
               else:
                   raise
           except CimisAPIError:
               # Don't retry API errors
               raise

Examples by Use Case
--------------------

Agricultural Applications
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Irrigation scheduling
   def calculate_irrigation_schedule(client, station_id, crop_kc=1.0):
       weather_data = client.get_daily_data(
           targets=[station_id],
           start_date=date.today() - timedelta(days=30),
           end_date=date.today() - timedelta(days=1),
           data_items=["day-eto", "day-precip"]
       )
       # Process irrigation needs...

Environmental Research
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Climate analysis
   def analyze_climate_trends(client, stations, years):
       all_data = []
       for year in years:
           weather_data = client.get_daily_data(
               targets=stations,
               start_date=f"{year}-01-01",
               end_date=f"{year}-12-31",
               data_items=["day-air-tmp-avg", "day-precip"]
           )
           all_data.extend(weather_data.get_all_records())
       # Analyze trends...

Data Science Integration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Machine learning feature engineering
   def create_weather_features(client, locations, date_range):
       weather_data = client.get_daily_data(
           targets=locations,
           start_date=date_range[0],
           end_date=date_range[1]
       )
       
       # Convert to DataFrame for ML processing
       df = weather_data_to_dataframe(weather_data)
       
       # Engineer features
       df['temp_range'] = df['day-air-tmp-max_value'] - df['day-air-tmp-min_value']
       df['growing_degree_days'] = (df['day-air-tmp-avg_value'] - 50).clip(lower=0)
       
       return df
