from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy import func, select
from uuid import UUID
from . import schemas

from src.models import Menu, Submenu, Dish


async def get_menus(db: AsyncSession) -> list[Menu]:
    query = select(Menu)
    result = await db.execute(query)
    result = list(result.scalars().all())
    return result


async def get_menu_by_id(db: AsyncSession, id: UUID) -> Menu | None:
    query = select(Menu).filter(Menu.id == id)
    result = await db.execute(query)
    result = result.scalar()
    return result
    # return db.query(Menu).filter(Menu.id == id).first()  # type: ignore


# def create_menu(db: Session, menu: schemas.MenuBase) -> Menu:
#     db_menu = Menu(**menu.model_dump())
#     db.add(db_menu)
#     db.commit()
#     db.refresh(db_menu)
#     return db_menu


# def patch_menu(db: Session, data: schemas.MenuBase, db_menu: Menu) -> Menu:
#     db_menu = db_menu
#     db_menu.title = data.title  # type: ignore
#     db_menu.description = data.description  # type: ignore
#     db.commit()
#     db.refresh(db_menu)
#     return db_menu


# def delete_menu(db: Session, db_menu: Menu):
#     db.delete(db_menu)
#     db.commit()


# def count_children(db: Session, db_menu: Menu) -> dict[str, int]:
#     dishes_count = 0

#     submenus = db.query(Submenu).filter(Submenu.menu_id == db_menu.id)
#     submenus_count = submenus.count()

#     for submenu in submenus:
#         count = db.query(Dish).filter(Dish.submenu_id == submenu.id).count()
#         dishes_count += count

#     return {"submenus_count": submenus_count, "dishes_count": dishes_count}
