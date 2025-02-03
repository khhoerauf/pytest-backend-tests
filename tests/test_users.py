import pytest
import requests
import time
from http import HTTPStatus
from tests.helpers.constants import API_HOST
from tests.helpers.assertions import Assertions

ENDPOINT = f"{API_HOST}/users"


@pytest.mark.api
class TestUsersApi:
    @pytest.mark.parametrize(
        "query, schema",
        [
            ("", "list_users.json"),
            ("?page=2", "list_users.json"),
            ("/2", "single_user.json"),
        ],
    )
    def test_get_users_success(self, query, schema):
        utilis = Assertions()
        response = requests.get(url=f"{ENDPOINT}{query}")
        assert response.status_code == HTTPStatus.OK
        utilis.assert_valid_schema(response.json(), schema)

    def test_get_users_with_delay_param_success(self):
        utilis = Assertions()
        start_time = time.time()
        response = requests.get(url=f"{ENDPOINT}", params="delay=3")
        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == HTTPStatus.OK
        utilis.assert_valid_schema(response.json(), "list_users.json")
        assert response_time > 3

    def test_get_users_with_query_not_found(self):
        response = requests.get(url=f"{ENDPOINT}/23")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_post_users_without_payload_success(self):
        response = requests.post(url=f"{ENDPOINT}/2")
        assert response.status_code == HTTPStatus.CREATED

    def test_post_users_with_payload_success(self):
        payload = {"name": "morpheus", "job": "leader"}
        response = requests.post(url=f"{ENDPOINT}/2", data=payload)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["name"] == payload["name"]
        assert response.json()["job"] == payload["job"]

    def test_delete_users_success(self):
        response = requests.delete(url=f"{ENDPOINT}/2")
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_put_users_success(self):
        response = requests.put(url=f"{ENDPOINT}/2")
        assert response.status_code == HTTPStatus.OK

    def test_patch_users_success(self):
        response = requests.patch(url=f"{ENDPOINT}/2")
        assert response.status_code == HTTPStatus.OK
