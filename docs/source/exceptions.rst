Exceptions
==========

Custom exception classes for handling CIMIS API errors.

.. currentmodule:: python_cimis.exceptions

Exception Hierarchy
-------------------

All CIMIS-specific exceptions inherit from the base ``CimisAPIError`` class:

.. code-block:: text

   CimisAPIError
   ├── CimisAuthenticationError
   └── CimisConnectionError

CimisAPIError
-------------

Base exception for all CIMIS API errors.

.. autoclass:: CimisAPIError
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisAPIError

   try:
       weather_data = client.get_daily_data(
           targets=[2],
           start_date="2023-06-01",
           end_date="2023-06-07"
       )
   except CimisAPIError as e:
       print(f"API Error: {e.message}")
       if e.error_code:
           print(f"Error Code: {e.error_code}")
       if e.response:
           print(f"HTTP Status: {e.response.status_code}")

CimisAuthenticationError
------------------------

Exception raised for authentication-related errors.

.. autoclass:: CimisAuthenticationError
   :members:
   :undoc-members:
   :show-inheritance:

Common Causes
~~~~~~~~~~~~~

- Invalid API key
- Expired API key
- API key not provided
- Account suspended or deactivated

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisAuthenticationError

   try:
       client = CimisClient(app_key="invalid-key")
       weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   except CimisAuthenticationError as e:
       print(f"Authentication failed: {e.message}")
       print("Please check your API key and ensure it's valid")

CimisConnectionError
--------------------

Exception raised for connection-related errors.

.. autoclass:: CimisConnectionError
   :members:
   :undoc-members:
   :show-inheritance:

Common Causes
~~~~~~~~~~~~~

- Network connectivity issues
- CIMIS server temporarily unavailable
- Request timeout
- DNS resolution problems
- Firewall or proxy blocking requests

Usage Examples
~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisConnectionError
   import time

   def robust_request(client, max_retries=3):
       """Request with retry logic for connection errors."""
       
       for attempt in range(max_retries):
           try:
               return client.get_daily_data(
                   targets=[2],
                   start_date="2023-06-01",
                   end_date="2023-06-07"
               )
           except CimisConnectionError as e:
               print(f"Connection error (attempt {attempt + 1}): {e.message}")
               
               if attempt < max_retries - 1:
                   # Exponential backoff
                   wait_time = 2 ** attempt
                   print(f"Retrying in {wait_time} seconds...")
                   time.sleep(wait_time)
               else:
                   print("Max retries exceeded")
                   raise

Error Handling Patterns
------------------------

Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError

   def safe_api_call(client, **kwargs):
       """Safely call the CIMIS API with error handling."""
       try:
           return client.get_daily_data(**kwargs)
           
       except CimisAuthenticationError as e:
           print(f"❌ Authentication Error: {e.message}")
           print("💡 Solution: Check your API key")
           return None
           
       except CimisConnectionError as e:
           print(f"🌐 Connection Error: {e.message}")
           print("💡 Solution: Check your internet connection and try again")
           return None
           
       except CimisAPIError as e:
           print(f"⚠️ API Error: {e.message}")
           if e.error_code:
               print(f"📋 Error Code: {e.error_code}")
           return None

Advanced Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from typing import Optional
   from python_cimis import CimisClient, WeatherData
   from python_cimis.exceptions import CimisAPIError, CimisConnectionError, CimisAuthenticationError

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   class RobustCimisClient:
       """A wrapper around CimisClient with robust error handling."""
       
       def __init__(self, app_key: str, max_retries: int = 3, timeout: int = 30):
           self.client = CimisClient(app_key=app_key, timeout=timeout)
           self.max_retries = max_retries
       
       def get_daily_data_robust(self, **kwargs) -> Optional[WeatherData]:
           """Get daily data with comprehensive error handling and retries."""
           
           for attempt in range(self.max_retries):
               try:
                   logger.info(f"Attempting API call (attempt {attempt + 1})")
                   result = self.client.get_daily_data(**kwargs)
                   logger.info("API call successful")
                   return result
                   
               except CimisAuthenticationError as e:
                   logger.error(f"Authentication error: {e.message}")
                   # Don't retry authentication errors
                   break
                   
               except CimisConnectionError as e:
                   logger.warning(f"Connection error on attempt {attempt + 1}: {e.message}")
                   
                   if attempt < self.max_retries - 1:
                       wait_time = 2 ** attempt
                       logger.info(f"Retrying in {wait_time} seconds...")
                       time.sleep(wait_time)
                   else:
                       logger.error("Max retries exceeded for connection error")
                       
               except CimisAPIError as e:
                   logger.error(f"API error: {e.message} (Code: {e.error_code})")
                   # Don't retry generic API errors
                   break
                   
               except Exception as e:
                   logger.error(f"Unexpected error: {str(e)}")
                   break
           
           return None

Specific Error Scenarios
------------------------

Invalid API Key
~~~~~~~~~~~~~~~

.. code-block:: python

   def check_api_key(client):
       """Verify that the API key is valid."""
       try:
           # Try a simple request to verify the key
           stations = client.get_stations()
           print("✅ API key is valid")
           return True
           
       except CimisAuthenticationError:
           print("❌ Invalid API key")
           print("Please check:")
           print("  1. API key is correct")
           print("  2. API key is not expired")
           print("  3. Account is active")
           return False

Network Issues
~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from python_cimis.exceptions import CimisConnectionError

   def diagnose_connection_issue():
       """Diagnose connection issues."""
       try:
           # Test basic connectivity to CIMIS
           response = requests.get("https://et.water.ca.gov", timeout=10)
           if response.status_code == 200:
               print("✅ Can reach CIMIS website")
           else:
               print(f"⚠️ CIMIS website returned status {response.status_code}")
               
       except requests.ConnectionError:
           print("❌ Cannot connect to CIMIS website")
           print("Check your internet connection")
           
       except requests.Timeout:
           print("⏱️ Connection to CIMIS website timed out")
           print("Try increasing the timeout or check network speed")

Rate Limiting
~~~~~~~~~~~~~

.. code-block:: python

   import time
   from datetime import datetime

   class RateLimitedClient:
       """Client with built-in rate limiting."""
       
       def __init__(self, app_key, requests_per_minute=60):
           self.client = CimisClient(app_key=app_key)
           self.requests_per_minute = requests_per_minute
           self.request_times = []
       
       def _wait_if_needed(self):
           """Wait if rate limit would be exceeded."""
           now = datetime.now()
           
           # Remove requests older than 1 minute
           cutoff = now.timestamp() - 60
           self.request_times = [t for t in self.request_times if t > cutoff]
           
           # Wait if we're at the limit
           if len(self.request_times) >= self.requests_per_minute:
               wait_time = 60 - (now.timestamp() - self.request_times[0])
               if wait_time > 0:
                   print(f"Rate limiting: waiting {wait_time:.1f} seconds")
                   time.sleep(wait_time)
           
           self.request_times.append(now.timestamp())
       
       def get_daily_data(self, **kwargs):
           """Get daily data with rate limiting."""
           self._wait_if_needed()
           return self.client.get_daily_data(**kwargs)

Logging and Monitoring
----------------------

Setting Up Logging
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from python_cimis.exceptions import CimisAPIError

   # Configure logging for CIMIS operations
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('cimis_client.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger('cimis_client')

   def logged_api_call(client, operation_name, **kwargs):
       """Make API call with comprehensive logging."""
       logger.info(f"Starting {operation_name} with parameters: {kwargs}")
       
       try:
           result = client.get_daily_data(**kwargs)
           logger.info(f"{operation_name} completed successfully")
           return result
           
       except CimisAPIError as e:
           logger.error(f"{operation_name} failed: {e.message}")
           if e.error_code:
               logger.error(f"Error code: {e.error_code}")
           raise

Error Reporting
~~~~~~~~~~~~~~~

.. code-block:: python

   def create_error_report(exception, context=None):
       """Create a detailed error report for troubleshooting."""
       import traceback
       from datetime import datetime
       
       report = {
           'timestamp': datetime.now().isoformat(),
           'exception_type': type(exception).__name__,
           'message': str(exception),
           'context': context or {}
       }
       
       if isinstance(exception, CimisAPIError):
           report['error_code'] = getattr(exception, 'error_code', None)
           report['response_status'] = getattr(exception.response, 'status_code', None) if hasattr(exception, 'response') and exception.response else None
       
       report['traceback'] = traceback.format_exc()
       
       return report

   # Usage
   try:
       weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   except CimisAPIError as e:
       error_report = create_error_report(e, {'targets': [2], 'date_range': '2023-06-01 to 2023-06-07'})
       logger.error(f"Error report: {error_report}")

Best Practices
--------------

1. **Always use specific exception types** for different error scenarios
2. **Implement retry logic** for connection errors but not for authentication errors  
3. **Log errors appropriately** for debugging and monitoring
4. **Provide helpful error messages** to users
5. **Validate inputs** before making API calls to prevent errors
6. **Use timeouts** to prevent hanging requests
7. **Monitor API usage** to stay within rate limits

Testing Error Scenarios
------------------------

.. code-block:: python

   import pytest
   from python_cimis.exceptions import CimisAuthenticationError, CimisConnectionError

   def test_invalid_api_key():
       """Test handling of invalid API key."""
       client = CimisClient(app_key="invalid-key")
       
       with pytest.raises(CimisAuthenticationError):
           client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")

   def test_connection_error_handling():
       """Test connection error handling."""
       # Mock network issues and test retry logic
       # Implementation depends on your testing framework
