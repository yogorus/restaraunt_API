"""Test menu endpoints"""
import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.main import app

# pylint: disable=W0621
# pylint: disable=W0613


@pytest_asyncio.fixture(scope='session')
async def create_menu(client: AsyncClient):
    """Fixture to create menu and return json"""
    sent_json = {'title': 'My menu 1', 'description': 'My menu description 1'}
    response = await client.post(app.url_path_for('create_menu'), json=sent_json)
    response_json = response.json()

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 201
    assert 'id' in response_json
    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


@pytest.fixture(scope='session')
async def get_menu_by_id(client: AsyncClient, create_menu):
    'fixture to get menu by id and return json'
    response = await client.get(
        app.url_path_for('read_menu', menu_id=create_menu['id'])
    )
    response_json = response.json()
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    yield response_json


@pytest.fixture(scope='session')
async def patch_menu(client: AsyncClient, get_menu_by_id):
    """fixture to patch menu and return its contents"""
    sent_json = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
    }
    response = await client.patch(
        app.url_path_for('patch_menu', menu_id=get_menu_by_id['id']), json=sent_json
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    response_json = response.json()
    assert get_menu_by_id['id'] == response_json['id']
    assert get_menu_by_id['title'] != response_json['title']
    assert get_menu_by_id['description'] != response_json['description']

    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


@pytest.fixture(scope='session')
async def delete_menu(client: AsyncClient, patch_menu):
    """fixture to delete menu and return id of deleted menu"""
    response = await client.delete(
        app.url_path_for('delete_menu', menu_id=patch_menu['id'])
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    yield {'id': patch_menu['id']}


# Empty db
# @pytest.mark.asyncio
async def test_menu_root(client: AsyncClient):
    """test menu list before creation to be empty"""
    url = app.url_path_for('read_menus')
    response = await client.get(url)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


# After creation
# @pytest.mark.asyncio
async def test_menu_root_is_not_empty(client: AsyncClient, create_menu):
    """test menu list is not empty after creation"""
    response = await client.get(app.url_path_for('read_menus'))
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_menu_response_after_create(client: AsyncClient, create_menu):
    """test menu by id to exist after creation"""
    response = await client.get(
        app.url_path_for('read_menu', menu_id=create_menu['id'])
    )
    response_json = response.json()
    assert response_json == create_menu


# After patch
async def test_updated_menu_response(client: AsyncClient, patch_menu):
    """test menu by id after update"""
    response = await client.get(app.url_path_for('read_menu', menu_id=patch_menu['id']))
    assert response.status_code == 200
    assert response.json() == patch_menu


# After delete
async def test_menu_list_after_delete(client: AsyncClient, delete_menu):
    """test menu list is empty after delete"""
    response = await client.get(app.url_path_for('read_menus'))
    assert response.status_code == 200
    assert response.json() == []


async def test_menu_by_id_after_delete(client: AsyncClient, delete_menu):
    """test menu by id to return 404 after delete"""
    response = await client.get(
        app.url_path_for('read_menu', menu_id=delete_menu['id'])
    )
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'
