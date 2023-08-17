"""Tests for general endpoint"""
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from src.main import app

# flake8: noqa: f811
# pylint: disable=redefined-outer-name, unused-argument, unused-import


@pytest.fixture(scope='session')
async def create_two_menus(client: AsyncClient) -> AsyncGenerator[list[dict], None]:
    """Create two menus"""
    result: list[dict] = []

    for i in range(1, 3):
        sent_json = {'title': f'My menu {i}', 'description': f'My menu description {i}'}
        response = await client.post(app.url_path_for('create_menu'), json=sent_json)
        response_json = response.json()

        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == 201
        assert 'id' in response_json
        assert sent_json['title'] == response_json['title']
        assert sent_json['description'] == response_json['description']

        result.append(response_json)

    yield result


@pytest.fixture(scope='session')
async def update_first_menu(
    client: AsyncClient, create_two_menus
) -> AsyncGenerator[dict, None]:
    """Update first menu"""
    sent_json = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
    }
    response = await client.patch(
        app.url_path_for('patch_menu', menu_id=create_two_menus[0]['id']),
        json=sent_json,
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    response_json = response.json()
    assert create_two_menus[0]['id'] == response_json['id']
    assert create_two_menus[0]['title'] != response_json['title']
    assert create_two_menus[0]['description'] != response_json['description']

    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


@pytest.fixture(scope='session')
async def create_submenu_in_first_menu(
    client: AsyncClient, create_two_menus
) -> AsyncGenerator[dict, None]:
    """Create submenu in first menu"""
    sent_json = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
    response = await client.post(
        app.url_path_for('create_submenu', menu_id=create_two_menus[0]['id']),
        json=sent_json,
    )
    assert response.status_code == 201
    response_json = response.json()
    assert 'id' in response_json
    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    result = {'submenu': response_json, 'menu_id': create_two_menus[0]['id']}
    yield result


@pytest.fixture(scope='session')
async def create_2_dishes_in_first_submenu(
    client: AsyncClient, create_submenu_in_first_menu
) -> AsyncGenerator[list[dict], None]:
    """Create 2 dishes in first submenu"""
    result: list[dict] = []

    for i in range(1, 3):
        json = {
            'title': f'My dish {i}',
            'description': f'My dish description {i}',
            'price': f'{i}2.50',
        }
        response = await client.post(
            app.url_path_for(
                'create_dish',
                menu_id=create_submenu_in_first_menu['menu_id'],
                submenu_id=create_submenu_in_first_menu['submenu']['id'],
            ),
            json=json,
        )
        response_json = response.json()

        assert response.status_code == 201

        assert 'id' in response_json

        result.append(response_json)

    yield result


@pytest.fixture(scope='session')
async def create_submenu_in_second_menu(
    client: AsyncClient, create_two_menus
) -> AsyncGenerator[dict, None]:
    """Create submenu in second menu"""
    sent_json = {'title': 'My submenu 2', 'description': 'My submenu description 2'}
    response = await client.post(
        app.url_path_for('create_submenu', menu_id=create_two_menus[1]['id']),
        json=sent_json,
    )
    assert response.status_code == 201
    response_json = response.json()
    assert 'id' in response_json
    assert sent_json['title'] == response_json['title']
    assert sent_json['description'] == response_json['description']

    yield response_json


# Test that list is empty
async def test_endpoint_is_empty(client: AsyncClient) -> None:
    """Test list is empty"""
    response = await client.get(app.url_path_for('get_all'))
    assert response.status_code == 200
    assert response.json() == []


# Test list len is two and menu has nested submenu and dishes
async def test_endpoint_is_not_empty(
    client: AsyncClient,
    create_two_menus,
) -> None:
    """Test list is not empty"""
    response = await client.get(app.url_path_for('get_all'))
    response_json = response.json()
    assert response.status_code == 200

    # Test that route returns 2 menu
    assert len(response_json) == 2

    create_two_menus_ids = [menu['id'] for menu in create_two_menus]
    for i in range(2):
        # Check that the id from the response is in the id list from the create_two_menus
        assert response_json[i]['id'] in create_two_menus_ids

        # Check title is there
        assert response_json[i]['title'] in [menu['title'] for menu in create_two_menus]

        # Check description is there
        assert response_json[i]['description'] in [
            menu['description'] for menu in create_two_menus
        ]


# Test submenu in first menu
async def test_submenu_in_first_menu(
    client: AsyncClient, create_submenu_in_first_menu
) -> None:
    """Test created submenu in first menu appeared in first menu"""
    response = await client.get(app.url_path_for('get_all'))
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2

    for menu in response_json:
        if menu['submenus']:
            assert (
                create_submenu_in_first_menu['submenu']['id']
                == menu['submenus'][0]['id']
            )
            assert (
                create_submenu_in_first_menu['submenu']['title']
                == menu['submenus'][0]['title']
            )
            assert (
                create_submenu_in_first_menu['submenu']['description']
                == menu['submenus'][0]['description']
            )


async def test_2_dishes_in_first_submenu(
    client: AsyncClient, create_2_dishes_in_first_submenu
) -> None:
    """Test 2 created dishes appeared in first submenu"""
    response = await client.get(app.url_path_for('get_all'))
    response_json = response.json()
    assert response.status_code == 200
    assert len(response_json) == 2

    for menu in response_json:
        if menu['submenus']:
            submenu = menu['submenus'][0]
            if submenu['dishes']:
                assert len(submenu['dishes']) == 2
                for dish in create_2_dishes_in_first_submenu:
                    assert dish in submenu['dishes']
                    assert dish['submenu_id'] == submenu['id']


# Update first menu and check the contents have changed
async def test_endpoint_first_menu_after_update(
    client: AsyncClient, update_first_menu
) -> None:
    """Update first menu in the database and test if contents of endpoint have changed"""
    response = await client.get(app.url_path_for('get_all'))
    response_json = response.json()
    assert response.status_code == 200
    assert len(response_json) == 2

    for menu in response_json:
        if menu['submenus']:
            assert menu['id'] == update_first_menu['id']
            assert menu['title'] == update_first_menu['title']
            assert menu['description'] == update_first_menu['description']


# Create second submenu in second menu and check for nested submenu
async def test_endpoint_after_creating_second_submenu_in_second_menu(
    client: AsyncClient, create_submenu_in_second_menu
) -> None:
    """Create second submenu in second menu and check for changes"""
    response = await client.get(app.url_path_for('get_all'))
    response_json = response.json()
    assert response.status_code == 200
    assert len(response_json) == 2

    for menu in response_json:
        assert len(menu['submenus']) == 1
        if not menu['submenus'][0]['dishes']:
            submenu = menu['submenus'][0]
            assert create_submenu_in_second_menu['id'] == submenu['id']
            assert create_submenu_in_second_menu['title'] == submenu['title']
            assert (
                create_submenu_in_second_menu['description'] == submenu['description']
            )


# Delete all menus and check if endpoint returns empty list
async def test_endpoint_after_deleting_menus(
    client: AsyncClient, create_submenu_in_second_menu
) -> None:
    """Delete all menus and check if endpoint returns empty list"""
    response = await client.get(app.url_path_for('get_all'))
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2

    for menu in response_json:
        await client.delete(app.url_path_for('delete_menu', menu_id=menu['id']))

    response = await client.get(app.url_path_for('get_all'))
    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json() == []
