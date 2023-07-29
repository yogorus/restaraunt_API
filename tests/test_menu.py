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
    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def get_updated_menu_by_id(patch_menu):
    response = client.get(f"{base_url}/menus/{patch_menu['id']}")
    response_json = response.json()
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

    assert response_json["id"] == patch_menu["id"]
    assert response_json["title"] == patch_menu["title"]
    assert response_json["description"] == patch_menu["description"]

    yield response_json


@pytest.fixture(scope="session")
def delete_menu(get_updated_menu_by_id):
    response = client.delete(f"{base_url}/menus/{get_updated_menu_by_id['id']}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    yield response.json()


def test_menu_root():
    response = client.get(f"{base_url}/menus")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert response.json() == []


def test_response_contains_id(create_menu):
    assert "id" in create_menu
    assert type(create_menu["id"]) == str


def test_response_contains_title(create_menu):
    assert "title" in create_menu
    assert type(create_menu["title"]) == str


def test_response_contains_description(create_menu):
    assert "description" in create_menu
    assert type(create_menu["description"]) == str


def test_menu_root_is_not_empty(create_menu):
    response = client.get(f"{base_url}/menus")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_menu_id(get_menu_by_id, create_menu):
    assert "id" in get_menu_by_id
    assert type(get_menu_by_id["id"]) == str
    assert get_menu_by_id["id"] == create_menu["id"]


def test_menu_title(get_menu_by_id, create_menu):
    assert "title" in get_menu_by_id
    assert type(get_menu_by_id["title"]) == str
    assert get_menu_by_id["title"] == create_menu["title"]


def test_menu_description(get_menu_by_id, create_menu):
    assert "description" in get_menu_by_id
    assert type(get_menu_by_id["description"]) == str
    assert get_menu_by_id["description"] == create_menu["description"]


def test_patched_menu_id(patch_menu, get_menu_by_id):
    assert "id" in patch_menu
    assert type(patch_menu["id"]) == str
    assert patch_menu["id"] == get_menu_by_id["id"]


def test_patched_menu_title(patch_menu, get_menu_by_id):
    assert "title" in patch_menu
    assert type(patch_menu["title"]) == str
    assert patch_menu["title"] != get_menu_by_id["title"]


def test_patched_menu_description(patch_menu, get_menu_by_id):
    assert "description" in patch_menu
    assert type(patch_menu["description"]) == str
    assert patch_menu["description"] != get_menu_by_id["description"]


def test_updated_menu_contains_id(get_updated_menu_by_id):
    assert "id" in get_updated_menu_by_id


def test_updated_menu_contains_title(get_updated_menu_by_id):
    assert "title" in get_updated_menu_by_id


def test_updated_menu_contains_description(get_updated_menu_by_id):
    assert "description" in get_updated_menu_by_id


def test_menu_list_after_delete(delete_menu):
    response = client.get(f"{base_url}/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_menu_by_id_after_delete(delete_menu, get_updated_menu_by_id):
    response = client.get(f"{base_url}/menus/{get_updated_menu_by_id['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"
