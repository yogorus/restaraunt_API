import pytest
from tests.conftest import client

from tests.test_menu import create_menu, delete_menu

base_url = "http://localhost/api/v1"


@pytest.fixture(scope="session")
def create_submenu(create_menu):
    sent_json = {"title": "My submenu 1", "description": "My submenu description 1"}
    response = client.post(
        f"{base_url}/menus/{create_menu['id']}/submenus/", json=sent_json
    )
    assert response.status_code == 201
    response_json = response.json()
    assert "id" in response_json
    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def patch_submenu(create_menu, create_submenu):
    sent_json = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }
    response = client.patch(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}",
        json=sent_json,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]
    assert response_json["id"] == create_submenu["id"]

    yield response_json


@pytest.fixture(scope="session")
def get_updated_submenu(create_menu, patch_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{patch_submenu['id']}"
    )
    response_json = response.json()
    assert response_json == patch_submenu

    yield response_json


@pytest.fixture(scope="session")
def delete_submenu(create_menu, get_updated_submenu):
    response = client.delete(
        f"{base_url}/menus/{create_menu['id']}/submenus/{get_updated_submenu['id']}"
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    yield response.json()


def test_emtpy_submenu_list(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_contains_id(create_submenu):
    assert "id" in create_submenu
    assert type(create_submenu["id"]) == str


# def test_submenu_contains_title(create_submenu):
#     assert "title" in create_submenu
#     assert type(create_submenu["title"]) == str

# def test_submenu_contains_description()


def test_submenu_list_after_create(create_menu, create_submenu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_submenu_by_id_after_create(create_menu, create_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    assert response.status_code == 200
    assert response.json() == create_submenu


def test_updated_submenu_by_title(create_submenu, patch_submenu):
    assert create_submenu["title"] != patch_submenu["title"]


def test_updated_submenu_by_description(create_submenu, patch_submenu):
    assert create_submenu["description"] != patch_submenu["description"]


def test_updated_submenu_by_response(create_menu, get_updated_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{get_updated_submenu['id']}"
    )
    assert response.status_code == 200
    assert response.json() == get_updated_submenu


def test_submenu_list_after_delete(delete_submenu, create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_after_delete(delete_submenu, get_updated_submenu, create_menu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{get_updated_submenu['id']}"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_menu_list_after_menu_delete(create_menu):
    response = client.delete(f"{base_url}/menus/{create_menu['id']}")

    response = client.get(f"{base_url}/menus")

    assert response.status_code == 200
    assert response.json() == []
