import pytest
import requests
from http import HTTPStatus
from tests.helpers.constants import API_HOST

ENDPOINT = f"{API_HOST}/register"


@pytest.mark.api
class TestRegisterApi:

    def test_post_register_with_payload_success(self):
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["token"] is not None

    def test_post_register_without_password_unsuccessful(self):
        payload = {"email": "morpheus"}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Missing password"

    def test_post_register_without_email_unsuccessful(self):
        payload = {"password": "pistol"}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Missing email or username"

    def test_post_register_incorrect_email_unsuccessful(self):
        payload = {"email": "eve.holt", "password": "pistol"}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["error"] == "Note: Only defined users succeed registration"
        )

    @pytest.mark.parametrize(
        "password",
        [
            "",
            None,
        ],
    )
    def test_post_register_password_validation_success(self, password):
        payload = {"email": "eve.holt@reqres.in", "password": password}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        "password",
        [" ", "##$$$***???!!!"],
    )
    def test_post_register_password_validation_unsuccessful(self, password):
        payload = {"email": "eve.holt@reqres.in", "password": password}
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.OK

    def test_post_register_password_with_xss_attack(self):
        payload = {
            "email": "eve.holt@reqres.in",
            "password": "<script>alert('XSS')</script>",
        }
        response = requests.post(url=f"{ENDPOINT}", data=payload)
        assert response.status_code == HTTPStatus.OK
