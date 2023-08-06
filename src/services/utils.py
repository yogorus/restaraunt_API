"""Dependencies to check for parent existence"""
from uuid import UUID

from fastapi import Depends

from src.models import Menu, Submenu
from src.services.menu.menu_repository import MenuCRUDRepository
from src.services.submenu.submenu_repository import SubmenuCRUDRepository


async def check_menu_id(menu_id: UUID):
    """Check menu_id from path"""
    return menu_id


async def return_menu_or_404(
    menu_id: UUID = Depends(check_menu_id), menu_repo: MenuCRUDRepository = Depends()
) -> Menu:
    """Return menu or raise an exception"""
    return await menu_repo.get_one(id=menu_id)


async def return_submenu_or_404(
    submenu_id: UUID,
    menu: Menu = Depends(return_menu_or_404),
    submenu_repo: SubmenuCRUDRepository = Depends(),
) -> Submenu:
    """Return submenu or exception"""
    return await submenu_repo.get_one(id=submenu_id, menu_id=menu.id)


# async def return_submenu_or_404(
#     submenu_id: UUID,
#     db_menu: Annotated[Menu, Depends(return_menu_or_404)],
#     db: AsyncSession = Depends(get_db),
# ):
#     db_submenu = await get_submenu_by_id(db, submenu_id)
#     if not db_submenu:
#         raise HTTPException(status_code=404, detail='submenu not found')
#     return db_submenu


# async def return_dish_or_404(
#     dish_id: UUID,
#     db_submenu: Submenu = Depends(return_submenu_or_404),
#     db: AsyncSession = Depends(get_db),
# ):
#     db_dish = await get_dish_by_id(db, dish_id)
#     if not db_dish:
#         raise HTTPException(status_code=404, detail='dish not found')
#     return db_dish
