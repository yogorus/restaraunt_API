"""Tests for dish"""
import pytest
from httpx import AsyncClient

from src.main import app
from tests.test_submenu import create_menu, create_submenu

# flake8: noqa: f811
# pylint: disable=redefined-outer-name, unused-argument, unused-import


@pytest.fixture(scope='session')
async def create_dish(client: AsyncClient, create_menu, create_submenu):
    """Fixture to create dish"""
    sent_json = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50',
    }
    response = await client.post(
        app.url_path_for(
            'create_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        ),
        json=sent_json,
    )
    response_json = response.json()

    assert response.status_code == 201

    assert 'id' in response_json
    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']
    assert sent_json['price'] == response_json['price']

    yield response_json


@pytest.fixture(scope='session')
async def patch_dish(client: AsyncClient, create_menu, create_submenu, create_dish):
    """Update dish fixture"""
    sent_json = {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50',
    }
    response = await client.patch(
        app.url_path_for(
            'patch_dish',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
            dish_id=create_dish['id'],
        ),
        json=sent_json,
    )
    response_json = response.json()

    assert response.status_code == 200
    assert create_dish['id'] == response_json['id']
    assert create_dish['title'] != response_json['title']
    assert create_dish['price'] != response_json['price']
    assert create_dish['description'] != response_json['description']

    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']
    assert sent_json['price'] == response_json['price']

    yield response_json


@pytest.fixture(scope='session')
async def delete_dish(client: AsyncClient, create_menu, create_submenu, patch_dish):
    """Delete dish fixture"""
    response = await client.delete(
        app.url_path_for(
            'delete_dish',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
            dish_id=patch_dish['id'],
        ),
    )
    assert response.status_code == 200

    yield {'id': patch_dish['id']}


async def test_dish_empty_list(client: AsyncClient, create_menu, create_submenu):
    """Test that dish is empty before creation"""
    response = await client.get(
        app.url_path_for(
            'read_dishes',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
        ),
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_dish_list_after_create(
    client: AsyncClient, create_menu, create_submenu, create_dish
):
    """Test that dish list is not empty after create"""
    response = await client.get(
        app.url_path_for(
            'read_dishes',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
        ),
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_dish_by_id_after_create(
    client: AsyncClient, create_menu, create_submenu, create_dish
):
    """Test dish exists after create"""
    response = await client.get(
        app.url_path_for(
            'read_dish',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
            dish_id=create_dish['id'],
        ),
    )
    assert response.status_code == 200
    assert response.json() == create_dish


async def test_response_from_updated_dish(
    client: AsyncClient, create_menu, create_submenu, patch_dish
):
    """Test dish values are up to date"""
    response = await client.get(
        app.url_path_for(
            'read_dish',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
            dish_id=patch_dish['id'],
        ),
    )
    assert response.status_code == 200
    assert response.json() == patch_dish


async def test_dish_list_after_delete(
    client: AsyncClient, create_menu, create_submenu, delete_dish
):
    """Test dish list is empty after delete"""
    response = await client.get(
        app.url_path_for(
            'read_dishes',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
        ),
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_dish_by_id_after_delete(
    client: AsyncClient, create_menu, create_submenu, delete_dish
):
    """Test dish doesn't exists after delete"""
    response = await client.get(
        app.url_path_for(
            'read_dish',
            menu_id=create_menu['id'],
            submenu_id=create_submenu['id'],
            dish_id=delete_dish['id'],
        ),
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


async def test_submenu_list_after_submenu_delete(
    client: AsyncClient, create_menu, create_submenu
):
    """Test that submenu list is empty after delete"""
    response = await client.delete(
        app.url_path_for(
            'delete_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        )
    )
    assert response.status_code == 200

    response = await client.get(
        app.url_path_for('read_submenus', menu_id=create_menu['id'])
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_menu_list_after_menu_delete(client: AsyncClient, create_menu):
    """Test menu list is empty after delete"""
    response = await client.delete(
        app.url_path_for('delete_menu', menu_id=create_menu['id'])
    )
    assert response.status_code == 200

    response = await client.get(app.url_path_for('read_menus'))
    assert response.status_code == 200
    assert response.json() == []


# def test_dish_list_after_menu_delete(create_menu, create_submenu, create_dish):
#     response = client.delete(f"{base_url}/menus/{create_menu['id']}")

#     response = client.get(
#         f"{base_url}/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/"
#     )
#     assert response.json() == []
