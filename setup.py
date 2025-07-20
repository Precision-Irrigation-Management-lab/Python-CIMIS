"""
Setup script for python-cimis package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="python-CIMIS",
    version="1.0.0",
    author="Mahipal Reddy Ramireddy, M. A. Andrade",
    author_email="mahipalbablu16@gmail.com",
    maintainer="Precision Irrigation Management Lab (PRIMA)",
    description="A comprehensive Python client for the California Irrigation Management Information System (CIMIS) API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/python-cimis/python-cimis-client",
    project_urls={
        "Bug Reports": "https://github.com/python-cimis/python-cimis-client/issues",
        "Source": "https://github.com/python-cimis/python-cimis-client",
        "Documentation": "https://python-cimis-client.readthedocs.io/",
        "ReadTheDocs": "https://python-cimis-client.readthedocs.io/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    keywords="cimis weather california irrigation agriculture climate data api",
    include_package_data=True,
    zip_safe=False,
)