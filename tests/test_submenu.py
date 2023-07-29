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
    assert create_submenu["id"] == create_submenu["id"]
    assert create_submenu["title"] != response_json["title"]
    assert create_submenu["description"] != response_json["description"]

    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def delete_submenu(create_menu, patch_submenu):
    response = client.delete(
        f"{base_url}/menus/{create_menu['id']}/submenus/{patch_submenu['id']}"
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    yield {"id": patch_submenu["id"]}


# No submenus
def test_emtpy_submenu_list(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


# After submenu is created
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


# After update
def test_updated_submenu_by_response(create_menu, patch_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{patch_submenu['id']}"
    )
    assert response.status_code == 200
    assert response.json() == patch_submenu


# After submenu is deleted
def test_submenu_list_after_delete(delete_submenu, create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


def test_submenu_by_id_after_delete(delete_submenu, create_menu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{delete_submenu['id']}"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


# Test menu list after menu is deleted
def test_menu_list_after_menu_delete(create_menu):
    response = client.delete(f"{base_url}/menus/{create_menu['id']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/menus")

    assert response.status_code == 200
    assert response.json() == []
