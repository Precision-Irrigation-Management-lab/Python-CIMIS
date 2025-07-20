Contributing
============

Thank you for your interest in contributing to the Python CIMIS Client library! 

Development Setup
-----------------

1. **Fork and Clone**::

    git clone https://github.com/yourusername/python-cimis-client.git
    cd python-cimis-client

2. **Create Virtual Environment**::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**::

    pip install -e .[dev]

4. **Run Tests**::

    pytest

Contributing Guidelines
-----------------------

- Follow PEP 8 coding standards
- Write comprehensive tests for new features
- Update documentation for any API changes
- Use meaningful commit messages
- Create feature branches for new development

Testing
-------

Run the test suite::

    pytest tests/

For coverage reports::

    pytest --cov=python_cimis tests/

Documentation
-------------

Build documentation locally::

    cd docs
    make html

The documentation uses Sphinx with the Read the Docs theme.

Pull Request Process
--------------------

1. Create a feature branch from main
2. Make your changes
3. Add or update tests
4. Update documentation if needed
5. Ensure all tests pass
6. Submit a pull request

For detailed contributing guidelines, see the `CONTRIBUTING.md <https://github.com/python-cimis/python-cimis-client/blob/main/CONTRIBUTING.md>`_ file in the repository.
