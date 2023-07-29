import pytest
from tests.conftest import client

base_url = "http://localhost/api/v1"


@pytest.fixture(scope="session")
def create_menu():
    sent_json = {"title": "My menu 1", "description": "My menu description 1"}
    response = client.post(f"{base_url}/menus", json=sent_json)
    response_json = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 201
    assert "id" in response_json
    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def get_menu_by_id(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}")
    response_json = response.json()
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

    yield response_json


@pytest.fixture(scope="session")
def patch_menu(get_menu_by_id):
    sent_json = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }
    response = client.patch(f"{base_url}/menus/{get_menu_by_id['id']}", json=sent_json)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_json = response.json()
    assert get_menu_by_id["id"] == response_json["id"]
    assert get_menu_by_id["title"] != response_json["title"]
    assert get_menu_by_id["description"] != response_json["description"]

    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def delete_menu(patch_menu):
    response = client.delete(f"{base_url}/menus/{patch_menu['id']}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    yield {"id": patch_menu["id"]}


# Empty db
def test_menu_root():
    response = client.get(f"{base_url}/menus")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert response.json() == []


# After creation
def test_menu_root_is_not_empty(create_menu):
    response = client.get(f"{base_url}/menus")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_menu_response_after_create(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}")
    assert response.json() == create_menu


# After patch
def test_updated_menu_response(patch_menu):
    response = client.get(f"{base_url}/menus/{patch_menu['id']}")
    assert response.status_code == 200
    assert response.json() == patch_menu


# After delete
def test_menu_list_after_delete(delete_menu):
    response = client.get(f"{base_url}/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_menu_by_id_after_delete(delete_menu):
    response = client.get(f"{base_url}/menus/{delete_menu['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"
