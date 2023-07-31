import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient

# from tests.conftest import client

base_url = "http://localhost/api/v1"
pytest_plugins = ("pytest_asyncio",)


@pytest_asyncio.fixture(scope="session")
async def create_menu(client: AsyncClient):
    sent_json = {"title": "My menu 1", "description": "My menu description 1"}
    response = await client.post(f"/menus/", json=sent_json)
    response_json = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 201
    assert "id" in response_json
    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
async def get_menu_by_id(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/{create_menu['id']}/")
    response_json = response.json()
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200

    yield response_json


@pytest.fixture(scope="session")
async def patch_menu(client: AsyncClient, get_menu_by_id):
    sent_json = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }
    response = await client.patch(f"/menus/{get_menu_by_id['id']}/", json=sent_json)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_json = response.json()
    assert get_menu_by_id["id"] == response_json["id"]
    assert get_menu_by_id["title"] != response_json["title"]
    assert get_menu_by_id["description"] != response_json["description"]

    assert sent_json["title"] == response_json["title"]
    assert sent_json["description"] == response_json["description"]

    yield response_json


@pytest.fixture(scope="session")
async def delete_menu(client: AsyncClient, patch_menu):
    response = await client.delete(f"/menus/{patch_menu['id']}/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    yield {"id": patch_menu["id"]}


# Empty db
@pytest.mark.asyncio
async def test_menu_root(
    client: AsyncClient,
):
    response = await client.get(f"/menus/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert response.json() == []


# After creation
@pytest.mark.asyncio
async def test_menu_root_is_not_empty(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_menu_response_after_create(client: AsyncClient, create_menu):
    response = await client.get(f"/menus/{create_menu['id']}/")
    response_json = response.json()
    assert response_json == create_menu


# After patch
async def test_updated_menu_response(client: AsyncClient, patch_menu):
    response = await client.get(f"/menus/{patch_menu['id']}/")
    assert response.status_code == 200
    assert response.json() == patch_menu


# After delete
async def test_menu_list_after_delete(client: AsyncClient, delete_menu):
    response = await client.get(f"/menus/")
    assert response.status_code == 200
    assert response.json() == []


async def test_menu_by_id_after_delete(client: AsyncClient, delete_menu):
    response = await client.get(f"/menus/{delete_menu['id']}/")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"
