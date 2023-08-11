"""Tasks for celery"""
import pandas as pd

# from src.models import Menu, Submenu, Dish
menu_dict: dict = {}

menu_df = pd.read_excel('admin/Menu.xlsx', header=None)
for index, row in menu_df.iterrows():
    # If this is a menu
    if pd.notnull(row.iloc[0]):
        print('Menu:')
        print(row.iloc[0], row.iloc[1], row.iloc[2])
    # If this is a submenu
    elif row.iloc[1:4].notna().all():
        print('Submenu:')
        print(row.iloc[1], row.iloc[2], row.iloc[3])
    # if row is a Dish
    elif row.iloc[2:6].notna().all():
        print('Dish:')
        print(row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5])


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
