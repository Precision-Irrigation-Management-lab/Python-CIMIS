"""
Centralized endpoint handling for the Python CIMIS API client.

This module contains all API endpoint configurations and request handling logic.
"""

from typing import Dict, Any, Optional, Union, List
from datetime import datetime, date


class CimisEndpoints:
    """Centralized handling of CIMIS API endpoints and request configurations."""
    
    # Base API URL
    BASE_URL = "https://et.water.ca.gov/api"
    
    # Endpoint configurations
    ENDPOINTS = {
        'data': 'data',
        'station': 'station/{station_id}',
        'stations': 'station',
        'zip_code': 'stationzipcode/{zip_code}',
        'zip_codes': 'stationzipcode',
        'spatial_zip_code': 'spatialzipcode/{zip_code}',
        'spatial_zip_codes': 'spatialzipcode'
    }
    
    # Default data items for comprehensive data collection
    DEFAULT_DAILY_DATA_ITEMS = [
        "day-air-tmp-avg", "day-air-tmp-max", "day-air-tmp-min",
        "day-dew-pnt", "day-eto", "day-asce-eto", "day-asce-etr",
        "day-precip", "day-rel-hum-avg", "day-rel-hum-max", "day-rel-hum-min",
        "day-soil-tmp-avg", "day-soil-tmp-max", "day-soil-tmp-min",
        "day-sol-rad-avg", "day-sol-rad-net", "day-vap-pres-max",
        "day-vap-pres-avg", "day-wind-ene", "day-wind-ese", "day-wind-nne",
        "day-wind-nnw", "day-wind-run", "day-wind-spd-avg", "day-wind-ssw",
        "day-wind-wnw", "day-wind-wsw"
    ]
    
    DEFAULT_HOURLY_DATA_ITEMS = [
        "hly-air-tmp", "hly-dew-pnt", "hly-eto", "hly-net-rad",
        "hly-asce-eto", "hly-asce-etr", "hly-precip", "hly-rel-hum",
        "hly-res-wind", "hly-soil-tmp", "hly-sol-rad", "hly-vap-pres",
        "hly-wind-dir", "hly-wind-spd"
    ]
    
    # Error codes mapping
    ERROR_CODES = {
        "ERR1006": "INVALID APP KEY",
        "ERR1019": "STATION NOT FOUND",
        "ERR1031": "UNSUPPORTED ZIP CODE",
        "ERR1034": "COORD NOT IN CA",
        "ERR1035": "DATA ITEM NOT FOUND",
        "ERR1025": "INVALID COORDINATE",
        "ERR2006": "INVALID TARGET",
        "ERR2115": "INVALID ADDRESS DATA ITEM",
        "ERR2114": "INVALID COORDINATE DATA ITEM",
        "ERR2007": "HLY COORDINATES FAULT",
        "ERR1010": "FUTURE DATE FAULT",
        "ERR1011": "ORIGIN DATE FAULT",
        "ERR1012": "DATE ORDER FAULT",
        "ERR1032": "INVALID UNIT OF MEASURE",
        "ERR2112": "DATA VOLUME VIOLATION"
    }
    
    @classmethod
    def get_url(cls, endpoint: str, **kwargs) -> str:
        """
        Get the full URL for an endpoint with optional parameters.
        
        Args:
            endpoint: Endpoint key from ENDPOINTS dict
            **kwargs: Parameters to format into the endpoint URL
            
        Returns:
            Full URL for the endpoint
        """
        endpoint_template = cls.ENDPOINTS.get(endpoint)
        if not endpoint_template:
            raise ValueError(f"Unknown endpoint: {endpoint}")
        
        # Format the endpoint with provided kwargs
        formatted_endpoint = endpoint_template.format(**kwargs)
        return f"{cls.BASE_URL}/{formatted_endpoint}"
    
    @classmethod
    def prepare_data_request_params(cls,
                                   app_key: str,
                                   targets: Union[str, List[str]],
                                   start_date: Union[str, date, datetime],
                                   end_date: Union[str, date, datetime],
                                   data_items: Optional[List[str]] = None,
                                   unit_of_measure: str = 'E',
                                   prioritize_scs: bool = True) -> Dict[str, Any]:
        """
        Prepare parameters for a data request.
        
        Args:
            app_key: CIMIS API application key
            targets: Station numbers, zip codes, coordinates, or addresses
            start_date: Start date
            end_date: End date
            data_items: List of data items to retrieve
            unit_of_measure: 'E' for English or 'M' for Metric
            prioritize_scs: Whether to prioritize SCS data for zip codes
            
        Returns:
            Dictionary of prepared parameters
        """
        # Format dates
        if isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime('%Y-%m-%d')
        if isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime('%Y-%m-%d')
        
        # Format targets
        if isinstance(targets, list):
            # Determine the type of targets and format accordingly
            if cls._is_coordinate_list(targets):
                targets_str = ';'.join(targets)
            elif cls._is_address_list(targets):
                targets_str = ';'.join(targets)
            else:
                targets_str = ','.join(map(str, targets))
        else:
            targets_str = str(targets)
        
        # Use default data items if none provided
        if data_items is None:
            data_items = cls.DEFAULT_DAILY_DATA_ITEMS.copy()
        
        return {
            'appKey': app_key,
            'targets': targets_str,
            'startDate': start_date,
            'endDate': end_date,
            'dataItems': ','.join(data_items),
            'unitOfMeasure': unit_of_measure,
            'prioritizeSCS': 'Y' if prioritize_scs else 'N'
        }
    
    @classmethod
    def prepare_basic_request_params(cls, app_key: str) -> Dict[str, str]:
        """
        Prepare basic parameters for simple requests.
        
        Args:
            app_key: CIMIS API application key
            
        Returns:
            Dictionary with basic parameters
        """
        return {'appKey': app_key}
    
    @classmethod
    def _is_coordinate_list(cls, targets: List[str]) -> bool:
        """Check if targets list contains coordinates."""
        return any('lat=' in str(target) and 'lng=' in str(target) for target in targets)
    
    @classmethod
    def _is_address_list(cls, targets: List[str]) -> bool:
        """Check if targets list contains addresses."""
        return any('addr-name=' in str(target) and 'addr=' in str(target) for target in targets)
    
    @classmethod
    def get_daily_data_items(cls) -> List[str]:
        """Get default daily data items."""
        return cls.DEFAULT_DAILY_DATA_ITEMS.copy()
    
    @classmethod
    def get_hourly_data_items(cls) -> List[str]:
        """Get default hourly data items."""
        return cls.DEFAULT_HOURLY_DATA_ITEMS.copy()
    
    @classmethod
    def get_all_data_items(cls) -> List[str]:
        """Get all available data items (daily + hourly)."""
        return cls.DEFAULT_DAILY_DATA_ITEMS + cls.DEFAULT_HOURLY_DATA_ITEMS
    
    @classmethod
    def validate_unit_of_measure(cls, unit: str) -> bool:
        """Validate unit of measure parameter."""
        return unit.upper() in ['E', 'M']
    
    @classmethod
    def validate_date_format(cls, date_str: str) -> bool:
        """Validate date string format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_error_description(cls, error_code: str) -> str:
        """Get human-readable error description."""
        return cls.ERROR_CODES.get(error_code, f"Unknown error: {error_code}")
    
    @classmethod
    def prepare_data_params(cls,
                           targets: Union[str, List[str]],
                           start_date: Union[str, date, datetime],
                           end_date: Union[str, date, datetime],
                           items: Optional[List[str]] = None,
                           measure_unit: str = 'E',
                           prioritize_sri: bool = True,
                           prioritize_scs: bool = True,
                           **kwargs) -> Dict[str, Any]:
        """
        Prepare parameters for data requests using the new parameter format.
        
        Args:
            targets: Station numbers, zip codes, coordinates, or addresses
            start_date: Start date
            end_date: End date
            items: List of data items to retrieve
            measure_unit: 'E' for English or 'M' for Metric
            prioritize_sri: Whether to prioritize Solar Radiation Index
            prioritize_scs: Whether to prioritize SCS data for zip codes
            **kwargs: Additional parameters
            
        Returns:
            Dictionary of prepared parameters
        """
        # Format dates
        if isinstance(start_date, (date, datetime)):
            start_date = start_date.strftime('%Y-%m-%d')
        if isinstance(end_date, (date, datetime)):
            end_date = end_date.strftime('%Y-%m-%d')
        
        # Format targets
        if isinstance(targets, list):
            # Determine the type of targets and format accordingly
            if cls._is_coordinate_list(targets):
                targets_str = ';'.join(targets)
            elif cls._is_address_list(targets):
                targets_str = ';'.join(targets)
            else:
                targets_str = ','.join(map(str, targets))
        else:
            targets_str = str(targets)
        
        # Use all available data items if none provided
        if items is None or len(items) == 0:
            items = cls.get_all_data_items()
        
        params = {
            'targets': targets_str,
            'startDate': start_date,
            'endDate': end_date,
            'dataItems': ','.join(items),
            'unitOfMeasure': measure_unit,
            'prioritizeSri': 'true' if prioritize_sri else 'false',
            'prioritizeSCS': 'Y' if prioritize_scs else 'N'
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        return params
    
    @classmethod
    def parse_data_response(cls, data: Dict[str, Any]) -> 'WeatherData':
        """Parse weather data response into WeatherData object."""
        from .models import WeatherData, WeatherProvider, WeatherRecord, DataValue
        
        weather_data = WeatherData()
        
        if 'Data' not in data or 'Providers' not in data['Data']:
            return weather_data
        
        for provider_data in data['Data']['Providers']:
            provider = WeatherProvider(
                name=provider_data.get('Name', ''),
                type=provider_data.get('Type', ''),
                owner=provider_data.get('Owner', '')
            )
            
            for record_data in provider_data.get('Records', []):
                record = WeatherRecord(
                    date=record_data.get('Date', ''),
                    julian=record_data.get('Julian', ''),
                    station=record_data.get('Station'),
                    standard=record_data.get('Standard', 'english'),
                    zip_codes=record_data.get('ZipCodes', ''),
                    scope=record_data.get('Scope', 'daily'),
                    hour=record_data.get('Hour')
                )
                
                # Parse data values
                for key, value in record_data.items():
                    if isinstance(value, dict) and 'Value' in value:
                        data_value = DataValue(
                            value=value.get('Value'),
                            qc=value.get('Qc', ' '),
                            unit=value.get('Unit', '')
                        )
                        record.data_values[key] = data_value
                
                provider.records.append(record)
            
            weather_data.providers.append(provider)
        
        return weather_data
    
    @classmethod
    def parse_stations_response(cls, data: Dict[str, Any]) -> List['Station']:
        """Parse stations response into list of Station objects."""
        from .models import Station
        
        stations = []
        
        for station_data in data.get('Stations', []):
            station = Station(
                station_nbr=station_data.get('StationNbr', ''),
                name=station_data.get('Name', ''),
                city=station_data.get('City', ''),
                regional_office=station_data.get('RegionalOffice'),
                county=station_data.get('County'),
                connect_date=station_data.get('ConnectDate', ''),
                disconnect_date=station_data.get('DisconnectDate', ''),
                is_active=station_data.get('IsActive', 'True').lower() == 'true',
                is_eto_station=station_data.get('IsEtoStation', 'True').lower() == 'true',
                elevation=station_data.get('Elevation', ''),
                ground_cover=station_data.get('GroundCover', ''),
                hms_latitude=station_data.get('HmsLatitude', ''),
                hms_longitude=station_data.get('HmsLongitude', ''),
                zip_codes=station_data.get('ZipCodes', []),
                siting_desc=station_data.get('SitingDesc', '')
            )
            stations.append(station)
        
        return stations
    
    @classmethod
    def parse_zip_codes_response(cls, data: Dict[str, Any]) -> List['ZipCode']:
        """Parse zip codes response into list of ZipCode objects."""
        from .models import ZipCode
        
        zip_codes = []
        for zip_data in data.get('ZipCodes', []):
            zip_code_obj = ZipCode(
                zip_code=zip_data.get('ZipCode', ''),
                station_nbr=str(zip_data.get('StationNbr', '')),
                connect_date=zip_data.get('ConnectDate', ''),
                disconnect_date=zip_data.get('DisconnectDate', ''),
                is_active=zip_data.get('IsActive', 'True').lower() == 'true'
            )
            zip_codes.append(zip_code_obj)
        
        return zip_codes
    
    @classmethod
    def parse_spatial_zip_codes_response(cls, data: Dict[str, Any]) -> List['SpatialZipCode']:
        """Parse spatial zip codes response into list of SpatialZipCode objects."""
        from .models import SpatialZipCode
        
        zip_codes = []
        for zip_data in data.get('ZipCodes', []):
            zip_code_obj = SpatialZipCode(
                zip_code=zip_data.get('ZipCode', ''),
                city=zip_data.get('City', ''),
                county=zip_data.get('County', ''),
                connect_date=zip_data.get('ConnectDate', ''),
                disconnect_date=zip_data.get('DisconnectDate', ''),
                is_active=zip_data.get('IsActive', 'True').lower() == 'true'
            )
            zip_codes.append(zip_code_obj)
        
        return zip_codes


# Convenience functions for endpoint access
def get_data_endpoint() -> str:
    """Get the data endpoint URL."""
    return CimisEndpoints.get_url('data')


def get_station_endpoint(station_id: Optional[str] = None) -> str:
    """Get the station endpoint URL."""
    if station_id:
        return CimisEndpoints.get_url('station_by_id', station_id=station_id)
    return CimisEndpoints.get_url('station')


def get_station_zipcode_endpoint(zipcode: Optional[str] = None) -> str:
    """Get the station zipcode endpoint URL."""
    if zipcode:
        return CimisEndpoints.get_url('station_zipcode_by_id', zipcode=zipcode)
    return CimisEndpoints.get_url('station_zipcode')


def get_spatial_zipcode_endpoint(zipcode: Optional[str] = None) -> str:
    """Get the spatial zipcode endpoint URL."""
    if zipcode:
        return CimisEndpoints.get_url('spatial_zipcode_by_id', zipcode=zipcode)
    return CimisEndpoints.get_url('spatial_zipcode')
