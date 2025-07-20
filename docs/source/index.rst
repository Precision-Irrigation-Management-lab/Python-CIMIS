Python CIMIS Client Documentation
===================================

Welcome to the Python CIMIS Client documentation! This library provides easy access to the California Irrigation Management Information System (CIMIS) API for retrieving weather data, evapotranspiration estimates, and station information.

.. image:: https://img.shields.io/pypi/v/python-CIMIS.svg
   :target: https://pypi.org/project/python-CIMIS/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/python-CIMIS.svg
   :target: https://pypi.org/project/python-CIMIS/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/python-cimis/python-cimis-client.svg
   :target: https://github.com/python-cimis/python-cimis-client/blob/main/LICENSE
   :alt: License

Quick Start
-----------

Install the library:

.. code-block:: bash

   pip install python-CIMIS

Get your API key from the `CIMIS website <https://et.water.ca.gov/Rest/Index>`_ and start using the library:

.. code-block:: python

   from python_cimis import CimisClient
   from datetime import date, timedelta
   import os

   # Initialize client with your API key
   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

   # Get daily weather data for the last week
   end_date = date.today() - timedelta(days=1)
   start_date = end_date - timedelta(days=6)

   weather_data = client.get_daily_data(
       targets=[2],  # Five Points station
       start_date=start_date,
       end_date=end_date
   )

   # Export to CSV
   csv_file = client.export_to_csv(weather_data)
   print(f"Weather data exported to: {csv_file}")

Key Features
------------

🌤️ **Comprehensive Weather Data**
   - Daily and hourly weather measurements
   - Evapotranspiration (ET) calculations
   - Quality control flags and data validation

🏛️ **Multiple Data Sources**
   - Weather Station Network (WSN) data
   - Spatial CIMIS System (SCS) interpolated data
   - Station information and metadata

📊 **Flexible Data Retrieval**
   - Multiple target types: station numbers, coordinates, zip codes, addresses
   - Custom date ranges and data item selection
   - Built-in CSV export with intelligent file naming

🔧 **Developer Friendly**
   - Type hints for better IDE integration
   - Comprehensive error handling
   - Extensive documentation and examples

🌾 **Agricultural Applications**
   - Irrigation scheduling calculations
   - Growing degree day computations
   - Crop coefficient integration

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   user_guide
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference
   client
   models
   exceptions
   utils

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog
   license

Data Sources and Coverage
-------------------------

The CIMIS system provides data from two main sources:

**Weather Station Network (WSN)**
   Physical weather stations throughout California providing:
   
   - Daily and hourly measurements
   - High-quality instrumentation
   - Direct measurements of meteorological parameters
   - Limited geographic coverage

**Spatial CIMIS System (SCS)**
   Grid-based interpolated data covering:
   
   - Areas without physical stations
   - Daily data only (no hourly measurements)
   - Interpolated from nearby WSN stations and satellite data
   - Statewide coverage

Use Cases
---------

The Python CIMIS Client is ideal for:

🌾 **Agricultural Applications**
   - Irrigation scheduling and water management
   - Crop growth monitoring and yield prediction
   - Pest and disease management timing
   - Harvest planning optimization

🏞️ **Environmental Research**
   - Climate change impact studies
   - Ecosystem water balance modeling
   - Drought monitoring and assessment
   - Urban heat island analysis

💧 **Water Resources**
   - Regional water demand forecasting
   - Reservoir management planning
   - Groundwater recharge estimation
   - Water conservation program evaluation

📊 **Data Science and Analytics**
   - Weather pattern analysis
   - Machine learning model development
   - Agricultural decision support systems
   - Environmental monitoring dashboards

Support and Community
---------------------

- **Documentation**: You're reading it! Check the user guide and API reference for detailed information.
- **GitHub Issues**: Report bugs and request features at our `GitHub repository <https://github.com/python-cimis/python-cimis-client/issues>`_.
- **Examples**: See the `examples directory <https://github.com/python-cimis/python-cimis-client/tree/main/examples>`_ for practical use cases.
- **CIMIS Official**: Visit the `official CIMIS site <https://cimis.water.ca.gov/>`_ for more information about the data and services.

License
-------

This project is licensed under the MIT License. See the `LICENSE file <https://github.com/python-cimis/python-cimis-client/blob/main/LICENSE>`_ for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
