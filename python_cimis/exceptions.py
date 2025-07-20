"""
Exception classes for the Python CIMIS Client library.
"""


class CimisError(Exception):
    """Base exception class for all CIMIS-related errors."""
    pass


class CimisAPIError(CimisError):
    """Exception raised when the CIMIS API returns an error response."""
    
    def __init__(self, message, error_code=None, http_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.http_code = http_code
        
    def __str__(self):
        if self.error_code and self.http_code:
            return f"[{self.error_code}] HTTP {self.http_code}: {super().__str__()}"
        return super().__str__()


class CimisDataError(CimisError):
    """Exception raised when there are issues with data processing or validation."""
    pass


class CimisConnectionError(CimisError):
    """Exception raised when there are connection issues with the CIMIS API."""
    pass


class CimisAuthenticationError(CimisAPIError):
    """Exception raised when there are authentication issues with the API key."""
    pass
