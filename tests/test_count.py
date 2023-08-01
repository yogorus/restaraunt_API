import pytest
from httpx import AsyncClient
from tests.test_dish import create_menu, create_submenu, base_url


# Create dishes
async def test_create_2_dishes(client: AsyncClient, create_menu, create_submenu):
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
        response = await client.post(
            f"/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/",
            json=json,
        )
        response_json = response.json()

        assert response.status_code == 201

        assert "id" in response_json


# Test menu by id
async def test_get_menu_by_id(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/{create_menu['id']}")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == create_menu["id"]
    assert response_json["submenus_count"] == 1
    assert response_json["dishes_count"] == 2


# Test submenu by id
async def test_get_submenu_by_id(client: AsyncClient, create_menu, create_submenu):
    response = await client.get(
        f"/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["id"] == create_submenu["id"]
    assert response_json["dishes_count"] == 2


# Test delete submenu
async def test_delete_submenu_by_id(client: AsyncClient, create_menu, create_submenu):
    response = await client.delete(
        f"/menus/{create_menu['id']}/submenus/{create_submenu['id']}"
    )
    assert response.status_code == 200


# Test empty submenu list after submenu deletion
async def test_submenu_list_after_delete(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/{create_menu['id']}/submenus/")
    assert response.status_code == 200
    assert response.json() == []


# Test dish list after submenu deletion
async def test_dish_list_after_submenu_deletion(
    client: AsyncClient, create_menu, create_submenu
):
    response = await client.get(
        f"/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/"
    )
    assert response.status_code == 200
    assert response.json() == []


# Test menu when all children are deleted
async def test_get_menu_with_no_children(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/{create_menu['id']}")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["id"] == create_menu["id"]
    assert response_json["submenus_count"] == 0
    assert response_json["dishes_count"] == 0


# Delete menu
async def test_delete_menu(client: AsyncClient, create_menu):
    response = await client.delete(f"/menus/{create_menu['id']}")
    assert response.status_code == 200


# Test if menus are empty
async def test_menu_after_delete(
    client: AsyncClient,
):
    response = await client.get(f"{base_url}/menus/")
    assert response.status_code == 200
    assert response.json() == []
