import pytest
import requests
from http import HTTPStatus
from tests.helpers.constants import API_HOST
from tests.helpers.assertions import Assertions

ENDPOINT = f"{API_HOST}/unknown"


@pytest.mark.api
class TestUnknownApi:

    @pytest.mark.parametrize(
        "query, schema",
        [
            ("", "list_unknowns.json"),
            ("/2", "single_unknown.json"),
        ],
    )
    def test_get_users_success(self, query, schema):
        utilis = Assertions()
        response = requests.get(url=f"{ENDPOINT}{query}")
        assert response.status_code == HTTPStatus.OK
        utilis.assert_valid_schema(response.json(), schema)

    def test_get_users_with_query_not_found(self):
        response = requests.get(url=f"{ENDPOINT}/23")
        assert response.status_code == HTTPStatus.NOT_FOUND
