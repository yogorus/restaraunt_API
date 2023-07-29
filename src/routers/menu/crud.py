from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy import func
from uuid import UUID
from . import schemas

from src.models import Menu, Submenu, Dish


def get_menus(db: Session) -> list[Menu]:
    return db.query(Menu).all()


def get_menu_by_id(db: Session, id: UUID) -> Menu:
    return db.query(Menu).filter(Menu.id == id).first()  # type: ignore


def create_menu(db: Session, menu: schemas.MenuBase) -> Menu:
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def patch_menu(db: Session, data: schemas.MenuBase, db_menu: Menu) -> Menu:
    db_menu = db_menu
    db_menu.title = data.title  # type: ignore
    db_menu.description = data.description  # type: ignore
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, db_menu: Menu):
    db.delete(db_menu)
    db.commit()


def count_children(db: Session, db_menu: Menu) -> dict[str, int]:
    dishes_count = 0

    submenus = db.query(Submenu).filter(Submenu.menu_id == db_menu.id)
    submenus_count = submenus.count()

    for submenu in submenus:
        count = db.query(Dish).filter(Dish.submenu_id == submenu.id).count()
        dishes_count += count

    return {"submenus_count": submenus_count, "dishes_count": dishes_count}


# def count_dishes(db: Session, db_menu: Menu) -> int:
#     submenus = db.query(Submenu).filter(Submenu.menu_id == db_menu.id)
#     dishes = submenus.filter
#     return count


# def count_dishes(db: Session, db_menu: Menu):
#     submenu_count = (
#         db.query(func.count(Submenu.id))
#         .join(Menu)
#         .filter(Submenu.menu_id == db_menu.id)
#         .scalar()
#     )

#     dishes_count = (
#         db.query(func.count(Dish.id))
#         .join(Submenu)
#         .filter(Submenu.menu_id == db_menu.id)
#         .scalar()
#     )
#     return dishes_count

# def count_submenus(db: Session, db_menu: Menu)


# def count_children(db: Session, db_menu: Menu):
#     count = select(
#         Menu.id,
#         func.count(Submenu.id)
#         .filter(Submenu.menu_id == db_menu.id)
#         .label("submenus_count"),
#         func.count(Dish.id)
#         .filter(Dish.submenu_id == Submenu.id, Submenu.menu_id == db_menu.id)
#         .label("dishes_count"),
#     ).group_by(Menu.id, Menu.title)
#     result = db.execute(count).fetchone()
#     return result
# return {"submenus_count": count.submenus_count, "dishes_count": count.dishes_count}
