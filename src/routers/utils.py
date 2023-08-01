from uuid import UUID
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from .menu.crud import get_menu_by_id
from src.models import Menu

from .submenu.crud import get_submenu_by_id

# from .dish.crud import get_dish_by_id

from src.database import get_db


async def check_menu_id(menu_id: UUID):
    return menu_id


async def return_menu_or_404(
    menu_id: Annotated[UUID, Depends(check_menu_id)], db: AsyncSession = Depends(get_db)
):
    db_menu = await get_menu_by_id(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


async def return_submenu_or_404(
    submenu_id: UUID,
    db_menu: Annotated[Menu, Depends(return_menu_or_404)],
    db: AsyncSession = Depends(get_db),
):
    db_submenu = await get_submenu_by_id(db, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


# async def check_menu_id(menu_id: UUID, db: AsyncSession = Depends(get_db)):
#     db_menu = await get_menu_by_id(db, menu_id)
#     if not db_menu:
#         raise HTTPException(status_code=404, detail="menu not found")
#     return {"db_menu": db_menu}


# async def check_menu_id(menu_id: UUID, db: AsyncSession = Depends(get_db)):
#     menu = await get_menu_by_id(db, menu_id)
#     if not menu:
#         raise HTTPException(status_code=404, detail="menu not found")


# def check_submenu_id(submenu_id: UUID, db: AsyncSession = Depends(get_db)):
#     submenu = get_submenu_by_id(db, submenu_id)
#     if not submenu:
#         raise HTTPException(status_code=404, detail="submenu not found")


# def check_dish_id(dish_id: UUID, db: AsyncSession = Depends(get_db)):
#     dish = get_dish_by_id(db, dish_id)
#     if not dish:
#         raise HTTPException(status_code=404, detail="dish not found")
