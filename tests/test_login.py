import pytest
import requests
from http import HTTPStatus
from tests.helpers.constants import LOGIN_ENDPOINT, API_KEY, XSS_PAYLOADS

ENDPOINT = LOGIN_ENDPOINT


@pytest.mark.login
class TestLoginApi:

    def test_post_login_with_payload_success(self):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["token"] is not None

    def test_post_login_without_password_unsuccessful(self):
        payload = {"email": "eve.holt@reqres.in"}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Missing password"

    def test_post_login_without_email_unsuccessful(self):
        payload = {"password": "cityslicka"}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Missing email or username"

    def test_post_login_incorrect_email_unsuccessful(self):
        payload = {"email": "eve.holt", "password": "cityslicka"}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "user not found"

    @pytest.mark.parametrize(
        "password",
        [
            "",
            None,
        ],
    )
    def test_post_login_password_validation_success(self, password):
        payload = {"email": "eve.holt@reqres.in", "password": password}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        "password",
        [" ", "##$$$***???!!!"],
    )
    def test_post_login_password_validation_unsuccessful(self, password):
        payload = {"email": "eve.holt@reqres.in", "password": password}
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.xss
    @pytest.mark.parametrize("xss_payload", XSS_PAYLOADS)
    def test_xss_rejection_in_email_field(self, xss_payload):
        payload = {
            "email": xss_payload,
            "password": "password",
        }
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)

        # Check if API allows XSS payloads (it should NOT)
        assert response.status_code in [
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
        ], f"Unexpected status {response.status_code}, API should reject XSS payloads!"

    @pytest.mark.xss
    @pytest.mark.parametrize("xss_payload", XSS_PAYLOADS)
    def _test_xss_rejection_in_password_field(self, xss_payload):
        payload = {
            "email": "eve.holt@reqres.in",
            "password": xss_payload,
        }
        response = requests.post(url=f"{ENDPOINT}", json=payload, headers=API_KEY)

        # Check if API allows XSS payloads (it should NOT)
        assert response.status_code in [
            HTTPStatus.BAD_REQUEST,
            HTTPStatus.UNAUTHORIZED,
        ], f"Unexpected status {response.status_code}, API should reject XSS payloads!"
