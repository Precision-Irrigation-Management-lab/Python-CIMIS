Quick Start Guide
=================

This guide will get you started with the Python CIMIS Client in just a few minutes.

Prerequisites
-------------

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed
2. **CIMIS API key** (get one from `CIMIS REST API page <https://et.water.ca.gov/Rest/Index>`_)
3. **Library installed**: ``pip install python-CIMIS``

Basic Usage
-----------

1. Import and Initialize
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis import CimisClient
   import os

   # Initialize client with your API key
   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

2. Get Weather Data
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import date, timedelta

   # Get daily data for the last week
   end_date = date.today() - timedelta(days=1)  # Yesterday
   start_date = end_date - timedelta(days=6)    # Week ago

   weather_data = client.get_daily_data(
       targets=[2],  # Five Points station
       start_date=start_date,
       end_date=end_date
   )

   print(f"Retrieved {len(weather_data.get_all_records())} records")

3. Export to CSV
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Export with auto-generated filename
   csv_file = client.export_to_csv(weather_data)
   print(f"Exported to: {csv_file}")

   # Or with custom filename
   client.export_to_csv(weather_data, filename="my_weather_data.csv")

Complete Example
----------------

Here's a complete working example:

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete example: Get weather data and export to CSV
   """

   import os
   from datetime import date, timedelta
   from python_cimis import CimisClient

   def main():
       # Initialize client
       client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))
       
       # Define date range (last 7 days)
       end_date = date.today() - timedelta(days=1)
       start_date = end_date - timedelta(days=6)
       
       # Get weather data for multiple stations
       weather_data = client.get_daily_data(
           targets=[2, 8, 127],  # Multiple stations
           start_date=start_date,
           end_date=end_date,
           data_items=[
               "day-air-tmp-avg",  # Average temperature
               "day-eto",          # Reference ET
               "day-precip"        # Precipitation
           ]
       )
       
       # Process the data
       records = weather_data.get_all_records()
       print(f"Retrieved {len(records)} records")
       
       # Show sample data
       if records:
           record = records[0]
           print(f"\\nSample record for {record.date}:")
           print(f"  Station: {record.station}")
           
           # Display weather values
           for key, value in record.data_values.items():
               if value.value:  # Only show non-empty values
                   print(f"  {key}: {value.value} {value.unit}")
       
       # Export to CSV
       csv_file = client.export_to_csv(weather_data)
       print(f"\\nData exported to: {csv_file}")

   if __name__ == "__main__":
       main()

Common Usage Patterns
----------------------

Multiple Target Types
~~~~~~~~~~~~~~~~~~~~~~

You can request data using different target types:

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

   # Mixed types
   weather_data = client.get_daily_data(
       targets=[2, "95823", "lat=38.5816,lng=-121.4944"],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

Hourly Data
~~~~~~~~~~~

Get hourly data from Weather Station Network (WSN) stations:

.. code-block:: python

   # Get hourly data (WSN stations only)
   hourly_data = client.get_hourly_data(
       targets=[2, 8],
       start_date="2023-06-01",
       end_date="2023-06-01",  # Single day for hourly
       data_items=["hly-air-tmp", "hly-rel-hum", "hly-eto"]
   )

Station Information
~~~~~~~~~~~~~~~~~~~

Discover available weather stations:

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
   print(f"Active ETo stations: {len(active_eto_stations)}")

Error Handling
~~~~~~~~~~~~~~

Always include error handling for robust applications:

.. code-block:: python

   from python_cimis.exceptions import (
       CimisAPIError, 
       CimisConnectionError, 
       CimisAuthenticationError
   )

   try:
       weather_data = client.get_daily_data(
           targets=[2],
           start_date="2023-06-01",
           end_date="2023-06-07"
       )
       print("Success!")
       
   except CimisAuthenticationError:
       print("Error: Invalid API key")
       
   except CimisConnectionError as e:
       print(f"Connection error: {e.message}")
       
   except CimisAPIError as e:
       print(f"API error: {e.message} (Code: {e.error_code})")

Data Processing
---------------

Access Individual Records
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all records
   records = weather_data.get_all_records()

   # Process each record
   for record in records:
       print(f"Date: {record.date}, Station: {record.station}")
       
       # Access specific data items
       temp_data = record.data_values.get('day-air-tmp-avg')
       if temp_data and temp_data.value:
           print(f"  Temperature: {temp_data.value}°{temp_data.unit}")
           
       # Check quality control
       if temp_data.qc == 'M':
           print("  Warning: Missing data")
       elif temp_data.qc == 'Y':
           print("  Note: Estimated value")

Filter by Station
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get records for a specific station
   station_2_records = weather_data.get_records_by_station("2")
   print(f"Station 2 has {len(station_2_records)} records")

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_weather_data(weather_data):
       """Basic validation of weather data."""
       records = weather_data.get_all_records()
       
       if not records:
           print("Warning: No data records found")
           return False
           
       missing_count = 0
       for record in records:
           for key, value in record.data_values.items():
               if value.qc == 'M':  # Missing data
                   missing_count += 1
       
       if missing_count > 0:
           print(f"Warning: {missing_count} missing data points")
       
       print(f"Validation complete: {len(records)} records")
       return True

   # Use validation
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   validate_weather_data(weather_data)

Best Practices
--------------

1. **Use Environment Variables** for API keys (never hardcode them)
2. **Handle Exceptions** gracefully for robust applications
3. **Validate Data** before processing for critical applications
4. **Limit Date Ranges** for large requests (1-2 months for daily, 7-14 days for hourly)
5. **Cache Results** for repeated requests to improve performance
6. **Check QC Flags** when data quality is important

Next Steps
----------

Now that you know the basics, explore:

- :doc:`user_guide` - Comprehensive usage guide with advanced features
- :doc:`api_reference` - Complete API documentation
- :doc:`examples` - Real-world examples and use cases
- `GitHub Examples <https://github.com/python-cimis/python-cimis-client/tree/main/examples>`_ - Working code samples

Happy coding! 🌾💧📊
