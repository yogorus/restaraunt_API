from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy import func, select, insert
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from . import schemas
from typing import Sequence

from src.models import Menu, Submenu, Dish


async def get_menus(db: AsyncSession) -> Sequence:
    query = select(Menu)
    result = await db.execute(query)
    # result = list(result.scalars().fetchall())
    return result.scalars().all()


async def get_menu_by_id(db: AsyncSession, id: UUID) -> Menu | None:
    query = select(Menu).filter(Menu.id == id)
    result = await db.execute(query)
    result = result.scalar()
    return result
    # return db.query(Menu).filter(Menu.id == id).first()  # type: ignore


async def create_menu(db: AsyncSession, menu: schemas.MenuBase):
    # query = insert(Menu).values(**menu.model_dump())
    # db_menu: Menu = await db.execute(query)
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


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


async def count_children(db: AsyncSession, db_menu: Menu) -> dict:
    query = (
        select(
            Menu.title,
            func.count(Submenu.id).label("submenus_count"),
            func.count(Dish.id).label("dishes_count"),
        )
        .select_from(Menu)
        .join(Submenu, Submenu.menu_id == Menu.id, isouter=True)
        .join(Dish, Dish.submenu_id == Submenu.id, isouter=True)
        .where(Menu.id == db_menu.id)
        .group_by(Menu.title)
    )
    result = await db.execute(query)

    # Convert result into dictionary
    row = result.fetchone()
    columns = result.keys()
    result_dict = {}
    if row is not None:
        result_dict = dict(zip(columns, row))
    return result_dict
