"""Functions to handle excel rows"""
from uuid import UUID

import httpx
from pandas.core.series import Series

from src.main import app

BASE_URL = 'http://ylab_api:8000'


async def handle_menu_row(row: Series) -> dict:
    """Perform CRUD for menu row in excel and return the menu dictionary"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        menu_id = row.iloc[0]
        title = row.iloc[1]
        description = row.iloc[2]
        data = {
            'id': menu_id,
            'title': title,
            'description': description,
        }
        response = await client.get(app.url_path_for('read_menu', menu_id=menu_id))
        response_json = response.json()
        keys = set(data.keys())

        # Create menu if it doesn't exists
        if response.status_code == 404:
            result = await client.post(app.url_path_for('create_menu'), json=data)
            print(f'Created menu:\n{result.json()}')
            # print(f"no menu with id{menu_id}")

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


async def cleanup_database(menu_list: list[dict]) -> None:
    """Cleanup database if something got deleted from excel table"""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Get All menus
        response_menus = await client.get(app.url_path_for('read_menus'))
        # If database have more menus than table, delete those not in table
        if len(response_menus.json()) > len(menu_list):
            menu_id_list: list[UUID] = [menu['id'] for menu in menu_list]

            await client.request(
                method='DELETE',
                url=app.url_path_for('delete_unspecified_menus'),
                json=menu_id_list,
            )
            print('Deleted some menus...')

        # For every menu, check its child submenus
        for menu in menu_list:
            response_submenus = await client.get(
                app.url_path_for('read_submenus', menu_id=menu['id'])
            )
            # TODO: delete these submenus
            if len(response_submenus.json()) > len(menu['submenus']):
                pass
