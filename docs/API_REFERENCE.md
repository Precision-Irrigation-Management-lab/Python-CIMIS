# Python CIMIS Client - API Reference

Complete API reference for the Python CIMIS Client library.

## Table of Contents

- [CimisClient](#cimisclient)
- [Data Models](#data-models)
- [Exceptions](#exceptions)
- [Utilities](#utilities)
- [Constants](#constants)

---

## CimisClient

The main client class for interacting with the CIMIS API.

### Constructor

```python
CimisClient(app_key: str, timeout: int = 30)
```

**Parameters:**
- `app_key` (str): Your CIMIS API key
- `timeout` (int, optional): Request timeout in seconds. Default: 30

**Example:**
```python
from python_cimis import CimisClient
import os

# Using environment variable (recommended)
client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

# Direct key (not recommended for production)
client = CimisClient(app_key="your-api-key-here", timeout=60)
```

### Methods

#### get_daily_data()

Retrieve daily weather data from CIMIS stations.

```python
get_daily_data(
    targets: List[Union[int, str]],
    start_date: Union[str, date],
    end_date: Union[str, date],
    data_items: Optional[List[str]] = None,
    unit_of_measure: str = "Metric",
    prioritize_scs: bool = False
) -> WeatherData
```

**Parameters:**
- `targets`: List of station numbers, zip codes, coordinates, or addresses
- `start_date`: Start date (ISO format "YYYY-MM-DD" or date object)
- `end_date`: End date (ISO format "YYYY-MM-DD" or date object)
- `data_items`: Specific data items to retrieve (optional, defaults to all)
- `unit_of_measure`: "Metric" for metric units (default), "English" for English units
- `prioritize_scs`: Prioritize Spatial CIMIS System data

**Target Types:**
```python
# Station numbers
targets=[2, 8, 127]

# Zip codes
targets=["95823", "94503"]

# Coordinates
targets=["lat=38.5816,lng=-121.4944"]

# Addresses
targets=["addr-name=Capitol,addr=1315 10th Street Sacramento, CA 95814"]

# Mixed types
targets=[2, "95823", "lat=38.5816,lng=-121.4944"]
```

**Returns:** `WeatherData` object containing the response

**Example:**
```python
from datetime import date

weather_data = client.get_daily_data(
    targets=[2, 8],
    start_date=date(2023, 1, 1),
    end_date=date(2023, 1, 7),
    data_items=["day-air-tmp-avg", "day-eto", "day-precip"]
    # unit_of_measure defaults to "Metric"
)
```

#### get_hourly_data()

Retrieve hourly weather data from WSN stations only.

```python
get_hourly_data(
    targets: List[Union[int, str]],
    start_date: Union[str, date],
    end_date: Union[str, date],
    data_items: Optional[List[str]] = None,
    unit_of_measure: str = "E"
) -> WeatherData
```

**Parameters:** Same as `get_daily_data()` except `prioritize_scs` (not applicable)

**Note:** Hourly data is only available from Weather Station Network (WSN) stations, not Spatial CIMIS System (SCS).

**Example:**
```python
# Get hourly data for yesterday
from datetime import date, timedelta

yesterday = date.today() - timedelta(days=1)
hourly_data = client.get_hourly_data(
    targets=[2, 8],
    start_date=yesterday,
    end_date=yesterday,
    data_items=["hly-air-tmp", "hly-rel-hum", "hly-eto"]
)
```

#### get_stations()

Retrieve information about CIMIS weather stations.

```python
get_stations(station_number: Optional[str] = None) -> List[Station]
```

**Parameters:**
- `station_number`: Specific station number (optional, returns all if not specified)

**Returns:** List of `Station` objects

**Example:**
```python
# Get all stations
all_stations = client.get_stations()

# Get specific station
station_2 = client.get_stations(station_number="2")

# Find active ETo stations
active_eto_stations = [s for s in all_stations if s.is_active and s.is_eto_station]
```

#### get_station_zip_codes()

Get zip codes served by WSN stations.

```python
get_station_zip_codes() -> List[ZipCode]
```

**Returns:** List of `ZipCode` objects for WSN stations

#### get_spatial_zip_codes()

Get zip codes served by the Spatial CIMIS System.

```python
get_spatial_zip_codes() -> List[SpatialZipCode]
```

**Returns:** List of `SpatialZipCode` objects for SCS

#### export_to_csv()

Export weather data to CSV file with comprehensive column coverage.

```python
export_to_csv(
    weather_data: WeatherData,
    filename: Optional[str] = None
) -> str
```

**Parameters:**
- `weather_data`: WeatherData object to export
- `filename`: Output filename (optional, auto-generated if not provided)

**Returns:** Path to the created CSV file

**Auto-generated Filename Format:**
- Single station: `"Station{number}_{name}_{start_date}_to_{end_date}.csv"`
- Multiple stations: `"MultiStation_{start_date}_to_{end_date}.csv"`

**CSV Columns:**
- Provider metadata: Provider_Name, Provider_Type, Date, Julian, Station, etc.
- Data values: Each data item gets three columns (Value, QC, Unit)
- Example: `day-air-tmp-avg_Value`, `day-air-tmp-avg_QC`, `day-air-tmp-avg_Unit`

**Example:**
```python
# Auto-generated filename
csv_file = client.export_to_csv(weather_data)
print(f"Exported to: {csv_file}")

# Custom filename
client.export_to_csv(weather_data, filename="my_weather_data.csv")
```

#### export_stations_to_csv()

Export station information to CSV file.

```python
export_stations_to_csv(
    stations: List[Station],
    filename: str = "stations.csv"
) -> str
```

**Parameters:**
- `stations`: List of Station objects
- `filename`: Output filename

**Returns:** Path to the created CSV file

---

## Data Models

### WeatherData

Container for weather data API responses.

**Attributes:**
- `providers: List[Provider]` - List of data providers (WSN/SCS)

**Methods:**

#### get_all_records()
```python
get_all_records() -> List[WeatherRecord]
```
Returns all weather records from all providers.

#### get_records_by_station()
```python
get_records_by_station(station: str) -> List[WeatherRecord]
```
Returns records for a specific station.

**Example:**
```python
# Get all records
all_records = weather_data.get_all_records()

# Get records for station 2
station_2_records = weather_data.get_records_by_station("2")

# Check total record count
print(f"Total records: {len(all_records)}")
```

### Provider

Represents a data provider (WSN or SCS).

**Attributes:**
- `name: str` - Provider name ("WSN" or "SCS")
- `records: List[WeatherRecord]` - List of weather records

### WeatherRecord

Individual weather data record.

**Attributes:**
- `date: str` - Date in YYYY-MM-DD format
- `julian: str` - Julian day
- `station: str` - Station identifier
- `standard: str` - Data standard
- `hour: Optional[str]` - Hour (for hourly data)
- `data_values: Dict[str, DataValue]` - Dictionary of data values

**Example:**
```python
for record in weather_data.get_all_records():
    print(f"Date: {record.date}, Station: {record.station}")
    
    # Access specific data items
    temp_data = record.data_values.get('day-air-tmp-avg')
    if temp_data and temp_data.value:
        print(f"Average Temperature: {temp_data.value} {temp_data.unit}")
```

### DataValue

Individual data point with quality control information.

**Attributes:**
- `value: Optional[str]` - Data value
- `qc: str` - Quality control flag
- `unit: str` - Unit of measurement

**Quality Control Flags:**
- `" "` (space) - Measured or calculated
- `"Y"` - Missing data replaced with estimated value
- `"M"` - Missing data not replaced

### Station

Weather station information.

**Attributes:**
- `station_nbr: str` - Station number
- `name: str` - Station name
- `city: str` - City name
- `regional_office: str` - Regional office
- `county: str` - County
- `connect_date: str` - Connection date
- `disconnect_date: Optional[str]` - Disconnection date
- `is_active: bool` - Whether station is active
- `is_eto_station: bool` - Whether station calculates ETo
- `elevation: str` - Elevation
- `ground_cover: str` - Ground cover type
- `hms_latitude: str` - Latitude in HMS format
- `hms_longitude: str` - Longitude in HMS format
- `zip_codes: str` - Associated zip codes
- `site_url: str` - Site URL

### ZipCode

WSN station zip code information.

**Attributes:**
- `zip_code: str` - Zip code
- `station_nbr: str` - Associated station number

### SpatialZipCode

Spatial CIMIS System zip code information.

**Attributes:**
- `zip_code: str` - Zip code
- `city: str` - City name
- `county: str` - County name

---

## Exceptions

### CimisAPIError

Base exception for CIMIS API errors.

**Attributes:**
- `message: str` - Error message
- `error_code: Optional[str]` - API error code
- `response: Optional[requests.Response]` - HTTP response object

### CimisConnectionError

Exception for connection-related errors.

**Attributes:**
- `message: str` - Error message

### CimisAuthenticationError

Exception for authentication errors (invalid API key).

**Attributes:**
- `message: str` - Error message

**Example:**
```python
from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError

try:
    weather_data = client.get_daily_data(targets=[2], start_date="2023-01-01", end_date="2023-01-07")
except CimisAuthenticationError:
    print("Invalid API key")
except CimisConnectionError as e:
    print(f"Connection error: {e.message}")
except CimisAPIError as e:
    print(f"API error: {e.message} (Code: {e.error_code})")
```

---

## Utilities

### FilenameGenerator

Utility class for generating intelligent CSV filenames.

**Methods:**

#### generate()
```python
generate(weather_data: WeatherData) -> str
```
Generates a filename based on weather data content.

**Example:**
```python
from python_cimis.utils import FilenameGenerator

filename = FilenameGenerator.generate(weather_data)
# Result: "Station2_FivePoints_20230101_to_20230107.csv"
```

---

## Constants

### Available Data Items

#### Daily Data Items
```python
DAILY_DATA_ITEMS = [
    # Temperature
    "day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min",
    
    # Humidity  
    "day-rel-hum-avg", "day-rel-hum-max", "day-rel-hum-min",
    
    # Evapotranspiration
    "day-eto", "day-asce-eto", "day-asce-etr",
    
    # Solar Radiation
    "day-sol-rad-avg", "day-sol-rad-net",
    
    # Wind
    "day-wind-spd-avg", "day-wind-run",
    "day-wind-nw", "day-wind-ene", "day-wind-wsw", "day-wind-sse",
    
    # Soil
    "day-soil-tmp-avg", "day-soil-tmp-max", "day-soil-tmp-min",
    
    # Other
    "day-precip", "day-dew-pnt", "day-vap-pres-avg", "day-vap-pres-max"
]
```

#### Hourly Data Items
```python
HOURLY_DATA_ITEMS = [
    # Temperature
    "hly-air-tmp", "hly-soil-tmp",
    
    # Humidity
    "hly-rel-hum",
    
    # Evapotranspiration
    "hly-eto", "hly-asce-eto", "hly-asce-etr",
    
    # Solar
    "hly-sol-rad", "hly-net-rad",
    
    # Wind
    "hly-wind-spd", "hly-wind-dir", "hly-res-wind",
    
    # Other
    "hly-precip", "hly-dew-pnt", "hly-vap-pres"
]
```

### Unit Types
- `"M"` - Metric units (default)
- `"E"` - English units

### Provider Types
- `"WSN"` - Weather Station Network
- `"SCS"` - Spatial CIMIS System

---

## Type Hints

The library provides comprehensive type hints for better IDE integration:

```python
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
    try:
        weather_data: WeatherData = client.get_daily_data(
            targets=stations,
            start_date=start,
            end_date=end
        )
        return client.export_to_csv(weather_data)
    except Exception:
        return None
```

---

## Performance Considerations

### Request Limits
- Daily data: Recommend limiting to 1-2 months per request
- Hourly data: Recommend limiting to 7-14 days per request
- Large date ranges should be split into smaller chunks

### CSV Export
- Large datasets may take time to process
- Consider filtering data items for faster exports
- Auto-generated filenames prevent overwriting

### Error Handling
- Always wrap API calls in try-catch blocks
- Check for data availability before processing
- Implement retry logic for connection errors

**Example:**
```python
import time
from python_cimis.exceptions import CimisConnectionError

def robust_data_request(client, targets, start_date, end_date, retries=3):
    """Request data with retry logic."""
    for attempt in range(retries):
        try:
            return client.get_daily_data(targets, start_date, end_date)
        except CimisConnectionError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
```
