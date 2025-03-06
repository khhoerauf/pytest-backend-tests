API_HOST = "https://reqres.in/api"
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<a href=javascript:alert('XSS')>Click me</a>",
    "><script>alert(1)</script>",
    "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",
]
