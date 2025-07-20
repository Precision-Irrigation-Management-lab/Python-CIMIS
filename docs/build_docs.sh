#!/bin/bash
# Documentation build script for the Python CIMIS Client

# Exit on any error
set -e

echo "Building Python CIMIS Client Documentation..."

# Navigate to the docs directory
cd "$(dirname "$0")"

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing documentation dependencies..."
    pip install -r requirements.txt
fi

# Build the documentation
echo "Building HTML documentation..."
sphinx-build -b html source build

echo "Documentation built successfully!"
echo "Open build/index.html in your browser to view the documentation."
