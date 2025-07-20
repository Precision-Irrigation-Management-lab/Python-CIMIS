"""
Utility functions and classes for the Python CIMIS Client library.

This module provides helper functions for filename generation, data formatting,
and other utility operations.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import WeatherData, Station


class FilenameGenerator:
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
    
    def generate_weather_filename(self, weather_data: 'WeatherData') -> str:
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
                    stations.append(f"Station{record.station}")
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
    
    def generate_stations_filename(self, stations: List['Station']) -> str:
        """
        Generate filename for station data export.
        
        Args:
            stations: List of Station objects
            
        Returns:
            Generated filename with full path
        """
        if not stations:
            station_part = "all_stations"
        else:
            station_names = [self._sanitize_name(station.name) for station in stations[:5]]
            if len(stations) == 1:
                station_part = station_names[0]
            elif len(stations) <= 3:
                station_part = "_".join(station_names)
            else:
                station_part = f"{station_names[0]}_plus{len(stations)-1}more"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cimis_stations_{station_part}_{timestamp}.csv"
        
        # Ensure filename is valid
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_zip_codes_filename(self, zip_codes: List[str]) -> str:
        """
        Generate filename for zip code data export.
        
        Args:
            zip_codes: List of zip codes
            
        Returns:
            Generated filename with full path
        """
        if not zip_codes:
            zip_part = "all_zipcodes"
        elif len(zip_codes) == 1:
            zip_part = f"zipcode_{zip_codes[0]}"
        elif len(zip_codes) <= 5:
            zip_part = "_".join(zip_codes)
        else:
            zip_part = f"{len(zip_codes)}_zipcodes"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cimis_zipcode_data_{zip_part}_{timestamp}.csv"
        
        # Ensure filename is valid
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_custom_filename(self, 
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
            if len(identifiers) <= 3:
                components.extend(identifiers)
            else:
                components.append(f"{len(identifiers)}_targets")
        
        if date_range:
            components.append(date_range)
        
        # Add timestamp
        components.append(datetime.now().strftime("%Y%m%d_%H%M%S"))
        
        filename = '_'.join(components) + '.csv'
        filename = self._sanitize_filename(filename)
        
        return str(self.base_directory / filename)
    
    def generate_for_weather_data(self, weather_data: 'WeatherData') -> str:
        """
        Generate filename for weather data export.
        Alias for generate_weather_filename for compatibility.
        """
        return self.generate_weather_filename(weather_data)
    
    def generate_for_stations(self, stations: List['Station']) -> str:
        """
        Generate filename for stations data export.
        Alias for generate_stations_filename for compatibility.
        """
        return self.generate_stations_filename(stations)
    
    def _format_station_names(self, stations: List[str]) -> str:
        """Format station names/numbers for filename."""
        if not stations:
            return "unknown"
        
        # Clean and format station identifiers
        clean_stations = []
        for station in stations[:5]:
            clean_stations.append(self._sanitize_name(station))
        
        if len(stations) == 1:
            return clean_stations[0]
        elif len(stations) <= 3:
            return "_".join(clean_stations)
        else:
            return f"{clean_stations[0]}_plus{len(stations)-1}more"
    
    def _format_date_range(self, dates: List[str]) -> str:
        """Format date range for filename."""
        if not dates:
            return f"unknown_{datetime.now().strftime('%Y%m%d')}"
        
        # Convert dates to YYYYMMDD format
        formatted_dates = []
        for date_str in dates:
            try:
                # Handle different date formats
                if '-' in date_str:
                    formatted_dates.append(date_str.replace('-', ''))
                else:
                    formatted_dates.append(date_str)
            except:
                continue
        
        if len(formatted_dates) == 1:
            return formatted_dates[0]
        elif len(formatted_dates) > 1:
            return f"{formatted_dates[0]}_to_{formatted_dates[-1]}"
        else:
            return f"unknown_{datetime.now().strftime('%Y%m%d')}"
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name for use in filename."""
        if not name:
            return "unnamed"
        
        # Remove special characters and spaces
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '', sanitized)
        
        return sanitized[:50]  # Limit length
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to ensure it's valid for the filesystem."""
        if not filename:
            return f"cimis_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Remove invalid characters
        invalid_chars = r'<>:"|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Replace multiple underscores with single
        filename = re.sub(r'_+', '_', filename)
        
        # Ensure reasonable length
        if len(filename) > 200:
            base, ext = filename.rsplit('.', 1)
            filename = base[:190] + f"_{datetime.now().strftime('%H%M%S')}.{ext}"
        
        return filename
    
    def set_base_directory(self, directory: Union[str, Path]) -> None:
        """Set the base directory for file output."""
        self.base_directory = Path(directory)


# Convenience functions for quick filename generation
def generate_weather_filename(weather_data: 'WeatherData', 
                            base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for weather data."""
    generator = FilenameGenerator(base_dir)
    return generator.generate_weather_filename(weather_data)


def generate_stations_filename(stations: List['Station'], 
                             base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for stations data."""
    generator = FilenameGenerator(base_dir)
    return generator.generate_stations_filename(stations)


def generate_zip_codes_filename(zip_codes: List[str], 
                              base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate filename for zip codes data."""
    generator = FilenameGenerator(base_dir)
    return generator.generate_zip_codes_filename(zip_codes)


def generate_custom_filename(data_type: str, 
                           identifiers: Optional[List[str]] = None,
                           date_range: Optional[str] = None,
                           base_dir: Optional[Union[str, Path]] = None) -> str:
    """Quick function to generate custom filename."""
    generator = FilenameGenerator(base_dir)
    return generator.generate_custom_filename(data_type, identifiers, date_range)