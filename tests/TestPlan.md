# Integration Test Plan
SME (Subject Matter Expert): @khhoerauf

---

## Test Project Overview

This test plan covers integration testing of the [reqres.in](https://reqres.in) REST API. Tests are implemented in Python using [`pytest`](https://docs.pytest.org/en/7.4.x/) and validate the full HTTP request/response cycle for each endpoint — including status codes, response body structure, field values, and security behaviour.

**Target API:** `https://reqres.in/api`  
**Test file location:** `tests/`  
**Run command:** `make api-tests`

---

## Test Objectives

- Verify each endpoint returns the correct HTTP status code for both valid and invalid inputs
- Validate response body structure against JSON schemas for all successful responses
- Confirm error responses return meaningful, correctly structured error messages
- Ensure the API rejects missing or malformed required fields with `400 Bad Request`
- Validate that XSS payloads in input fields are rejected and do not pass through

---

## Endpoints Under Test

| Endpoint | Method | Pytest Mark | Test File |
|----------|--------|-------------|-----------|
| `/api/users` | GET, POST, PUT, PATCH, DELETE | `users` | `test_users.py` |
| `/api/login` | POST | `login` | `test_login.py` |
| `/api/register` | POST | `register` | `test_register.py` |
| `/api/unknown` | GET | `unknown` | `test_unknown.py` |

---

## Test Cases

### GET /api/users

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 1 | List users — default page | No query params | `200 OK`, body matches `list_users.json` schema | ✅ Implemented |
| 2 | List users — page 2 | `?page=2` | `200 OK`, body matches `list_users.json` schema | ✅ Implemented |
| 3 | Get single user | `/2` | `200 OK`, body matches `single_user.json` schema | ✅ Implemented |
| 4 | Get user with delay param | `?delay=3` | `200 OK`, response time > 3s, schema valid | ✅ Implemented |
| 5 | Get non-existent user | `/23` | `404 Not Found` | ✅ Implemented |

### POST /api/users

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 6 | Create user without payload | No body | `201 Created` | ✅ Implemented |
| 7 | Create user with payload | `name`, `job` fields | `201 Created`, response contains `name` and `job` | ✅ Implemented |

### PUT / PATCH / DELETE /api/users

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 8 | Full update user | PUT `/2` | `200 OK` | ✅ Implemented |
| 9 | Partial update user | PATCH `/2` | `200 OK` | ✅ Implemented |
| 10 | Delete user | DELETE `/2` | `204 No Content` | ✅ Implemented |

---

### POST /api/login

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 11 | Successful login | Valid `email` + `password` | `200 OK`, `token` present in response | ✅ Implemented |
| 12 | Missing password | `email` only | `400 Bad Request`, `error: "Missing password"` | ✅ Implemented |
| 13 | Missing email | `password` only | `400 Bad Request`, `error: "Missing email or username"` | ✅ Implemented |
| 14 | Invalid email format | `email: "eve.holt"` | `400 Bad Request`, `error: "user not found"` | ✅ Implemented |
| 15 | Empty password | `password: ""` | `400 Bad Request` | ✅ Implemented |
| 16 | Null password | `password: null` | `400 Bad Request` | ✅ Implemented |
| 17 | Whitespace password | `password: " "` | `200 OK` (API accepts it) | ✅ Implemented |
| 18 | Special characters password | `password: "##$$$***???!!!"` | `200 OK` (API accepts it) | ✅ Implemented |
| 19 | XSS payload in email field | 6 XSS variants | `400` or `401` — payload must be rejected | ✅ Implemented |
| 20 | XSS payload in password field | 6 XSS variants | `400` or `401` — payload must be rejected | ⚠️ Skipped (prefixed `_test`) |

---

### POST /api/register

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 21 | Successful registration | Valid `email` + `password` | `200 OK`, `token` and `id` present in response | ✅ Implemented |
| 22 | Missing password | `email` only | `400 Bad Request`, `error: "Missing password"` | ✅ Implemented |
| 23 | Missing email | `password` only | `400 Bad Request`, `error: "Missing email or username"` | ✅ Implemented |
| 24 | Unregistered email | `email: "eve.holt"` | `400 Bad Request`, `error: "Note: Only defined users succeed registration"` | ✅ Implemented |
| 25 | Empty password | `password: ""` | `400 Bad Request` | ✅ Implemented |
| 26 | Null password | `password: null` | `400 Bad Request` | ✅ Implemented |
| 27 | Whitespace password | `password: " "` | `200 OK` (API accepts it) | ✅ Implemented |
| 28 | Special characters password | `password: "##$$$***???!!!"` | `200 OK` (API accepts it) | ✅ Implemented |
| 29 | XSS payload in email field | 6 XSS variants | `400` or `401` — payload must be rejected | ✅ Implemented |
| 30 | XSS payload in password field | 6 XSS variants | `400` or `401` — payload must be rejected | ⚠️ Skipped (prefixed `_test`) |

---

### GET /api/unknown

| # | Test Case | Input | Expected Result | Status |
|---|-----------|-------|-----------------|--------|
| 31 | List unknown resources | No query params | `200 OK`, body matches `list_unknowns.json` schema | ✅ Implemented |
| 32 | Get single unknown resource | `/2` | `200 OK`, body matches `single_unknown.json` schema | ✅ Implemented |
| 33 | Get non-existent resource | `/23` | `404 Not Found` | ✅ Implemented |

---

## Assertions

| Type | Detail |
|------|--------|
| HTTP status code | Validated using `HTTPStatus` enum on every test |
| JSON schema | Validated against schemas in `tests/helpers/support/schemas/` using `jsonschema` |
| Response field values | Key fields asserted directly (e.g. `token`, `name`, `job`, `error` message text) |
| Response time | Validated in delay test — asserts response time > 3s when `?delay=3` is used |
| XSS rejection | Asserts status is `400` or `401` when XSS payloads are submitted |

---

## How to Run

Run all integration tests:
```bash
make api-tests
```

Run a specific suite by mark:
```bash
pytest -m login
pytest -m register
pytest -m users
pytest -m unknown
pytest -m xss
```

Run with verbose output:
```bash
pytest -v
```

---

## Known Issues / Gaps

| # | Description |
|---|-------------|
| 1 | XSS tests for the **password field** in both `/login` and `/register` are skipped — the test methods are prefixed with `_test` instead of `test_`, so pytest does not collect them. The API currently returns `200 OK` for XSS payloads in the password field, which may be acceptable depending on server-side sanitisation. |
| 2 | Whitespace and special character passwords (`" "`, `"##$$$***???!!!"`) return `200 OK` — this is documented as observed behaviour, not necessarily a defect, but worth reviewing with the API owner. |
| 3 | No tests currently cover pagination boundary conditions (e.g. `?page=0`, `?page=999`). |
| 4 | No tests cover invalid HTTP methods (e.g. DELETE on `/api/login`). |

---

## Out of Scope

- Performance and load testing (covered separately in `jmeter/PerformanceTestPlan.md`)
- UI / end-to-end testing
- Database-level validation
- Authentication token expiry and refresh flows
- Rate limiting behaviour
