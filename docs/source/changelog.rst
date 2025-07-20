Changelog
=========

All notable changes to the Python CIMIS Client project will be documented here.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

[1.3.2] - 2025-07-20
---------------------

Added
~~~~~
- Complete ReadTheDocs documentation with Sphinx
- Comprehensive API reference documentation
- User guide with practical examples
- Installation guide with troubleshooting
- Examples section with real-world use cases
- Fixed get_daily_data() to return only daily records
- Enhanced README with comprehensive PyPI documentation

Changed
~~~~~~~
- Updated package metadata with correct author name
- Added M. A. Andrade as co-author
- Added Precision Irrigation Management Lab (PRIMA) as maintainer
- Updated documentation URLs to working GitHub links
- Improved CSV export with better column naming
- Enhanced error handling and validation

Fixed
~~~~~
- get_daily_data() now properly filters out hourly data
- Package metadata now shows correct author information
- Documentation URLs now point to working resources

[1.3.1] - 2025-07-18
---------------------

Added
~~~~~
- Enhanced CSV export functionality
- Automatic filename generation for exports
- Better error handling and validation
- Comprehensive test suite

Changed
~~~~~~~
- Improved API response handling
- Better data model structure
- Enhanced documentation

[1.3.0] - 2025-07-15
---------------------

Added
~~~~~
- Support for multiple target types (stations, zip codes, coordinates, addresses)
- Comprehensive data models for weather data and stations
- Custom exception classes for better error handling
- CSV export functionality with intelligent file naming
- Station discovery and information retrieval
- Quality control flag handling

Changed
~~~~~~~
- Restructured package organization
- Improved API client with better error handling
- Enhanced data validation and processing

[1.2.0] - 2025-07-10
---------------------

Added
~~~~~
- Hourly data support for WSN stations
- Spatial CIMIS System (SCS) data support
- Enhanced data filtering capabilities
- Comprehensive type hints

Changed
~~~~~~~
- Improved API response parsing
- Better handling of missing data
- Enhanced documentation

[1.1.0] - 2025-07-05
---------------------

Added
~~~~~
- Daily weather data retrieval
- Basic CSV export functionality
- Station information access
- Simple error handling

Changed
~~~~~~~
- Improved API client structure
- Better data model organization

[1.0.0] - 2025-07-01
---------------------

Added
~~~~~
- Initial release
- Basic CIMIS API client
- Core functionality for weather data retrieval
- MIT License
- Basic documentation

Features
--------

Current Features (v1.3.2)
~~~~~~~~~~~~~~~~~~~~~~~~~~

🌤️ **Weather Data Access**
   - Daily and hourly weather measurements
   - Multiple data sources (WSN and SCS)
   - Quality control information
   - Comprehensive data validation

🏛️ **Station Information**
   - Complete station metadata
   - Geographic coverage information
   - Active/inactive status tracking
   - ETo calculation capabilities

📊 **Data Export**
   - CSV export with intelligent naming
   - Configurable data filtering
   - Quality control flag inclusion
   - Batch processing support

🔧 **Developer Experience**
   - Complete type hints
   - Comprehensive error handling
   - Extensive documentation
   - Real-world examples

🌾 **Agricultural Applications**
   - Irrigation scheduling calculations
   - Growing degree day computations
   - Frost monitoring and alerts
   - Crop coefficient integration

Breaking Changes
----------------

Version 1.3.2
~~~~~~~~~~~~~~
- ``get_daily_data()`` now returns only daily records (previously could include hourly data)
- This ensures clean separation between daily and hourly data retrieval methods

Version 1.3.0
~~~~~~~~~~~~~~
- Restructured package organization - imports may need updating
- Enhanced data models with new attributes
- Improved error handling with custom exception classes

Migration Guide
---------------

From 1.3.1 to 1.3.2
~~~~~~~~~~~~~~~~~~~~

**Daily Data Filtering**

The ``get_daily_data()`` method now automatically filters out any hourly records:

.. code-block:: python

   # Before (1.3.1) - could return mixed data
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   records = weather_data.get_all_records()  # Might include hourly records
   
   # After (1.3.2) - only daily records
   weather_data = client.get_daily_data(targets=[2], start_date="2023-06-01", end_date="2023-06-07")
   records = weather_data.get_all_records()  # Only daily records

**No Action Required**

This change is backward compatible and improves data consistency. No code changes are needed.

From 1.2.x to 1.3.0
~~~~~~~~~~~~~~~~~~~~

**Package Import Changes**

.. code-block:: python

   # Before (1.2.x)
   from python_cimis.client import CimisClient
   
   # After (1.3.0)
   from python_cimis import CimisClient

**Exception Handling**

.. code-block:: python

   # Before (1.2.x)
   try:
       weather_data = client.get_daily_data(...)
   except Exception as e:
       print(f"Error: {e}")
   
   # After (1.3.0)
   from python_cimis.exceptions import CimisAPIError, CimisConnectionError
   
   try:
       weather_data = client.get_daily_data(...)
   except CimisConnectionError as e:
       print(f"Connection error: {e.message}")
   except CimisAPIError as e:
       print(f"API error: {e.message}")

Roadmap
-------

Planned Features
~~~~~~~~~~~~~~~~

**Version 1.4.0** (Q3 2025)
   - Enhanced caching system
   - Improved batch processing
   - Advanced data analytics functions
   - Integration with popular data science libraries

**Version 1.5.0** (Q4 2025)
   - Real-time data streaming
   - Advanced visualization tools
   - Machine learning integration
   - Enhanced agricultural decision support

**Version 2.0.0** (Q1 2026)
   - Async/await support
   - Multi-threaded processing
   - Advanced caching strategies
   - Enhanced performance optimizations

Contributing
------------

We welcome contributions! See our `Contributing Guide <https://github.com/python-cimis/python-cimis-client/blob/main/CONTRIBUTING.md>`_ for details.

**Areas where we need help:**
- Documentation improvements
- Example applications
- Bug reports and fixes
- Performance optimizations
- Integration with other libraries

Support
-------

- **Documentation**: Complete guides and API reference
- **Examples**: Real-world usage patterns in the examples directory
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Community support and questions

License
-------

This project is licensed under the MIT License - see the `LICENSE <https://github.com/python-cimis/python-cimis-client/blob/main/LICENSE>`_ file for details.
