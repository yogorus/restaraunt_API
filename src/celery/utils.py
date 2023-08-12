"""Functions to handle excel rows"""
from uuid import UUID

import httpx
from pandas.core.series import Series

from src.main import app

BASE_URL = 'http://ylab_api:8000'


async def handle_menu_row(row: Series) -> dict:
    """Perform necessary CRUD from excel menu row and return menu dictionary"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        menu_id = row.iloc[0]
        title = row.iloc[1]
        description = row.iloc[2]

        data = {
            'id': menu_id,
            'title': title,
            'description': description,
        }
        keys = set(data.keys())

        response = await client.get(app.url_path_for('read_menu', menu_id=menu_id))
        response_json = response.json()

        # Create menu if it doesn't exists
        if response.status_code == 404:
            result = await client.post(app.url_path_for('create_menu'), json=data)
            print(f'Created menu:\n{result.json()}')

        # If menu exists, check if it has the same contents as excel row, if not, update it
        elif all(response_json[key] == data[key] for key in keys):
            print('Nothing to update')
            return data

        else:
            result = await client.patch(
                app.url_path_for('patch_menu', menu_id=menu_id), json=data
            )
            print('Menu updated!')

        return result.json()


async def hande_submenu_row(row: Series, menu_id: UUID) -> dict:
    """Perform CRUD from excel submenu row and return submenu dictionary"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        submenu_id = row.iloc[1]
        title = row.iloc[2]
        description = row.iloc[3]

        data = {
            'id': submenu_id,
            'title': title,
            'description': description,
        }
        keys = set(data.keys())

        response = await client.get(
            app.url_path_for('read_submenu', submenu_id=submenu_id, menu_id=menu_id)
        )

        response_json = response.json()

        # Create submenu if it doesn't exists
        if response.status_code == 404:
            result = await client.post(
                app.url_path_for('create_submenu', menu_id=menu_id), json=data
            )
            print(f'Created submenu:\n{result.json()}')

        # If submenu exists, check if it has the same contents as excel row, if not, update it
        elif all(response_json[key] == data[key] for key in keys):
            print('Nothing to update')
            return data

        else:
            result = await client.patch(
                app.url_path_for(
                    'update_submenu', submenu_id=submenu_id, menu_id=menu_id
                ),
                json=data,
            )
            print('Submenu updated!')

        return result.json()


async def handle_dish_row(row: Series, menu_id: UUID, submenu_id: UUID):
    """Perform CRUD from excel dish row and return submenu dictionary"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        dish_id = row.iloc[2]
        title = row.iloc[3]
        description = row.iloc[4]
        price = str(row.iloc[5])

        data = {
            'id': dish_id,
            'title': title,
            'description': description,
            'price': price,
        }
        keys = set(data.keys())

        response = await client.get(
            app.url_path_for(
                'read_dish', submenu_id=submenu_id, menu_id=menu_id, dish_id=dish_id
            )
        )

        response_json = response.json()

        # Create dish if it doesn't exists
        if response.status_code == 404:
            result = await client.post(
                app.url_path_for('create_dish', menu_id=menu_id, submenu_id=submenu_id),
                json=data,
            )
            print(f'Created dish:\n{result.json()}')

        # If submenu dish, check if it has the same contents as excel row, if not, update it
        elif all(response_json[key] == data[key] for key in keys):
            print('Nothing to update')
            return data

        else:
            result = await client.patch(
                app.url_path_for(
                    'patch_dish',
                    submenu_id=submenu_id,
                    menu_id=menu_id,
                    dish_id=dish_id,
                ),
                json=data,
            )
            print('Dish updated!')

        return result.json()


async def cleanup_database(menu_list: list[dict]) -> None:
    """Cleanup database if something got deleted from excel table"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Get All menus
        response_menus = await client.get(app.url_path_for('read_menus'))
        response_menus_json = response_menus.json()

        await cleanup_menu(response_menus_json, menu_list, client)

        await cleanup_submenu(menu_list, client)


async def cleanup_menu(
    response_menus_json: dict, menu_list: list[dict], client: httpx.AsyncClient
) -> None:
    """Delete menus that are not present in excel table"""
    # If database have more menus than table, delete those not in table
    if len(response_menus_json) > len(menu_list):
        menu_xlsx_id_list: list[UUID] = [menu['id'] for menu in menu_list]
        menu_db_id_list: list[UUID] = [menu['id'] for menu in response_menus_json]

        # Get menu UUIDs not present in the excel table
        non_matches = list(set(menu_db_id_list).difference(menu_xlsx_id_list))

        # Delete these menus
        if non_matches:
            for menu_id in non_matches:
                await client.delete(app.url_path_for('delete_menu', menu_id=menu_id))


async def cleanup_submenu(menu_list: list[dict], client: httpx.AsyncClient) -> None:
    """Delete submenus that are not present in excel table"""

    # For every menu, check its child submenus
    submenu_xlsx_id_list: list[dict[str, UUID]] = []
    submenu_db_id_list: list[dict[str, UUID]] = []

    # For every menu, get its child submenus
    for menu in menu_list:
        response_submenus = await client.get(
            app.url_path_for('read_submenus', menu_id=menu['id'])
        )
        response_submenus_json = response_submenus.json()

        # Cleanup dishes
        submenu_list = menu['submenus']
        await cleanup_dishes(submenu_list, menu['id'], client)

        # Check if excel table and db doesnt match
        if len(response_submenus_json) > len(menu['submenus']):
            # Append these ids to submenu id lists
            submenu_xlsx_id_list += [
                {'submenu_id': submenu['id'], 'menu_id': menu['id']}
                for submenu in menu['submenus']
            ]
            submenu_db_id_list += [
                {'submenu_id': submenu['id'], 'menu_id': submenu['menu_id']}
                for submenu in response_submenus_json
            ]

    # Get submenus UUIDs not present in the excel table
    non_matches: list[dict] = list(
        set(submenu_db_id_list).difference(submenu_xlsx_id_list)
    )

    # Delete non matching submenus
    if non_matches:
        for submenu in non_matches:
            await client.delete(
                app.url_path_for(
                    'delete_submenu',
                    menu_id=submenu['menu_id'],
                    submenu_id=submenu['submenu_id'],
                )
            )


async def cleanup_dishes(
    submenu_list: list[dict], menu_id: UUID, client: httpx.AsyncClient
) -> None:
    """Delete dishes that are not present in excel table"""
    dish_xlsx_id_list: list[tuple] = []
    dish_db_id_list: list[tuple] = []

    for submenu in submenu_list:
        response_dishes = await client.get(
            app.url_path_for(
                'read_dishes',
                menu_id=menu_id,
                submenu_id=submenu['id'],
            ),
            params={'filter_by_submenu': True},
        )

        response_dishes_json = response_dishes.json()

        # Check if excel table and db doesnt match
        if len(response_dishes_json) > len(submenu['dishes']):
            # Append these ids to submenu id lists
            dish_xlsx_id_list += [
                (
                    dish['id'],
                    submenu['id'],
                    menu_id,
                )
                for dish in submenu['dishes']
            ]
            dish_db_id_list += [
                (
                    dish['id'],
                    submenu['id'],
                    menu_id,
                )
                for dish in response_dishes_json
            ]

    # Get dish UUIDs not present in the excel table
    non_matches: list[tuple] = list(set(dish_db_id_list).difference(dish_xlsx_id_list))

    # Delete non matching submenus
    if non_matches:
        for dish in non_matches:
            await client.delete(
                app.url_path_for(
                    'delete_dish',
                    dish_id=dish[0],
                    submenu_id=dish[1],
                    menu_id=dish[2],
                )
            )
