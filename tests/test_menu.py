import pytest
from tests.conftest import client

base_url = "localhost:8000/api/v1/menus/"


def test_menu_root():
    response = client.get(f"{base_url}/")
    assert response.status_code == 200
    assert response.json == []
    # assert 1 == 1
