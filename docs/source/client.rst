CimisClient
===========

The main client class for interacting with the CIMIS API.

.. currentmodule:: python_cimis

.. autoclass:: CimisClient
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from python_cimis import CimisClient
   import os

   # Initialize client
   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

   # Get daily weather data
   weather_data = client.get_daily_data(
       targets=[2, 8, 127],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   # Export to CSV
   csv_file = client.export_to_csv(weather_data)

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Custom timeout and configuration
   client = CimisClient(
       app_key="your-api-key",
       timeout=60  # 60 second timeout
   )

   # Get specific data items only
   weather_data = client.get_daily_data(
       targets=[2],
       start_date="2023-06-01",
       end_date="2023-06-30",
       data_items=["day-air-tmp-avg", "day-eto", "day-precip"],
       unit_of_measure="M",  # Metric units
       prioritize_scs=True   # Prefer Spatial CIMIS System data
   )

Target Types
~~~~~~~~~~~~

The client supports multiple target types:

.. code-block:: python

   # Station numbers
   weather_data = client.get_daily_data(
       targets=[2, 8, 127],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   # Zip codes  
   weather_data = client.get_daily_data(
       targets=["95823", "94503"],
       start_date="2023-06-01", 
       end_date="2023-06-07"
   )

   # Coordinates
   weather_data = client.get_daily_data(
       targets=["lat=38.5816,lng=-121.4944"],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   # Addresses
   weather_data = client.get_daily_data(
       targets=["addr-name=Capitol,addr=1315 10th Street Sacramento, CA 95814"],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   # Mixed types
   weather_data = client.get_daily_data(
       targets=[2, "95823", "lat=38.5816,lng=-121.4944"],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError

   try:
       weather_data = client.get_daily_data(
           targets=[2],
           start_date="2023-06-01",
           end_date="2023-06-07"
       )
   except CimisAuthenticationError:
       print("Invalid API key")
   except CimisConnectionError as e:
       print(f"Connection error: {e.message}")
   except CimisAPIError as e:
       print(f"API error: {e.message} (Code: {e.error_code})")

Station Discovery
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all stations
   all_stations = client.get_stations()
   print(f"Total stations: {len(all_stations)}")

   # Get specific station
   station_2 = client.get_stations(station_number="2")
   if station_2:
       station = station_2[0]
       print(f"Station 2: {station.name} in {station.city}")

   # Find active ETo stations
   active_eto_stations = [
       s for s in all_stations 
       if s.is_active and s.is_eto_station
   ]

   # Get zip code coverage
   wsn_zips = client.get_station_zip_codes()
   scs_zips = client.get_spatial_zip_codes()

CSV Export Options
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Auto-generated filename
   csv_file = client.export_to_csv(weather_data)
   print(f"Exported to: {csv_file}")

   # Custom filename  
   client.export_to_csv(weather_data, filename="my_weather_data.csv")

   # Export station information
   stations = client.get_stations()
   station_csv = client.export_stations_to_csv(stations, filename="stations.csv")

Performance Tips
~~~~~~~~~~~~~~~~

.. code-block:: python

   # For large date ranges, split into smaller chunks
   from datetime import date, timedelta

   def get_large_dataset(client, targets, start_date, end_date, chunk_days=30):
       """Get large dataset by splitting into chunks."""
       all_records = []
       current_date = start_date
       
       while current_date <= end_date:
           chunk_end = min(current_date + timedelta(days=chunk_days), end_date)
           
           weather_data = client.get_daily_data(
               targets=targets,
               start_date=current_date,
               end_date=chunk_end
           )
           
           all_records.extend(weather_data.get_all_records())
           current_date = chunk_end + timedelta(days=1)
       
       return all_records

   # Use specific data items for faster responses
   weather_data = client.get_daily_data(
       targets=[2],
       start_date="2023-01-01",
       end_date="2023-12-31",
       data_items=["day-air-tmp-avg", "day-eto"]  # Only what you need
   )
