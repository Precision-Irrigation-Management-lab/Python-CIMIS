Examples
========

Practical examples and use cases for the Python CIMIS Client library.

.. contents:: Table of Contents
   :local:
   :depth: 2

Basic Examples
--------------

Getting Started
~~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis import CimisClient
   from datetime import date, timedelta
   import os

   # Initialize client
   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

   # Get weather data for the last week
   end_date = date.today() - timedelta(days=1)
   start_date = end_date - timedelta(days=6)

   weather_data = client.get_daily_data(
       targets=[2],  # Five Points station
       start_date=start_date,
       end_date=end_date
   )

   # Display basic information
   records = weather_data.get_all_records()
   print(f"Retrieved {len(records)} records")

   for record in records:
       print(f"Date: {record.date}, Station: {record.station}")
       
       # Show temperature if available
       temp = record.data_values.get('day-air-tmp-avg')
       if temp and temp.value:
           print(f"  Average Temperature: {temp.value}°{temp.unit}")

Multiple Stations
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get data from multiple stations
   weather_data = client.get_daily_data(
       targets=[2, 8, 127],  # Five Points, Parlier, Fresno
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   # Group records by station
   station_records = {}
   for record in weather_data.get_all_records():
       if record.station not in station_records:
           station_records[record.station] = []
       station_records[record.station].append(record)

   # Display summary for each station
   for station, records in station_records.items():
       print(f"\\nStation {station}: {len(records)} records")
       
       # Calculate average temperature
       temps = []
       for record in records:
           temp = record.data_values.get('day-air-tmp-avg')
           if temp and temp.value:
               temps.append(float(temp.value))
       
       if temps:
           avg_temp = sum(temps) / len(temps)
           print(f"  Average Temperature: {avg_temp:.1f}°C")

Different Target Types
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Mix different target types
   weather_data = client.get_daily_data(
       targets=[
           2,                                      # Station number
           "95823",                               # Zip code
           "lat=38.5816,lng=-121.4944",          # Coordinates
       ],
       start_date="2023-06-01",
       end_date="2023-06-07"
   )

   print(f"Retrieved data for {len(weather_data.get_all_records())} records")

Specific Data Items
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Request only specific weather variables
   weather_data = client.get_daily_data(
       targets=[2],
       start_date="2023-06-01",
       end_date="2023-06-30",
       data_items=[
           "day-air-tmp-avg",    # Average temperature
           "day-eto",            # Reference ET
           "day-precip"          # Precipitation
       ]
   )

   for record in weather_data.get_all_records():
       print(f"Date: {record.date}")
       
       for item in ["day-air-tmp-avg", "day-eto", "day-precip"]:
           data_value = record.data_values.get(item)
           if data_value and data_value.value:
               print(f"  {item}: {data_value.value} {data_value.unit}")

Agricultural Examples
---------------------

Irrigation Scheduling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculate_irrigation_schedule(client, station_id, crop_kc=1.0, soil_capacity=2.0):
       """Calculate irrigation schedule based on ET and precipitation."""
       
       # Get recent weather data
       end_date = date.today() - timedelta(days=1)
       start_date = end_date - timedelta(days=30)
       
       weather_data = client.get_daily_data(
           targets=[station_id],
           start_date=start_date,
           end_date=end_date,
           data_items=["day-eto", "day-precip"]
       )
       
       irrigation_schedule = []
       soil_moisture_deficit = 0
       
       for record in weather_data.get_all_records():
           # Get ET and precipitation
           eto_data = record.data_values.get('day-eto')
           precip_data = record.data_values.get('day-precip')
           
           if not (eto_data and eto_data.value):
               continue
           
           eto = float(eto_data.value)
           precip = float(precip_data.value) if precip_data and precip_data.value else 0
           
           # Calculate crop water use
           etc = eto * crop_kc
           
           # Update soil moisture deficit
           soil_moisture_deficit += etc - precip
           soil_moisture_deficit = max(0, soil_moisture_deficit)  # Can't be negative
           
           # Determine if irrigation is needed
           if soil_moisture_deficit >= soil_capacity * 0.5:  # Irrigate at 50% depletion
               irrigation_amount = soil_moisture_deficit
               soil_moisture_deficit = 0  # Reset after irrigation
               
               irrigation_schedule.append({
                   'date': record.date,
                   'irrigation_amount': irrigation_amount,
                   'etc': etc,
                   'precipitation': precip
               })
       
       return irrigation_schedule

   # Usage
   schedule = calculate_irrigation_schedule(client, station_id=2, crop_kc=1.2)
   
   print("Irrigation Schedule:")
   for event in schedule:
       print(f"Date: {event['date']}")
       print(f"  Irrigation needed: {event['irrigation_amount']:.2f} inches")
       print(f"  Crop ET: {event['etc']:.2f} inches")
       print(f"  Precipitation: {event['precipitation']:.2f} inches")

Growing Degree Days
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def calculate_gdd(client, station_id, base_temp=50, max_temp=86, start_date=None):
       """Calculate Growing Degree Days for crop development."""
       
       if not start_date:
           start_date = date(date.today().year, 4, 1)  # April 1st
       
       end_date = date.today() - timedelta(days=1)
       
       weather_data = client.get_daily_data(
           targets=[station_id],
           start_date=start_date,
           end_date=end_date,
           data_items=["day-air-tmp-max", "day-air-tmp-min"]
       )
       
       gdd_data = []
       cumulative_gdd = 0
       
       for record in weather_data.get_all_records():
           max_temp_data = record.data_values.get('day-air-tmp-max')
           min_temp_data = record.data_values.get('day-air-tmp-min')
           
           if not (max_temp_data and max_temp_data.value and 
                   min_temp_data and min_temp_data.value):
               continue
           
           daily_max = float(max_temp_data.value)
           daily_min = float(min_temp_data.value)
           
           # Convert to Fahrenheit if needed
           if max_temp_data.unit == 'C':
               daily_max = daily_max * 9/5 + 32
               daily_min = daily_min * 9/5 + 32
           
           # Apply temperature caps
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

   # Usage
   gdd_data = calculate_gdd(client, station_id=2, base_temp=50)
   
   if gdd_data:
       print(f"Growing Degree Days from {gdd_data[0]['date']} to {gdd_data[-1]['date']}:")
       print(f"Total GDD: {gdd_data[-1]['cumulative_gdd']:.1f}")
       
       # Show recent daily values
       for day in gdd_data[-7:]:  # Last 7 days
           print(f"  {day['date']}: {day['daily_gdd']:.1f} GDD (Total: {day['cumulative_gdd']:.1f})")

Frost Protection
~~~~~~~~~~~~~~~~

.. code-block:: python

   def frost_alert_system(client, station_ids, frost_threshold=32):
       """Monitor stations for frost conditions."""
       
       # Get recent and forecast data
       end_date = date.today()
       start_date = end_date - timedelta(days=2)
       
       weather_data = client.get_daily_data(
           targets=station_ids,
           start_date=start_date,
           end_date=end_date,
           data_items=["day-air-tmp-min"]
       )
       
       frost_alerts = []
       
       for record in weather_data.get_all_records():
           min_temp_data = record.data_values.get('day-air-tmp-min')
           
           if min_temp_data and min_temp_data.value:
               min_temp = float(min_temp_data.value)
               
               # Convert to Fahrenheit if needed
               if min_temp_data.unit == 'C':
                   min_temp = min_temp * 9/5 + 32
               
               if min_temp <= frost_threshold:
                   frost_alerts.append({
                       'date': record.date,
                       'station': record.station,
                       'min_temperature': min_temp,
                       'severity': 'Hard Frost' if min_temp <= 28 else 'Light Frost'
                   })
       
       return frost_alerts

   # Usage
   frost_alerts = frost_alert_system(client, station_ids=[2, 8, 127])
   
   if frost_alerts:
       print("🌡️ FROST ALERTS:")
       for alert in frost_alerts:
           print(f"  {alert['date']} - Station {alert['station']}")
           print(f"    Min Temp: {alert['min_temperature']:.1f}°F ({alert['severity']})")
   else:
       print("✅ No frost conditions detected")

Data Analysis Examples
----------------------

Climate Trends
~~~~~~~~~~~~~~

.. code-block:: python

   def analyze_temperature_trends(client, station_id, years):
       """Analyze temperature trends over multiple years."""
       import statistics
       
       yearly_data = {}
       
       for year in years:
           weather_data = client.get_daily_data(
               targets=[station_id],
               start_date=f"{year}-01-01",
               end_date=f"{year}-12-31",
               data_items=["day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min"]
           )
           
           temps = {'avg': [], 'max': [], 'min': []}
           
           for record in weather_data.get_all_records():
               for temp_type in temps.keys():
                   temp_data = record.data_values.get(f'day-air-tmp-{temp_type}')
                   if temp_data and temp_data.value:
                       temps[temp_type].append(float(temp_data.value))
           
           yearly_data[year] = {
               'avg_temp': statistics.mean(temps['avg']) if temps['avg'] else None,
               'max_temp': max(temps['max']) if temps['max'] else None,
               'min_temp': min(temps['min']) if temps['min'] else None,
               'days_with_data': len(temps['avg'])
           }
       
       return yearly_data

   # Usage
   trends = analyze_temperature_trends(client, station_id=2, years=[2020, 2021, 2022, 2023])
   
   print("Temperature Trends Analysis:")
   for year, data in trends.items():
       if data['avg_temp']:
           print(f"{year}: Avg={data['avg_temp']:.1f}°C, Max={data['max_temp']:.1f}°C, Min={data['min_temp']:.1f}°C")

Water Balance Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def water_balance_analysis(client, station_id, start_date, end_date):
       """Perform water balance analysis."""
       
       weather_data = client.get_daily_data(
           targets=[station_id],
           start_date=start_date,
           end_date=end_date,
           data_items=["day-eto", "day-precip"]
       )
       
       daily_balance = []
       cumulative_deficit = 0
       total_eto = 0
       total_precip = 0
       
       for record in weather_data.get_all_records():
           eto_data = record.data_values.get('day-eto')
           precip_data = record.data_values.get('day-precip')
           
           eto = float(eto_data.value) if eto_data and eto_data.value else 0
           precip = float(precip_data.value) if precip_data and precip_data.value else 0
           
           daily_deficit = eto - precip
           cumulative_deficit += daily_deficit
           
           total_eto += eto
           total_precip += precip
           
           daily_balance.append({
               'date': record.date,
               'eto': eto,
               'precipitation': precip,
               'daily_deficit': daily_deficit,
               'cumulative_deficit': cumulative_deficit
           })
       
       summary = {
           'period': f"{start_date} to {end_date}",
           'total_eto': total_eto,
           'total_precipitation': total_precip,
           'net_deficit': total_eto - total_precip,
           'daily_data': daily_balance
       }
       
       return summary

   # Usage
   balance = water_balance_analysis(client, station_id=2, start_date="2023-06-01", end_date="2023-06-30")
   
   print(f"Water Balance Analysis for {balance['period']}:")
   print(f"Total ET: {balance['total_eto']:.2f} inches")
   print(f"Total Precipitation: {balance['total_precipitation']:.2f} inches")
   print(f"Net Deficit: {balance['net_deficit']:.2f} inches")

Data Integration Examples
-------------------------

Pandas Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   import matplotlib.pyplot as plt

   def create_weather_dataframe(client, station_ids, start_date, end_date):
       """Create a pandas DataFrame from CIMIS weather data."""
       
       weather_data = client.get_daily_data(
           targets=station_ids,
           start_date=start_date,
           end_date=end_date
       )
       
       # Convert to DataFrame
       rows = []
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
           
           rows.append(row)
       
       df = pd.DataFrame(rows)
       df.set_index('date', inplace=True)
       return df

   def plot_temperature_comparison(df):
       """Plot temperature comparison between stations."""
       fig, ax = plt.subplots(figsize=(12, 6))
       
       for station in df['station'].unique():
           station_data = df[df['station'] == station]
           ax.plot(station_data.index, station_data['day-air-tmp-avg_value'], 
                  label=f'Station {station}', marker='o', markersize=3)
       
       ax.set_title('Daily Average Temperature Comparison')
       ax.set_xlabel('Date')
       ax.set_ylabel('Temperature (°C)')
       ax.legend()
       ax.grid(True, alpha=0.3)
       
       plt.tight_layout()
       plt.show()

   # Usage
   df = create_weather_dataframe(client, [2, 8, 127], "2023-06-01", "2023-06-30")
   print(df.head())
   print(f"\\nDataFrame shape: {df.shape}")
   print(f"Stations: {df['station'].unique()}")
   
   # Basic statistics
   print(f"\\nTemperature Statistics:")
   print(df['day-air-tmp-avg_value'].describe())
   
   # Plot comparison
   plot_temperature_comparison(df)

Database Integration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import sqlite3
   from contextlib import contextmanager

   class WeatherDatabase:
       """SQLite database for storing CIMIS weather data."""
       
       def __init__(self, db_path="weather.db"):
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
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS weather_records (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT NOT NULL,
                       station TEXT NOT NULL,
                       julian TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       UNIQUE(date, station)
                   )
               ''')
               
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS weather_data (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       record_id INTEGER,
                       data_item TEXT NOT NULL,
                       value TEXT,
                       qc TEXT,
                       unit TEXT,
                       FOREIGN KEY (record_id) REFERENCES weather_records (id)
                   )
               ''')
               
               conn.commit()
       
       def store_weather_data(self, weather_data):
           """Store weather data in the database."""
           with self.get_connection() as conn:
               for record in weather_data.get_all_records():
                   # Insert weather record
                   cursor = conn.execute('''
                       INSERT OR REPLACE INTO weather_records (date, station, julian)
                       VALUES (?, ?, ?)
                   ''', (record.date, record.station, record.julian))
                   
                   record_id = cursor.lastrowid
                   
                   # Delete existing data for this record
                   conn.execute('DELETE FROM weather_data WHERE record_id = ?', (record_id,))
                   
                   # Insert weather data
                   for key, value in record.data_values.items():
                       conn.execute('''
                           INSERT INTO weather_data (record_id, data_item, value, qc, unit)
                           VALUES (?, ?, ?, ?, ?)
                       ''', (record_id, key, value.value, value.qc, value.unit))
               
               conn.commit()
       
       def get_station_data(self, station, start_date, end_date):
           """Retrieve data for a specific station and date range."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   SELECT wr.date, wr.station, wd.data_item, wd.value, wd.qc, wd.unit
                   FROM weather_records wr
                   JOIN weather_data wd ON wr.id = wd.record_id
                   WHERE wr.station = ? AND wr.date BETWEEN ? AND ?
                   ORDER BY wr.date, wd.data_item
               ''', (station, start_date, end_date))
               
               return cursor.fetchall()

   # Usage
   db = WeatherDatabase()
   
   # Store current weather data
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   db.store_weather_data(weather_data)
   
   # Retrieve stored data
   stored_data = db.get_station_data("2", "2023-06-01", "2023-06-07")
   print(f"Retrieved {len(stored_data)} data points from database")

CSV Analysis
~~~~~~~~~~~~

.. code-block:: python

   def export_and_analyze(client, station_ids, start_date, end_date):
       """Export data to CSV and perform basic analysis."""
       
       # Get weather data
       weather_data = client.get_daily_data(
           targets=station_ids,
           start_date=start_date,
           end_date=end_date
       )
       
       # Export to CSV
       csv_file = client.export_to_csv(weather_data)
       print(f"Data exported to: {csv_file}")
       
       # Read back and analyze with pandas
       import pandas as pd
       
       df = pd.read_csv(csv_file)
       print(f"\\nDataset shape: {df.shape}")
       print(f"Columns: {list(df.columns)}")
       
       # Find temperature columns
       temp_cols = [col for col in df.columns if 'air-tmp' in col and '_Value' in col]
       
       for col in temp_cols:
           if col in df.columns:
               print(f"\\n{col} statistics:")
               print(df[col].describe())
       
       # Check for missing data
       missing_data = df.isnull().sum()
       if missing_data.any():
           print(f"\\nMissing data summary:")
           print(missing_data[missing_data > 0])
       
       return csv_file, df

   # Usage
   csv_file, df = export_and_analyze(client, [2, 8], "2023-06-01", "2023-06-30")

Utility Examples
----------------

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   def process_multiple_years(client, station_id, years, chunk_months=3):
       """Process multiple years of data in chunks."""
       from datetime import date
       import calendar
       
       all_records = []
       
       for year in years:
           print(f"Processing year {year}...")
           
           # Process year in chunks
           for month in range(1, 13, chunk_months):
               start_month = month
               end_month = min(month + chunk_months - 1, 12)
               
               start_date = date(year, start_month, 1)
               
               # Get last day of end month
               _, last_day = calendar.monthrange(year, end_month)
               end_date = date(year, end_month, last_day)
               
               try:
                   weather_data = client.get_daily_data(
                       targets=[station_id],
                       start_date=start_date,
                       end_date=end_date
                   )
                   
                   records = weather_data.get_all_records()
                   all_records.extend(records)
                   print(f"  {start_date} to {end_date}: {len(records)} records")
                   
               except Exception as e:
                   print(f"  Error processing {start_date} to {end_date}: {e}")
               
               # Small delay to be respectful to the API
               import time
               time.sleep(0.5)
       
       print(f"\\nTotal records processed: {len(all_records)}")
       return all_records

   # Usage
   records = process_multiple_years(client, station_id=2, years=[2021, 2022, 2023])

Error Handling Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError
   import time
   import logging

   def robust_weather_retrieval(client, targets, start_date, end_date, max_retries=3):
       """Retrieve weather data with comprehensive error handling."""
       
       for attempt in range(max_retries):
           try:
               weather_data = client.get_daily_data(
                   targets=targets,
                   start_date=start_date,
                   end_date=end_date
               )
               
               # Validate the response
               records = weather_data.get_all_records()
               if not records:
                   raise ValueError("No data returned from API")
               
               print(f"✅ Successfully retrieved {len(records)} records")
               return weather_data
               
           except CimisAuthenticationError as e:
               print(f"❌ Authentication error: {e.message}")
               print("Please check your API key")
               break
               
           except CimisConnectionError as e:
               print(f"🌐 Connection error (attempt {attempt + 1}): {e.message}")
               
               if attempt < max_retries - 1:
                   wait_time = 2 ** attempt  # Exponential backoff
                   print(f"Retrying in {wait_time} seconds...")
                   time.sleep(wait_time)
               else:
                   print("Max retries exceeded")
                   
           except CimisAPIError as e:
               print(f"⚠️ API error: {e.message}")
               if e.error_code:
                   print(f"Error code: {e.error_code}")
               break
               
           except Exception as e:
               print(f"💥 Unexpected error: {e}")
               break
       
       return None

   # Usage
   weather_data = robust_weather_retrieval(
       client, 
       targets=[2, 8], 
       start_date="2023-06-01", 
       end_date="2023-06-07"
   )

Complete Application Example
----------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete irrigation management application using CIMIS data.
   """

   import os
   import json
   from datetime import date, timedelta
   from python_cimis import CimisClient
   from python_cimis.exceptions import CimisAPIError

   class IrrigationManager:
       """Complete irrigation management system."""
       
       def __init__(self, config_file="irrigation_config.json"):
           self.config = self._load_config(config_file)
           self.client = CimisClient(app_key=self.config['api_key'])
       
       def _load_config(self, config_file):
           """Load configuration from file."""
           if os.path.exists(config_file):
               with open(config_file, 'r') as f:
                   return json.load(f)
           else:
               # Create default config
               config = {
                   'api_key': os.getenv('CIMIS_API_KEY'),
                   'stations': [2, 8, 127],
                   'crops': {
                       'tomatoes': {'kc': 1.2, 'root_depth': 24},
                       'almonds': {'kc': 1.0, 'root_depth': 48},
                       'grapes': {'kc': 0.8, 'root_depth': 36}
                   },
                   'soil_capacity': 2.0,
                   'irrigation_threshold': 0.5
               }
               
               with open(config_file, 'w') as f:
                   json.dump(config, f, indent=2)
               
               return config
       
       def get_irrigation_recommendations(self, crop_type, days_back=14):
           """Get irrigation recommendations for a specific crop."""
           
           if crop_type not in self.config['crops']:
               raise ValueError(f"Unknown crop type: {crop_type}")
           
           crop_config = self.config['crops'][crop_type]
           
           # Get recent weather data
           end_date = date.today() - timedelta(days=1)
           start_date = end_date - timedelta(days=days_back)
           
           recommendations = {}
           
           for station in self.config['stations']:
               try:
                   weather_data = self.client.get_daily_data(
                       targets=[station],
                       start_date=start_date,
                       end_date=end_date,
                       data_items=["day-eto", "day-precip"]
                   )
                   
                   schedule = self._calculate_irrigation_schedule(
                       weather_data, crop_config
                   )
                   
                   recommendations[station] = schedule
                   
               except CimisAPIError as e:
                   print(f"Error getting data for station {station}: {e.message}")
                   recommendations[station] = None
           
           return recommendations
       
       def _calculate_irrigation_schedule(self, weather_data, crop_config):
           """Calculate irrigation schedule for specific crop."""
           
           schedule = []
           soil_deficit = 0
           
           for record in weather_data.get_all_records():
               eto_data = record.data_values.get('day-eto')
               precip_data = record.data_values.get('day-precip')
               
               if not (eto_data and eto_data.value):
                   continue
               
               eto = float(eto_data.value)
               precip = float(precip_data.value) if precip_data and precip_data.value else 0
               
               # Calculate crop water use
               etc = eto * crop_config['kc']
               
               # Update soil moisture deficit
               soil_deficit += etc - precip
               soil_deficit = max(0, soil_deficit)
               
               # Check if irrigation is needed
               threshold = self.config['soil_capacity'] * self.config['irrigation_threshold']
               
               if soil_deficit >= threshold:
                   irrigation_amount = soil_deficit
                   soil_deficit = 0
                   
                   schedule.append({
                       'date': record.date,
                       'irrigation_inches': irrigation_amount,
                       'crop_et': etc,
                       'precipitation': precip,
                       'reason': f"Soil deficit reached {irrigation_amount:.2f} inches"
                   })
           
           return {
               'irrigation_events': schedule,
               'current_deficit': soil_deficit,
               'recommendation': 'Irrigate soon' if soil_deficit >= threshold * 0.8 else 'No irrigation needed'
           }
       
       def generate_report(self, crop_type):
           """Generate comprehensive irrigation report."""
           
           recommendations = self.get_irrigation_recommendations(crop_type)
           
           print(f"\\n🌾 IRRIGATION REPORT FOR {crop_type.upper()}")
           print("=" * 50)
           
           for station, schedule in recommendations.items():
               if schedule is None:
                   print(f"\\n❌ Station {station}: Data unavailable")
                   continue
               
               print(f"\\n📍 Station {station}:")
               print(f"   Current soil deficit: {schedule['current_deficit']:.2f} inches")
               print(f"   Recommendation: {schedule['recommendation']}")
               
               if schedule['irrigation_events']:
                   print(f"   Recent irrigations:")
                   for event in schedule['irrigation_events'][-3:]:  # Last 3 events
                       print(f"     {event['date']}: {event['irrigation_inches']:.2f} inches")
               else:
                   print("   No recent irrigation needs")

   def main():
       """Main application function."""
       try:
           manager = IrrigationManager()
           
           # Generate reports for all crops
           for crop_type in manager.config['crops'].keys():
               manager.generate_report(crop_type)
           
       except Exception as e:
           print(f"Application error: {e}")

   if __name__ == "__main__":
       main()

This examples section provides practical, real-world use cases for the Python CIMIS Client library. Each example is designed to be educational and directly applicable to agricultural and environmental applications.
