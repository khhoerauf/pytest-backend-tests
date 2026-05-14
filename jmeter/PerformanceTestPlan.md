# Performance Test Plan
SME (Subject Matter Expert): @khhoerauf

---

## Test Project Overview

This performance test plan covers the [reqres.in](https://reqres.in) REST API, which is used as the target system for this test suite. The goal is to validate that the API meets acceptable response time and reliability standards under concurrent load.

Tests are implemented in [Apache JMeter 5.6.3](https://jmeter.apache.org/) and executed via the `make performance-tests` command locally, or automatically via the GitHub Actions `performance-tests` workflow.

**Target API:** `https://reqres.in/api`  
**Endpoints under test:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users` | GET | List users (paginated) |
| `/api/users/2` | GET | Get single user |
| `/api/login` | POST | Authenticate a user |
| `/api/register` | POST | Register a new user |
| `/api/unknown` | GET | List unknown resources |

---

## Test Objectives

- Verify that all endpoints respond within **2000ms** under normal concurrent load
- Confirm **0% error rate** across all requests during load and spike scenarios
- Validate that response bodies contain the expected data structure under load (not just correct status codes)
- Establish a baseline for average, min, and max response times to detect regressions in future runs
- Ensure the API handles a sudden spike in traffic without returning errors or timing out

---

## Performance Type

### Load Testing

Simulates a realistic number of concurrent users making repeated requests over a sustained period.

**Goal:** Confirm the API performs consistently under expected production-like traffic.

| Parameter | Value |
|-----------|-------|
| Virtual users (threads) | 10 |
| Ramp-up time | 5 seconds |
| Iterations per user (loops) | 5 |
| Think time between requests | 500ms |
| Total requests per run | 250 |
| Response time threshold | 2000ms |

**Pass criteria:**
- Error rate = 0%
- All response times ≤ 2000ms
- All JSON path assertions pass (response body structure is valid)

---

### Spike Testing

Simulates a sudden, sharp increase in traffic to verify the API handles bursts without degrading.

**Goal:** Confirm the API recovers gracefully from a sudden surge in concurrent users.

To run a spike test, override the default parameters:

```bash
jmeter -n \
  -t jmeter/performance-tests.jmx \
  -l jmeter/results/results.jtl \
  -e -o jmeter/results/report \
  -Japi_key=$API_KEY \
  -Jthreads=50 \
  -Jramp_time=2 \
  -Jloops=3 \
  -Jthink_time=0 \
  -Jduration_threshold=3000
```

| Parameter | Value |
|-----------|-------|
| Virtual users (threads) | 50 |
| Ramp-up time | 2 seconds |
| Iterations per user (loops) | 3 |
| Think time between requests | 0ms |
| Response time threshold | 3000ms |

**Pass criteria:**
- Error rate = 0%
- All response times ≤ 3000ms
- No connection timeouts or refused connections

---

## Test Environment

| Item | Detail |
|------|--------|
| Tool | Apache JMeter 5.6.3 |
| JDK | OpenJDK 21 |
| Target environment | `https://reqres.in` (shared public API) |
| Authentication | `x-api-key` header |
| API tier | Free — **250 requests/day limit** |
| CI execution | GitHub Actions, Ubuntu latest, scheduled weekly (Mon 06:00 UTC) |

> ⚠️ **Free tier limit:** The reqres.in free plan allows 250 requests per day. A full load test run consumes the entire daily quota. Avoid running load and spike tests on the same day without upgrading the account.

---

## Assertions

Every sampler includes the following assertions:

| Assertion | Type | Detail |
|-----------|------|--------|
| HTTP status code | Response Assertion | Expects `200` |
| Response body structure | JSON Path Assertion | Validates key fields exist (e.g. `$.data`, `$.token`, `$.id`) |
| Response time | Duration Assertion | Must be within `DURATION_THRESHOLD` (default 2000ms) |

---

## Out of Scope

- Stress testing (pushing the API beyond its breaking point)
- Scalability testing (measuring behaviour as infrastructure scales)
- Endurance / soak testing (sustained load over hours)
- Network-level performance (latency, bandwidth)
- Database-level performance
- Testing non-reqres.in environments
