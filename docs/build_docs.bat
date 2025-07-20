@echo off
REM Documentation build script for the Python CIMIS Client (Windows)

echo Building Python CIMIS Client Documentation...

REM Navigate to the docs directory
cd /d "%~dp0"

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing documentation dependencies...
    pip install -r requirements.txt
)

REM Build the documentation
echo Building HTML documentation...
sphinx-build -b html source build

echo Documentation built successfully!
echo Open build\index.html in your browser to view the documentation.
