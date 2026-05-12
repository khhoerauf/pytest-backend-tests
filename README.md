# API Test Suite with PyTest & JMeter

This repository provides a framework for both functional and performance testing of a real API from https://reqres.in.

Functional API tests are managed by [`pytest`](https://docs.pytest.org/en/7.4.x/), using the [`requests`](https://pypi.org/project/requests/) package to send HTTP requests and [`HTTPStatus`](https://docs.python.org/3/library/http.html) to validate response codes.

Performance tests are written in [Apache JMeter](https://jmeter.apache.org/), validating response times, throughput, and error rates under concurrent load across all API endpoints.

## Table of Contents

- [Folder Structure](#folder-structure)
- [Local Development](#local-development)
- [Run Tests](#run-tests)
- [Performance Testing](#performance-testing)
- [Test Strategy](#test-strategy)

## Folder Structure

```
pytest-backend-tests/
├── tests/                  # Contains test scripts, following the test_*.py naming convention for pytest.
│    └── helpers/           # Stores reusable utilities like custom assertions and static variables.
│         └── support/      # Holds JSON schemas for validating API responses.
├── jmeter/                 # JMeter performance test plan and results.
│    └── performance-tests.jmx  # JMeter test plan covering all API endpoints.
├── .github/workflows/      # GitHub Actions CI workflows.
├── Makefile                # Defines scripts for running tests, setting up environments etc.
└── requirements.txt        # Lists dependencies for setting up the test environment.
```
## Local Development

1. Environment Variables:
   - This project uses environment variable `API_KEY`. The API key used for authenticated requests, you can get free API key [here](https://app.reqres.in/signup).
   - **Note:** the free tier allows **250 requests per day**. Running both the functional and performance test suites in full will consume the entire daily quota. Consider reducing loops or threads when running performance tests locally on a free account.
   - Create a file named `.env` in the root of your project and add the following:

       ```env
       API_KEY=your_actual_api_key_here
       ```
2. Please ensure that [`Makefile`](https://makefiletutorial.com) is installed on your local machine before proceeding.
3. Install the virtual environment by running:
   ```
    make install-virtual-environment
   ```
4. Install dependencies by running: 
    ```
    make install-dependencies
    ```
## Run tests

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

## Performance Testing

Performance tests are written in [Apache JMeter](https://jmeter.apache.org/) and cover all four API endpoints: `/users`, `/login`, `/register`, and `/unknown`.

Each request is validated for:
- Correct HTTP status code
- Expected response body structure (JSON path assertions)
- Response time within the configured threshold (default: 2000ms)

### Prerequisites

Install JMeter via Homebrew:

```bash
brew install jmeter
```

### Run performance tests

```bash
make performance-tests
```

This runs the test plan with default settings: **10 threads**, **5s ramp-up**, **5 loops**, **500ms think time**, **2000ms response threshold**.

### Override default parameters

All parameters can be overridden from the command line without editing the test plan:

```bash
jmeter -n \
  -t jmeter/performance-tests.jmx \
  -l jmeter/results/results.jtl \
  -e -o jmeter/results/report \
  -Japi_key=$API_KEY \
  -Jthreads=20 \
  -Jramp_time=10 \
  -Jloops=10 \
  -Jthink_time=1000 \
  -Jduration_threshold=3000
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | _(empty)_ | API key passed as `x-api-key` header |
| `base_url` | `reqres.in` | Target host — useful for pointing at staging |
| `threads` | `10` | Number of concurrent virtual users |
| `ramp_time` | `5` | Seconds to ramp up to full thread count |
| `loops` | `5` | Number of iterations per thread |
| `think_time` | `500` | Milliseconds to wait between requests |
| `duration_threshold` | `2000` | Max acceptable response time in ms |

### View the HTML report

After a test run, open the generated report in your browser:

```bash
make performance-tests-report
```

The report includes throughput graphs, response time percentiles, and a per-request breakdown.

### Clean results

```bash
make performance-tests-clean
```

### CI / GitHub Actions

Performance tests run automatically every **Monday at 06:00 UTC** via the [`performance-tests`](.github/workflows/performance-tests.yml) workflow. They can also be triggered manually from the **Actions** tab using `workflow_dispatch`.

After each run, two artifacts are available for download:
- `jmeter-jtl` — raw results file
- `jmeter-html-report` — full interactive HTML report

A summary table with total requests, pass/fail counts, error rate, and avg/min/max response times is written directly to the GitHub Actions step summary.
