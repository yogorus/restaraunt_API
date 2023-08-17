"""Tasks for celery"""
import asyncio

import pandas as pd

from src.celery.celery_worker import celery
from src.celery.utils import (
    cleanup_database,
    handle_dish_row,
    handle_menu_row,
    handle_submenu_row,
)


async def track_xlsx_to_db() -> None:
    """
    Function that tracks xlsx file and converts tables from it to database

    """
    menu_list: list[dict] = []
    menu_counter: int = -1
    submenu_counter: int = 0

    menu_df = pd.read_excel('admin/Menu.xlsx', header=None)

    # pylint: disable=unused-variable
    for index, row in menu_df.iterrows():
        # If this is a menu row
        if pd.notnull(row.iloc[0]):
            submenu_counter = -1
            menu = await handle_menu_row(row)
            menu['submenus'] = []
            menu_list.append(menu)
            menu_counter += 1

        # If this is a submenu
        elif row.iloc[1:4].notna().all():
            submenu = await handle_submenu_row(row, menu_list[menu_counter]['id'])
            submenu['dishes'] = []
            menu_list[menu_counter]['submenus'].append(submenu)
            submenu_counter += 1

        # if row is a Dish
        elif row.iloc[2:6].notna().all():
            current_menu = menu_list[menu_counter]
            current_submenu = current_menu['submenus'][submenu_counter]
            dish = await handle_dish_row(
                row, menu_id=current_menu['id'], submenu_id=current_submenu['id']
            )
            menu_list[menu_counter]['submenus'][submenu_counter]['dishes'].append(dish)

    # Cleanup the database
    await cleanup_database(menu_list)


@celery.task
def run_async_xlsx_tracker() -> None:
    """Function to run the tracker in the event loop"""
    # loop = asyncio.get_event_loop()
    # return loop.run_until_complete(track_xlsx_to_db())
    asyncio.run(track_xlsx_to_db())
