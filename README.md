# Backed Tests with PyTest

This repository provides frameworks for API tests, managed by [`pytest`](https://docs.pytest.org/en/7.4.x/).
Each test call API by [`requests`](https://pypi.org/project/requests/) package which allows easily send requests
and response code status are validated with [`HTTPStatus`](https://docs.python.org/3/library/http.html).

## Table of Contents

- [Folder Structure](#folder-structure)
- [Local Development](#local-development)
- [Test Strategy](#test-strategy)


## Folder Structure

```
pytest-backend-tests/
├── tests/                  # Contains test scripts, following the test_*.py naming convention for pytest.
│    └── helpers/           # Stores reusable utilities like custom assertions and static variables.
│         └── support/      # Holds JSON schemas for validating API responses.
├── Makefile                # Defines scripts for running tests, setting up environments etc.
└── requirements.txt        # Lists dependencies for setting up the test environment.
```

## Local Development

1. Please ensure that [`Makefile`](https://makefiletutorial.com) is installed on your local machine before proceeding.
2. Install the virtual environment by running:
   ```
    make install-virtual-environment
   ```
3. Install  dependencies by running: 
    ```
    make install-dependencies
    ```
   
### Run tests

- Execute all API Tests by running:
    ```commandline
    make api-tests
    ```
   
- Tests are written using the pytest mark feature, which allows you to execute only a selected test suite. 
  For example, to run tests for the login feature, use the following command:
    ```commandline
    pytest -m login
    ```

## Test Strategy
For each request, we should cover following general test scenario groups:
   -  Basic positive tests (happy paths)
     - This check should validate the json schema.
     - The schema can be created with this [tool](https://jsonformatter.org/json-to-jsonschema), all current schemas can be found `tests/helpers/support/schemas`
   - Extended positive testing with optional parameters to check crucial fields in response depending on test case objectives.
   - Negative testing with valid input.
   - Negative testing with invalid input (error handling).
   - Cover Cross-Site Scripting (XSS) attacks, to prevent input from an HTTP request, make its way into the HTML output.