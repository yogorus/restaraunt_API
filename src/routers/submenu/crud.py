from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from . import schemas

from src.models import Submenu, Menu, Dish


async def get_submenus(db: AsyncSession, db_menu: Menu) -> list[Submenu]:
    return db_menu.submenus


async def get_submenu_by_id(db: AsyncSession, id: UUID) -> Submenu | None:
    query = select(Submenu).filter(Submenu.id == id)
    result = await db.execute(query)
    result = result.scalar()
    return result


async def create_submenu(
    db: AsyncSession, menu_id: UUID, submenu: schemas.SubmenuBase
) -> Submenu:
    new_submenu = schemas.SubmenuForeignKey(**submenu.model_dump(), menu_id=menu_id)
    db_submenu = Submenu(**new_submenu.model_dump())
    db.add(db_submenu)
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


async def patch_submenu(
    db: AsyncSession, data: schemas.SubmenuBase, db_submenu: Submenu
) -> Submenu:
    db_submenu.title = data.title  # type: ignore
    db_submenu.description = data.description  # type: ignore
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


async def delete_submenu(db: AsyncSession, db_submenu: Submenu):
    await db.delete(db_submenu)
    await db.commit()


async def count_same_titles(db: AsyncSession, title: str) -> int:
    query = select(func.count(Submenu.title).label("title_count")).filter(
        Submenu.title == title
    )
    result = await db.execute(query)
    row = result.first()
    if row:
        return row.title_count
    return 0


async def count_dishes(db: AsyncSession, db_submenu: Submenu) -> int:
    query = (
        select(func.count(Dish.id).label("dishes_count"))
        .select_from(Submenu)
        .join(Dish, Dish.submenu_id == Submenu.id, isouter=True)
        .filter(Submenu.id == db_submenu.id)
    )
    result = await db.execute(query)
    row = result.first()
    if row:
        return row.dishes_count
    return 0
