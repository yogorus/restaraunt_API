import pytest
from tests.conftest import client
from tests.test_submenu import create_menu, create_submenu, base_url


@pytest.fixture(scope="session")
def create_dish(create_menu, create_submenu):
    sent_json = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
    }
    response = client.post(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes",
        json=sent_json,
    )
    response_json = response.json()
    assert response.status_code == 201
    assert "id" in response_json
    assert "title" in response_json
    assert "price" in response_json
    assert "description" in response_json

    yield response_json


@pytest.fixture(scope="session")
def patch_dish(create_menu, create_submenu, create_dish):
    sent_json = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
    }
    response = client.patch(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}",
        json=sent_json,
    )
    response_json = response.json()

    assert response.status_code == 200
    assert create_dish["id"] == response_json["id"]
    assert create_dish["title"] != response_json["title"]
    assert create_dish["price"] != response_json["price"]
    assert create_dish["description"] != response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
def delete_dish(create_menu, create_submenu, patch_dish):
    response = client.delete(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{patch_dish['id']}",
    )
    assert response.status_code == 200

    yield {"id": patch_dish["id"]}


def test_dish_empty_list(create_menu, create_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes"
    )
    assert response.status_code == 200
    assert response.json() == []


def test_dish_list_after_create(create_menu, create_submenu, create_dish):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_dish_by_id_after_create(create_menu, create_submenu, create_dish):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}"
    )
    assert response.status_code == 200
    assert response.json() == create_dish


def test_response_from_updated_dish(create_menu, create_submenu, patch_dish):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{patch_dish['id']}"
    )
    assert response.status_code == 200
    assert response.json() == patch_dish


def test_dish_list_after_delete(create_menu, create_submenu, delete_dish):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes"
    )
    assert response.status_code == 200
    assert response.json() == []


def test_dish_by_id_after_delete(create_menu, create_submenu, delete_dish):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{delete_dish['id']}"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_submenu_list_after_submenu_delete(create_menu, create_submenu):
    response = client.delete(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    assert response.status_code == 200

    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


def test_menu_list_after_menu_delete(create_menu):
    response = client.delete(f"{base_url}/menus/{create_menu['id']}")
    assert response.status_code == 200

    response = client.get(f"{base_url}/menus/")
    assert response.status_code == 200
    assert response.json() == []


# def test_dish_list_after_menu_delete(create_menu, create_submenu, create_dish):
#     response = client.delete(f"{base_url}/menus/{create_menu['id']}")

#     response = client.get(
#         f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/"
#     )
#     assert response.json() == []
