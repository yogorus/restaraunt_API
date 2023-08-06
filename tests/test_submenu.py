"""Tests for submenu"""
import pytest
from httpx import AsyncClient

from src.main import app
from tests.test_menu import create_menu, delete_menu

# flake8: noqa: f811
# pylint: disable=redefined-outer-name, unused-argument, unused-import


@pytest.fixture(scope='session')
async def create_submenu(client: AsyncClient, create_menu):
    """Fixture to create submenu and access the jsonifed result"""
    sent_json = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
    response = await client.post(
        app.url_path_for('create_submenu', menu_id=create_menu['id']), json=sent_json
    )
    assert response.status_code == 201
    response_json = response.json()
    assert 'id' in response_json
    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


@pytest.fixture(scope='session')
async def patch_submenu(client: AsyncClient, create_menu, create_submenu):
    """Fixture to update submenu and access the jsonified result"""
    sent_json = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
    }
    response = await client.patch(
        app.url_path_for(
            'update_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        ),
        json=sent_json,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert create_submenu['id'] == create_submenu['id']
    assert create_submenu['title'] != response_json['title']
    assert create_submenu['description'] != response_json['description']

    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


@pytest.fixture(scope='session')
async def delete_submenu(client: AsyncClient, create_menu, patch_submenu):
    """Delete fixture"""
    response = await client.delete(
        app.url_path_for(
            'delete_submenu', menu_id=create_menu['id'], submenu_id=patch_submenu['id']
        ),
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    yield {'id': patch_submenu['id']}


# No submenus
async def test_emtpy_submenu_list(client: AsyncClient, create_menu):
    """Test submenu list is empty before creation"""
    response = await client.get(
        app.url_path_for('read_submenus', menu_id=create_menu['id'])
    )
    assert response.status_code == 200
    assert response.json() == []


# After submenu is created
async def test_submenu_list_after_create(
    client: AsyncClient, create_menu, create_submenu
):
    """Test submenu list is not empty after creation"""
    response = await client.get(
        app.url_path_for('read_submenus', menu_id=create_menu['id'])
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_submenu_by_id_after_create(
    client: AsyncClient, create_menu, create_submenu
):
    """Test submenu exists after creation"""
    response = await client.get(
        app.url_path_for(
            'read_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == create_submenu


# After update
async def test_updated_submenu_by_response(
    client: AsyncClient, create_menu, patch_submenu
):
    """Test that updated submenu changed it's values"""
    response = await client.get(
        app.url_path_for(
            'read_submenu', menu_id=create_menu['id'], submenu_id=patch_submenu['id']
        )
    )
    assert response.status_code == 200
    assert response.json() == patch_submenu


# After submenu is deleted
async def test_submenu_list_after_delete(
    client: AsyncClient, delete_submenu, create_menu
):
    """Test list is empty after submenu is deleted"""
    response = await client.get(
        app.url_path_for('read_submenus', menu_id=create_menu['id'])
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_submenu_by_id_after_delete(
    client: AsyncClient, delete_submenu, create_menu
):
    """Test submenu doesn't exist after delete"""
    response = await client.get(
        app.url_path_for(
            'read_submenu', menu_id=create_menu['id'], submenu_id=delete_submenu['id']
        )
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


# Test menu after menu is deleted
async def test_menu_list_after_menu_delete(client: AsyncClient, create_menu):
    """Test no menus after menu is deleted"""
    response = await client.delete(
        app.url_path_for('read_menu', menu_id=create_menu['id'])
    )
    assert response.status_code == 200

    response = await client.get(app.url_path_for('read_menus'))

    assert response.status_code == 200
    assert response.json() == []
