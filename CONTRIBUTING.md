# Contributing to Python CIMIS Client

Thank you for your interest in contributing to the Python CIMIS Client library! This document provides guidelines and information for contributors.

**Project Maintainers:**
- Mahipal Reddy Ramireddy
- M. A. Andrade  
- Precision Irrigation Management Lab (PRIMA)

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Release Process](#release-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background, experience level, or personal characteristics.

### Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Public or private harassment
- Publishing others' private information without permission
- Other conduct that could reasonably be considered inappropriate

### Enforcement

Project maintainers are responsible for clarifying standards and taking appropriate action in response to unacceptable behavior. Report issues to the project maintainers.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A CIMIS API key for testing
- Basic familiarity with pytest and Python development

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/python-cimis-client.git
   cd python-cimis-client
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/python-cimis/python-cimis-client.git
   ```

---

## Development Setup

### Create Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev,docs]"
```

### Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

### Environment Variables

Create a `.env` file for development:

```bash
# .env
CIMIS_API_KEY=your-test-api-key-here
```

**Note:** Never commit your API key to the repository!

---

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

#### 🐛 Bug Reports
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS information

#### ✨ Feature Requests
- Clear description of the proposed feature
- Use case and justification
- Suggested implementation approach
- Backwards compatibility considerations

#### 📝 Documentation
- API documentation improvements
- User guide enhancements
- Example code and tutorials
- README updates

#### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code quality enhancements

### Coding Standards

#### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **String quotes**: Use double quotes for strings, single quotes for single characters
- **Import organization**: Follow isort configuration

#### Code Formatting

We use several tools to maintain code quality:

```bash
# Format code with Black
black python_cimis/ tests/ examples/

# Sort imports with isort
isort python_cimis/ tests/ examples/

# Lint with flake8
flake8 python_cimis/ tests/

# Type check with mypy
mypy python_cimis/
```

#### Naming Conventions

- **Classes**: PascalCase (`CimisClient`, `WeatherData`)
- **Functions/Methods**: snake_case (`get_daily_data`, `export_to_csv`)
- **Variables**: snake_case (`weather_data`, `station_id`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT`, `API_BASE_URL`)
- **Private methods**: Leading underscore (`_validate_dates`, `_build_url`)

### Documentation Standards

#### Docstrings

Use Google-style docstrings:

```python
def get_daily_data(
    self,
    targets: List[Union[int, str]],
    start_date: Union[str, date],
    end_date: Union[str, date],
    data_items: Optional[List[str]] = None,
    unit_of_measure: str = "Metric",
    prioritize_scs: bool = False
) -> WeatherData:
    """Retrieve daily weather data from CIMIS stations.
    
    Args:
        targets: List of station numbers, zip codes, coordinates, or addresses.
        start_date: Start date in YYYY-MM-DD format or date object.
        end_date: End date in YYYY-MM-DD format or date object.
        data_items: Specific data items to retrieve. If None, retrieves all available.
        unit_of_measure: Unit system - "Metric" for Metric (default), "English" for English.
        prioritize_scs: Whether to prioritize Spatial CIMIS System data.
        
    Returns:
        WeatherData object containing the API response.
        
    Raises:
        CimisAPIError: If the API returns an error.
        CimisConnectionError: If connection to the API fails.
        CimisAuthenticationError: If the API key is invalid.
        
    Example:
        >>> client = CimisClient(app_key="your-key")
        >>> weather_data = client.get_daily_data(
        ...     targets=[2, 8],
        ...     start_date="2023-01-01",
        ...     end_date="2023-01-07"
        ... )
        >>> print(len(weather_data.get_all_records()))
        14
    """
```

#### Type Hints

All public APIs must include comprehensive type hints:

```python
from typing import List, Optional, Union, Dict, Any
from datetime import date

def process_weather_data(
    weather_data: WeatherData,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Union[str, float]]]:
    """Process weather data with optional filters."""
    pass
```

---

## Testing

### Test Structure

Our test suite is organized as follows:

```
tests/
├── __init__.py
├── test_client.py          # CimisClient tests
├── test_endpoints.py       # Endpoint management tests
├── test_exceptions.py      # Exception handling tests
├── test_integration.py     # Integration tests (require API key)
├── test_models.py          # Data model tests
└── test_utils.py          # Utility function tests
```

### Writing Tests

#### Unit Tests

Use pytest with clear, descriptive test names:

```python
import pytest
from unittest.mock import Mock, patch
from python_cimis import CimisClient
from python_cimis.exceptions import CimisAPIError

class TestCimisClient:
    def test_init_with_valid_api_key(self):
        """Test client initialization with valid API key."""
        client = CimisClient(app_key="test-key")
        assert client.app_key == "test-key"
        assert client.timeout == 30  # default
    
    def test_init_with_custom_timeout(self):
        """Test client initialization with custom timeout."""
        client = CimisClient(app_key="test-key", timeout=60)
        assert client.timeout == 60
    
    @patch('python_cimis.client.requests.get')
    def test_get_daily_data_success(self, mock_get):
        """Test successful daily data retrieval."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Data": {"Providers": []}
        }
        mock_get.return_value = mock_response
        
        # Test
        client = CimisClient(app_key="test-key")
        result = client.get_daily_data(
            targets=[2],
            start_date="2023-01-01",
            end_date="2023-01-07"
        )
        
        # Assertions
        assert result is not None
        mock_get.assert_called_once()
    
    @patch('python_cimis.client.requests.get')
    def test_get_daily_data_api_error(self, mock_get):
        """Test API error handling in daily data retrieval."""
        # Setup mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "Errors": [{"Message": "Invalid station"}]
        }
        mock_get.return_value = mock_response
        
        # Test
        client = CimisClient(app_key="test-key")
        with pytest.raises(CimisAPIError, match="Invalid station"):
            client.get_daily_data(
                targets=[999999],
                start_date="2023-01-01",
                end_date="2023-01-07"
            )
```

#### Integration Tests

Integration tests require a valid API key:

```python
import os
import pytest
from datetime import date, timedelta
from python_cimis import CimisClient

@pytest.mark.integration
class TestCimisIntegration:
    @pytest.fixture
    def client(self):
        """Create client for integration tests."""
        api_key = os.getenv('CIMIS_API_KEY')
        if not api_key:
            pytest.skip("CIMIS_API_KEY not set")
        return CimisClient(app_key=api_key)
    
    def test_get_stations_integration(self, client):
        """Test actual stations retrieval."""
        stations = client.get_stations()
        assert len(stations) > 0
        assert all(hasattr(s, 'station_nbr') for s in stations)
    
    def test_get_daily_data_integration(self, client):
        """Test actual daily data retrieval."""
        end_date = date.today() - timedelta(days=2)
        start_date = end_date - timedelta(days=1)
        
        weather_data = client.get_daily_data(
            targets=[2],
            start_date=start_date,
            end_date=end_date
        )
        
        records = weather_data.get_all_records()
        assert len(records) >= 1
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run with coverage
pytest --cov=python_cimis --cov-report=html

# Run only unit tests (skip integration)
pytest -m "not integration"

# Run only integration tests
pytest -m integration

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_client.py::TestCimisClient::test_init_with_valid_api_key
```

### Test Coverage

Maintain test coverage above 90%. Check coverage with:

```bash
pytest --cov=python_cimis --cov-report=term-missing
```

### Mock Guidelines

- Mock external dependencies (HTTP requests, file system)
- Use descriptive mock names
- Verify mock interactions
- Test both success and failure scenarios

---

## Documentation

### Types of Documentation

#### API Reference
- Complete method documentation
- Parameter descriptions
- Return value specifications
- Exception documentation
- Usage examples

#### User Guide
- Comprehensive usage patterns
- Best practices
- Integration examples
- Troubleshooting guides

#### Examples
- Basic usage examples
- Advanced use cases
- Real-world applications
- Integration patterns

### Documentation Tools

We use several tools for documentation:

- **Docstrings**: In-code documentation
- **Markdown**: README, guides, and reference docs
- **Sphinx**: Generated API documentation (future)

### Writing Guidelines

#### README Updates

When adding features, update the README.md:
- Add to feature list if it's a major feature
- Update usage examples if API changes
- Add to installation instructions if dependencies change

#### Example Code

All example code should:
- Be tested and verified to work
- Include necessary imports
- Use realistic data and scenarios
- Include error handling where appropriate
- Be well-commented

```python
#!/usr/bin/env python3
"""
Example: Basic Weather Data Retrieval

This example demonstrates how to retrieve daily weather data
from CIMIS stations and export it to CSV.
"""

import os
from datetime import date, timedelta
from python_cimis import CimisClient
from python_cimis.exceptions import CimisAPIError

def main():
    # Initialize client with API key from environment
    api_key = os.getenv('CIMIS_API_KEY')
    if not api_key:
        print("Error: Please set CIMIS_API_KEY environment variable")
        return
    
    client = CimisClient(app_key=api_key)
    
    try:
        # Get data for the last 7 days
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=6)
        
        weather_data = client.get_daily_data(
            targets=[2, 8],  # Five Points and Blackwells Corner
            start_date=start_date,
            end_date=end_date
        )
        
        # Export to CSV
        csv_file = client.export_to_csv(weather_data)
        print(f"Data exported to: {csv_file}")
        
    except CimisAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
```

---

## Pull Request Process

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write code following our standards
   - Add or update tests
   - Update documentation
   - Commit with clear messages

4. **Run quality checks**:
   ```bash
   # Format code
   black python_cimis/ tests/ examples/
   isort python_cimis/ tests/ examples/
   
   # Run tests
   pytest
   
   # Check types
   mypy python_cimis/
   
   # Lint
   flake8 python_cimis/ tests/
   ```

### Pull Request Template

Use this template for your PR description:

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Added unit tests for new functionality
- [ ] Updated integration tests if needed
- [ ] All tests pass locally
- [ ] Tested with real CIMIS API (if applicable)

## Documentation
- [ ] Updated docstrings for new/modified functions
- [ ] Updated README.md if needed
- [ ] Added/updated examples if needed
- [ ] Updated API reference if needed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Changes generate no new warnings
- [ ] Any dependent changes have been merged

## Additional Notes
Any additional information, dependencies, or notes for reviewers.
```

### Review Process

1. **Automated checks**: All PRs run automated checks (tests, linting, etc.)
2. **Code review**: At least one maintainer will review your code
3. **Discussion**: Address any feedback or questions
4. **Approval**: Once approved, maintainers will merge the PR

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
feat: add support for hourly data retrieval

- Add get_hourly_data method to CimisClient
- Update endpoints to handle hourly data requests
- Add comprehensive tests for hourly data functionality
- Update documentation with hourly data examples

Closes #123
```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

---

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear and concise description of the bug.

**Steps to Reproduce**
1. Initialize client with...
2. Call method...
3. See error...

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- Python version:
- Library version:
- Operating system:
- CIMIS API endpoint (if custom):

**Additional Context**
Any other context about the problem.

**Code Sample**
```python
# Minimal code sample that reproduces the issue
```

### Feature Requests

Use the feature request template:

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Describe your use case and why this feature would be valuable.

**Proposed Solution**
Describe how you envision the feature working.

**Alternatives Considered**
Any alternative solutions or features you've considered.

**Additional Context**
Any other context or screenshots about the feature request.
```

### Issue Labels

We use these labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on

---

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (1.1.0): New features, backwards compatible
- **PATCH** (1.1.1): Bug fixes, backwards compatible

### Release Checklist

For maintainers preparing a release:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite** with latest dependencies
4. **Update documentation** if needed
5. **Create release tag**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
6. **Build and upload to PyPI**:
   ```bash
   python -m build
   twine upload dist/*
   ```
7. **Create GitHub release** with release notes

### Changelog Format

```markdown
# Changelog

## [1.1.0] - 2023-07-20

### Added
- New feature X
- Support for Y

### Changed
- Improved performance of Z
- Updated dependency versions

### Fixed
- Fixed bug in A
- Resolved issue with B

### Deprecated
- Feature C is deprecated

### Removed
- Removed deprecated feature D

### Security
- Fixed security vulnerability in E
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, questions
- **GitHub Discussions**: General discussion, ideas, Q&A
- **Pull Requests**: Code contributions and reviews

### Getting Help

- Check existing issues and documentation first
- Search closed issues for similar problems
- Provide complete information when asking questions
- Be patient and respectful

### Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub repository contributors section

---

## Additional Resources

### Development Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks

### Python Resources

- [PEP 8](https://pep8.org/): Style Guide for Python Code
- [PEP 484](https://pep.python.org/pep-0484/): Type Hints
- [pytest documentation](https://docs.pytest.org/)
- [Semantic Versioning](https://semver.org/)

### CIMIS Resources

- [CIMIS Website](https://cimis.water.ca.gov/)
- [CIMIS API Documentation](https://et.water.ca.gov/Rest/Index)
- [California DWR](https://water.ca.gov/)

---

Thank you for contributing to the Python CIMIS Client library! Your contributions help make this tool more valuable for the agricultural and scientific communities.
