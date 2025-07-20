"""
Auto filename generation utilities for the Python CIMIS API client.

This module provides intelligent filename generation based on station names,
dates, and data types for automatic CSV file naming.
"""

import re
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import WeatherData, Station


class AutoFilenameGenerator:
    """
    Generates intelligent filenames for CIMIS data exports based on:
    - Station names and numbers
    - Date ranges
    - Data types (weather data, stations, etc.)
    """
    
    def __init__(self, base_directory: Optional[Union[str, Path]] = None):
        """
        Initialize the filename generator.
        
        Args:
            base_directory: Base directory for file output (uses current directory if None)
        """
        self.base_directory = Path(base_directory) if base_directory else Path.cwd()
    
    def generate_for_weather_data(self, weather_data: 'WeatherData') -> str:
        """
        Generate filename for weather data export.
        
        Args:
            weather_data: WeatherData object containing the data
            
        Returns:
            Generated filename with full path
        """
        # Extract station information and date ranges
        stations = []
        dates = []
        
        for provider in weather_data.providers:
            for record in provider.records:
                if record.station:
                    stations.append(record.station)
                if record.date:
                    dates.append(record.date)
        
        # Remove duplicates and sort
        unique_stations = sorted(set(stations))
        unique_dates = sorted(set(dates))
        
        # Create filename components
        station_part = self._format_station_names(unique_stations)
        date_part = self._format_date_range(unique_dates)
        timestamp_part = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Combine components
        filename = f"cimis_weather_data_{station_part}_{date_part}_{timestamp_part}.csv"
        
        # Ensure filename is valid and not too long
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_for_stations(self, stations: List['Station']) -> str:
        """
        Generate filename for station data export.
        
        Args:
            stations: List of Station objects
            
        Returns:
            Generated filename with full path
        """
        if not stations:
            filename = f"cimis_stations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            # Extract station information
            station_numbers = [s.station_nbr for s in stations if s.station_nbr]
            station_names = [s.name for s in stations if s.name]
            
            if len(stations) == 1:
                # Single station
                station = stations[0]
                station_part = self._sanitize_name(station.name or station.station_nbr or 'unknown')
                filename = f"cimis_station_{station_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            elif len(stations) <= 5:
                # Few stations - use names/numbers
                station_part = self._format_station_names(station_numbers[:5])
                filename = f"cimis_stations_{station_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            else:
                # Many stations - use count
                filename = f"cimis_stations_{len(stations)}_stations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Ensure filename is valid
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_for_zip_codes(self, zip_codes: List[str]) -> str:
        """
        Generate filename for zip code data export.
        
        Args:
            zip_codes: List of zip codes
            
        Returns:
            Generated filename with full path
        """
        if not zip_codes:
            filename = f"cimis_zipcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        elif len(zip_codes) == 1:
            filename = f"cimis_zipcode_{zip_codes[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        elif len(zip_codes) <= 5:
            zip_part = '_'.join(zip_codes[:5])
            filename = f"cimis_zipcodes_{zip_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            filename = f"cimis_zipcodes_{len(zip_codes)}_codes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Ensure filename is valid
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_custom(self, 
                       data_type: str, 
                       identifiers: Optional[List[str]] = None,
                       date_range: Optional[str] = None) -> str:
        """
        Generate custom filename with specified components.
        
        Args:
            data_type: Type of data (e.g., 'weather', 'stations', 'hourly')
            identifiers: List of identifiers (station numbers, zip codes, etc.)
            date_range: Date range string
            
        Returns:
            Generated filename with full path
        """
        components = ['cimis', data_type]
        
        if identifiers:
            if len(identifiers) == 1:
                components.append(identifiers[0])
            elif len(identifiers) <= 3:
                components.append('_'.join(identifiers))
            else:
                components.append(f"{len(identifiers)}_items")
        
        if date_range:
            components.append(date_range)
        
        # Add timestamp
        components.append(datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        filename = '_'.join(components) + '.csv'
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def _format_station_names(self, stations: List[str]) -> str:
        """Format station names/numbers for filename."""
        if not stations:
            return "unknown"
        
        # Clean and format station identifiers
        clean_stations = []
        for station in stations[:5]:  # Limit to first 5 for filename length
            clean_station = self._sanitize_name(str(station))
            clean_stations.append(clean_station)
        
        if len(stations) == 1:
            return clean_stations[0]
        elif len(stations) <= 3:
            return '_'.join(clean_stations)
        else:
            return f"{clean_stations[0]}_plus_{len(stations)-1}_more"
    
    def _format_date_range(self, dates: List[str]) -> str:
        """Format date range for filename."""
        if not dates:
            return datetime.now().strftime("%Y%m%d")
        
        # Sort dates
        sorted_dates = sorted(dates)
        
        if len(sorted_dates) == 1:
            # Single date
            try:
                parsed_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
                return parsed_date.strftime("%Y%m%d")
            except ValueError:
                return datetime.now().strftime("%Y%m%d")
        else:
            # Date range
            try:
                start_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
                end_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")
                return f"{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}"
            except ValueError:
                return datetime.now().strftime("%Y%m%d")
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name for use in filenames."""
        if not name:
            return "unknown"
        
        # Remove or replace problematic characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)  # Remove invalid filename chars
        name = re.sub(r'[\s\-]+', '_', name)      # Replace spaces and hyphens with underscores
        name = re.sub(r'_+', '_', name)           # Replace multiple underscores with single
        name = name.strip('_')                    # Remove leading/trailing underscores
        name = name.lower()                       # Convert to lowercase
        
        # Limit length
        if len(name) > 30:
            name = name[:30]
        
        return name or "unknown"
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename and ensure it's not too long."""
        if not filename:
            return f"cimis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        
        # Ensure proper extension
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        
        # Limit total filename length (excluding path)
        name_part = Path(filename).stem
        extension = Path(filename).suffix
        
        if len(name_part) > 200:  # Leave room for extension and safety
            name_part = name_part[:200]
            filename = name_part + extension
        
        return filename
    
    def set_base_directory(self, directory: Union[str, Path]) -> None:
        """Set the base directory for file output."""
        self.base_directory = Path(directory)
        self.base_directory.mkdir(parents=True, exist_ok=True)


# Convenience functions for quick filename generation
def generate_weather_filename(weather_data: 'WeatherData', 
                            base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for weather data."""
    generator = AutoFilenameGenerator(base_dir)
    return generator.generate_for_weather_data(weather_data)


def generate_stations_filename(stations: List['Station'], 
                             base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for stations data."""
    generator = AutoFilenameGenerator(base_dir)
    return generator.generate_for_stations(stations)


def generate_zip_codes_filename(zip_codes: List[str], 
                              base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for zip codes data."""
    generator = AutoFilenameGenerator(base_dir)
    return generator.generate_for_zip_codes(zip_codes)


def generate_custom_filename(data_type: str, 
                           identifiers: Optional[List[str]] = None,
                           date_range: Optional[str] = None,
                           base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate custom filename."""
    generator = AutoFilenameGenerator(base_dir)
    return generator.generate_custom(data_type, identifiers, date_range)
