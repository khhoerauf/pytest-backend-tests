from dotenv import load_dotenv
import os

load_dotenv()

API_HOST = "https://reqres.in/api"
API_KEY = {"x-api-key": os.getenv("API_KEY")}

# Centralized endpoint definitions
ENDPOINTS = {
    "login": f"{API_HOST}/login",
    "register": f"{API_HOST}/register",
    "users": f"{API_HOST}/users",
    "unknown": f"{API_HOST}/unknown",
}

LOGIN_ENDPOINT = ENDPOINTS["login"]
REGISTER_ENDPOINT = ENDPOINTS["register"]
USERS_ENDPOINT = ENDPOINTS["users"]
UNKNOWN_ENDPOINT = ENDPOINTS["unknown"]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<a href=javascript:alert('XSS')>Click me</a>",
    "><script>alert(1)</script>",
    "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",
]
