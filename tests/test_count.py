import pytest
from tests.conftest import client
from tests.test_dish import create_menu, create_submenu, base_url


# Create dishes
def test_create_2_dishes(create_menu, create_submenu):
    data = (
        {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.50",
        },
        {
            "title": "My dish 2",
            "description": "My dish description 2",
            "price": "13.50",
        },
    )

    for json in data:
        response = client.post(
            f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes",
            json=json,
        )
        response_json = response.json()

        assert response.status_code == 201

        assert "id" in response_json


# Test menu by id
def test_get_menu_by_id(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == create_menu["id"]
    assert response_json["submenus_count"] == 1
    assert response_json["dishes_count"] == 2


# Test submenu by id
def test_get_submenu_by_id(create_menu, create_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["id"] == create_submenu["id"]
    assert response_json["dishes_count"] == 2


# Test delete submenu
def test_delete_submenu_by_id(create_menu, create_submenu):
    response = client.delete(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    assert response.status_code == 200


# Test empty submenu list after submenu deletion
def test_submenu_list_after_delete(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


# Test dish list after submenu deletion
def test_dish_list_after_submenu_deletion(create_menu, create_submenu):
    response = client.get(
        f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes"
    )
    assert response.status_code == 200
    assert response.json() == []


# Test menu when all children are deleted
def test_get_menu_with_no_children(create_menu):
    response = client.get(f"{base_url}/menus/{create_menu['id']}")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == create_menu["id"]
    assert response_json["submenus_count"] == 0
    assert response_json["dishes_count"] == 0


# Delete menu
def test_delete_menu(create_menu):
    response = client.delete(f"{base_url}/menus/{create_menu['id']}")
    assert response.status_code == 200


# Test if menus are empty
def test_menu_after_delete():
    response = client.get(f"{base_url}/menus/")
    assert response.status_code == 200
    assert response.json() == []
