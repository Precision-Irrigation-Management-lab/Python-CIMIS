"""
Python CIMIS Client - A comprehensive client library for the California Irrigation Management Information System (CIMIS) API.

This package provides easy access to CIMIS weather station data, spatial data, and station information
with built-in CSV export functionality.
"""

from .client import CimisClient
from .exceptions import CimisError, CimisAPIError, CimisDataError, CimisConnectionError, CimisAuthenticationError
from .models import WeatherData, Station, ZipCode, SpatialZipCode

__version__ = "1.0.0"
__author__ = "Mahipal Reddy Ramireddy, M. A. Andrade"
__email__ = "mahipalbablu16@gmail.com"
__maintainer__ = "Precision Irrigation Management Lab (PRIMA)"
__description__ = "A comprehensive Python client for the California Irrigation Management Information System (CIMIS) API"

__all__ = [
    "CimisClient",
    "CimisError", 
    "CimisAPIError",
    "CimisDataError",
    "CimisConnectionError",
    "CimisAuthenticationError",
    "WeatherData",
    "Station",
    "ZipCode",
    "SpatialZipCode"
]
