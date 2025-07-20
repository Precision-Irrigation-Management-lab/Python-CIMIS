Installation
============

System Requirements
-------------------

- **Python 3.8 or higher**
- **Operating Systems**: Windows, macOS, Linux
- **Dependencies**: requests >= 2.25.0 (automatically installed)

Installation Methods
--------------------

PyPI Installation (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install python-CIMIS

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For the latest development version or to contribute:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/python-cimis/python-cimis-client.git
   cd python-cimis-client

   # Install in development mode
   pip install -e .

   # Or install with development dependencies
   pip install -e ".[dev]"

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an isolated environment for your project:

**Using venv (Python 3.3+)**

.. code-block:: bash

   # Create virtual environment
   python -m venv cimis_env

   # Activate (Windows)
   cimis_env\\Scripts\\activate

   # Activate (Linux/macOS)
   source cimis_env/bin/activate

   # Install the library
   pip install python-CIMIS

**Using conda**

.. code-block:: bash

   # Create conda environment
   conda create -n cimis_env python=3.11

   # Activate environment
   conda activate cimis_env

   # Install the library
   pip install python-CIMIS

API Key Setup
-------------

Register for CIMIS API Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit the `CIMIS REST API page <https://et.water.ca.gov/Rest/Index>`_
2. Click "Register for a new account" or "Sign In" if you have an existing account
3. Fill out the registration form with your information and intended use
4. Agree to the terms and conditions and submit

Generate Your API Key
~~~~~~~~~~~~~~~~~~~~~~

1. After registration approval (usually immediate), log into your account
2. Navigate to the API Key section
3. Click "Generate New Key" or "Show API Key"
4. Copy your API key (format: ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx``)

Secure Your API Key
~~~~~~~~~~~~~~~~~~~

**Environment Variable (Recommended)**

*Windows:*

.. code-block:: batch

   # Command Prompt
   set CIMIS_API_KEY=your-actual-api-key-here

   # PowerShell
   $env:CIMIS_API_KEY="your-actual-api-key-here"

*Linux/macOS:*

.. code-block:: bash

   # Temporary (current session)
   export CIMIS_API_KEY="your-actual-api-key-here"

   # Permanent (add to ~/.bashrc or ~/.zshrc)
   echo 'export CIMIS_API_KEY="your-actual-api-key-here"' >> ~/.bashrc
   source ~/.bashrc

**.env File (For Development)**

Create a ``.env`` file in your project root:

.. code-block:: text

   # .env file
   CIMIS_API_KEY=your-actual-api-key-here

.. warning::
   Add ``.env`` to your ``.gitignore`` to prevent committing your API key!

Use with python-dotenv:

.. code-block:: bash

   pip install python-dotenv

.. code-block:: python

   from dotenv import load_dotenv
   load_dotenv()

   import os
   from python_cimis import CimisClient

   client = CimisClient(app_key=os.getenv('CIMIS_API_KEY'))

Verification
------------

Test your installation with this script:

.. code-block:: python

   #!/usr/bin/env python3
   """Test script to verify Python CIMIS Client installation."""

   import os
   from datetime import date, timedelta
   from python_cimis import CimisClient

   def test_installation():
       """Test the installation and API key."""
       try:
           # Check API key
           api_key = os.getenv('CIMIS_API_KEY')
           if not api_key:
               print("❌ Error: CIMIS_API_KEY environment variable not set")
               return False
           
           print(f"✅ API key found: {api_key[:8]}...{api_key[-4:]}")
           
           # Initialize client
           client = CimisClient(app_key=api_key)
           print("✅ Client initialized successfully")
           
           # Test station data
           stations = client.get_stations()
           print(f"✅ Retrieved {len(stations)} stations")
           
           # Test weather data
           yesterday = date.today() - timedelta(days=1)
           weather_data = client.get_daily_data(
               targets=[2],
               start_date=yesterday,
               end_date=yesterday
           )
           records = weather_data.get_all_records()
           print(f"✅ Retrieved {len(records)} weather records")
           
           # Test CSV export
           csv_file = client.export_to_csv(weather_data, filename="test_export.csv")
           print(f"✅ CSV exported to: {csv_file}")
           
           print("\\n🎉 All tests passed! Your installation is working correctly.")
           return True
           
       except Exception as e:
           print(f"❌ Error: {e}")
           return False

   if __name__ == "__main__":
       success = test_installation()
       exit(0 if success else 1)

Save this as ``test_installation.py`` and run:

.. code-block:: bash

   python test_installation.py

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Permission Denied**

.. code-block:: text

   ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied

*Solutions:*

.. code-block:: bash

   # Option 1: Use --user flag
   pip install --user python-CIMIS

   # Option 2: Use virtual environment (recommended)
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   pip install python-CIMIS

**Python Version Incompatibility**

.. code-block:: text

   ERROR: python-CIMIS requires Python '>=3.8' but the running Python is 3.7.x

*Solution:* Install Python 3.8 or higher from `python.org <https://www.python.org/downloads/>`_

**SSL Certificate Issues**

.. code-block:: text

   SSL: CERTIFICATE_VERIFY_FAILED

*Solutions:*

.. code-block:: bash

   # Update certificates (macOS)
   /Applications/Python\\ 3.11/Install\\ Certificates.command

   # Upgrade pip and certificates
   pip install --upgrade pip certifi

**Invalid API Key**

.. code-block:: text

   CimisAuthenticationError: Invalid API key

*Solutions:*

1. Verify your API key is correct (check for extra spaces)
2. Ensure your CIMIS account is active
3. Regenerate your API key on the CIMIS website
4. Check environment variable is set correctly

Getting Help
~~~~~~~~~~~~

- **Documentation**: Check this documentation and the API reference
- **GitHub Issues**: Report bugs at the `GitHub repository <https://github.com/python-cimis/python-cimis-client/issues>`_
- **Examples**: See the `examples directory <https://github.com/python-cimis/python-cimis-client/tree/main/examples>`_
- **CIMIS Official**: Visit the `CIMIS website <https://et.water.ca.gov/Rest/Index>`_ for API documentation
