"""Test children count"""
from httpx import AsyncClient

from src.main import app
from tests.test_dish import create_menu, create_submenu

# flake8: noqa: f811
# pylint: disable=redefined-outer-name, unused-argument, unused-import


# Create dishes
async def test_create_2_dishes(
    client: AsyncClient, create_menu, create_submenu
) -> None:
    """Test 2 dishes are 201"""
    data = (
        {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
        },
        {
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50',
        },
    )

    for json in data:
        response = await client.post(
            app.url_path_for(
                'create_dish',
                menu_id=create_menu['id'],
                submenu_id=create_submenu['id'],
            ),
            json=json,
        )
        response_json = response.json()

        assert response.status_code == 201

        assert 'id' in response_json


# Test menu by id
async def test_get_menu_by_id(client: AsyncClient, create_menu) -> None:
    """Test menu child count"""
    response = await client.get(
        app.url_path_for('read_menu', menu_id=create_menu['id'])
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['id'] == create_menu['id']
    assert response_json['submenus_count'] == 1
    assert response_json['dishes_count'] == 2


# Test submenu by id
async def test_get_submenu_by_id(
    client: AsyncClient, create_menu, create_submenu
) -> None:
    """Test submenu child dishes"""
    response = await client.get(
        app.url_path_for(
            'read_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        )
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['id'] == create_submenu['id']
    assert response_json['dishes_count'] == 2


# Test delete submenu
async def test_delete_submenu_by_id(
    client: AsyncClient, create_menu, create_submenu
) -> None:
    """Test submenu successfully deleted"""
    response = await client.delete(
        app.url_path_for(
            'delete_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        ),
    )
    assert response.status_code == 200


# Test empty submenu list after submenu deletion
async def test_submenu_list_after_delete(client: AsyncClient, create_menu) -> None:
    """Test submenu list is empty after delete"""
    response = await client.get(
        app.url_path_for('read_submenus', menu_id=create_menu['id'])
    )
    assert response.status_code == 200
    assert response.json() == []


# Test dish list after submenu deletion
async def test_dish_list_after_submenu_deletion(
    client: AsyncClient, create_menu, create_submenu
) -> None:
    """Test dish list is empty after submenu delete"""
    response = await client.get(
        app.url_path_for(
            'read_dishes',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
        ),
    )
    assert response.status_code == 200
    assert response.json() == []


# Test menu when all children are deleted
async def test_get_menu_with_no_children(client: AsyncClient, create_menu) -> None:
    """Test menu children count is zero"""
    response = await client.get(
        app.url_path_for('read_menu', menu_id=create_menu['id'])
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['id'] == create_menu['id']
    assert response_json['submenus_count'] == 0
    assert response_json['dishes_count'] == 0


# Delete menu
async def test_delete_menu(client: AsyncClient, create_menu) -> None:
    """Test menu deletes sucessfully"""
    response = await client.delete(
        app.url_path_for('delete_menu', menu_id=create_menu['id'])
    )
    assert response.status_code == 200


# Test if menus are empty
async def test_menu_list_after_delete(
    client: AsyncClient,
) -> None:
    """Test menu list is empty after delete"""
    response = await client.get(app.url_path_for('read_menus'))
    assert response.status_code == 200
    assert response.json() == []
