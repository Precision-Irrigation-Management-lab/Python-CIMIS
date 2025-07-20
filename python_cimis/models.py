"""
Data models for the Python CIMIS Client library.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


@dataclass
class DataValue:
    """Represents a single data value with quality control information."""
    value: Optional[str]
    qc: str = " "  # Quality control flag
    unit: str = ""
    
    @property
    def numeric_value(self) -> Optional[float]:
        """Return the numeric value if possible, None otherwise."""
        try:
            return float(self.value) if self.value else None
        except (ValueError, TypeError):
            return None


@dataclass
class WeatherRecord:
    """Represents a single weather data record."""
    date: str
    julian: str
    station: Optional[str] = None
    standard: str = "english"
    zip_codes: str = ""
    scope: str = "daily"
    hour: Optional[str] = None
    data_values: Dict[str, DataValue] = field(default_factory=dict)
    
    def get_value(self, data_item: str) -> Optional[DataValue]:
        """Get a specific data value by data item name."""
        return self.data_values.get(data_item)
    
    def get_numeric_value(self, data_item: str) -> Optional[float]:
        """Get a numeric value for a specific data item."""
        data_value = self.get_value(data_item)
        return data_value.numeric_value if data_value else None


@dataclass
class WeatherProvider:
    """Represents a weather data provider (WSN or SCS)."""
    name: str
    type: str  # "station" or "spatial"
    owner: str
    records: List[WeatherRecord] = field(default_factory=list)


@dataclass
class WeatherData:
    """Main container for weather data response."""
    providers: List[WeatherProvider] = field(default_factory=list)
    
    def get_all_records(self) -> List[WeatherRecord]:
        """Get all weather records from all providers."""
        all_records = []
        for provider in self.providers:
            all_records.extend(provider.records)
        return all_records
    
    def get_records_by_station(self, station_number: str) -> List[WeatherRecord]:
        """Get all records for a specific station."""
        return [record for record in self.get_all_records() 
                if record.station == station_number]
    
    def get_records_by_date(self, date: str) -> List[WeatherRecord]:
        """Get all records for a specific date."""
        return [record for record in self.get_all_records() 
                if record.date == date]


@dataclass
class Station:
    """Represents a CIMIS weather station."""
    station_nbr: str
    name: str
    city: str
    regional_office: Optional[str] = None
    county: Optional[str] = None
    connect_date: str = ""
    disconnect_date: str = ""
    is_active: bool = True
    is_eto_station: bool = True
    elevation: str = ""
    ground_cover: str = ""
    hms_latitude: str = ""
    hms_longitude: str = ""
    zip_codes: List[str] = field(default_factory=list)
    siting_desc: str = ""
    
    @property
    def latitude(self) -> Optional[float]:
        """Extract decimal latitude from HMS format."""
        try:
            if "/" in self.hms_latitude:
                decimal_part = self.hms_latitude.split("/")[1].strip()
                return float(decimal_part)
        except (ValueError, IndexError):
            pass
        return None
    
    @property
    def longitude(self) -> Optional[float]:
        """Extract decimal longitude from HMS format."""
        try:
            if "/" in self.hms_longitude:
                decimal_part = self.hms_longitude.split("/")[1].strip()
                return float(decimal_part)
        except (ValueError, IndexError):
            pass
        return None


@dataclass
class ZipCode:
    """Represents a zip code with CIMIS support information."""
    zip_code: str
    station_nbr: Optional[str] = None
    connect_date: str = ""
    disconnect_date: str = ""
    is_active: bool = True


@dataclass
class SpatialZipCode:
    """Represents a spatial zip code supported by SCS."""
    zip_code: str
    city: str = ""
    county: str = ""
    connect_date: str = ""
    disconnect_date: str = ""
    is_active: bool = True
