"""Tasks for celery"""
import asyncio

import pandas as pd

from src.celery.celery_worker import celery
from src.celery.utils import cleanup_database, handle_menu_row


async def track_xlsx_to_db() -> None:
    """
    Function that tracks xlsx file and converts tables from it to database

    """
    menu_list: list[dict] = []
    # menu_id_list: list[UUID] = []
    current_menu: dict | None = None

    # current_submenu: dict | None = None

    menu_df = pd.read_excel('admin/Menu.xlsx', header=None)

    # pylint: disable=unused-variable
    for index, row in menu_df.iterrows():
        # If this is a menu row
        if pd.notnull(row.iloc[0]):
            menu = await handle_menu_row(row)
            current_menu = menu
            current_menu['submenus'] = []
            menu_list.append(current_menu)

            # print(row.iloc[0], row.iloc[1], row.iloc[2])
        # If this is a submenu
        elif row.iloc[1:4].notna().all():
            # current_submenu = {
            #     "id": row.iloc[1],
            #     "title": row.iloc[2],
            #     "description": row.iloc[3],
            # }
            # current_menu["submenus"].append()
            print(f'Submenu child of {current_menu}')
            # print(row.iloc[1], row.iloc[2], row.iloc[3])
        # if row is a Dish
        elif row.iloc[2:6].notna().all():
            print('Dish:')
            # print(row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5])
        # Cleanup the database
        await cleanup_database(menu_list)


@celery.task
def run_async_xlsx_tracker():
    """Function to run the tracker in the event loop"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(track_xlsx_to_db())


# @celery.task()
# def test_task():
#     asyncio.run(track_xlsx_to_db)


# await track_xlsx_to_db()
# print(menus)

# current_menu = None
# current_submenu = None

# menu_dict = {"menus": []}
# submenu_dict = {"submenus": []}
# dish_dict = {"dishes": []}

# for index, row in menu_df.iterrows():
#     if pd.notnull(row["A"]) and pd.isnull(row["D"]):
#         current_menu = Menu(id=row["A"], title=row["B"], description=row["D"]).__dict__
#         current_menu["submenus"] = []
#         menu_dict["menus"].append(current_menu)

#     elif pd.notnull(row["B"]) and pd.notnull(row["C"]) and pd.notnull(row["D"]):
#         current_submenu = Submenu(
#             title=row["C"], description=row["D"], menu_id=current_menu["id"]
#         ).__dict__
#         current_submenu["dishes"] = []
#         current_menu["submenus"].append(current_submenu)
#         submenu_dict["submenus"].append(current_submenu)

#     elif pd.notnull(row["C"]) and pd.notnull(row["D"]) and pd.notnull(row["E"]):
#         dish = Dish(
#             title=row["C"],
#             description=row["D"],
#             price=str(row["E"]),
#             submenu_id=current_submenu["id"],
#         ).__dict__
#         current_submenu["dishes"].append(dish)
#         dish_dict["dishes"].append(dish)

# print(menu_dict)
# print(submenu_dict)
# print(dish_dict)
