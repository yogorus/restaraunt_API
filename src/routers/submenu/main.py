from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from . import crud, schemas

from src.database import get_db
from src.models import Menu, Submenu
from src.routers.utils import return_menu_or_404, return_submenu_or_404

router = APIRouter(prefix=("/api/v1/menus"))


# Get list of all submenus
@router.get("/{menu_id}/submenus/")
async def read_submenus(
    db_menu: Annotated[Menu, Depends(return_menu_or_404)],
    db: AsyncSession = Depends(get_db),
):
    db_submenus = await crud.get_submenus(db, db_menu)

    submenus = [
        schemas.SubmenuOutput(
            **submenu.__dict__, dishes_count=await crud.count_dishes(db, submenu)
        )
        for submenu in db_submenus
    ]
    return submenus


# Create submenu
@router.post("/{menu_id}/submenus/", status_code=201)
async def create_submenu(
    submenu: schemas.SubmenuBase,
    db_menu: Menu = Depends(return_menu_or_404),
    db: AsyncSession = Depends(get_db),
):
    if await crud.count_same_titles(db, submenu.title) >= 1:
        raise HTTPException(409, detail="submenu with that title already exists")

    db_submenu = await crud.create_submenu(db, db_menu.id, submenu)  # type: ignore
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=await crud.count_dishes(db, db_submenu)
    )


# Get submenu by id
@router.get(
    "/{menu_id}/submenus/{submenu_id}",
)
async def read_submenu(
    db_submenu: Submenu = Depends(return_submenu_or_404),
    db: AsyncSession = Depends(get_db),
):
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=await crud.count_dishes(db, db_submenu)
    )


# Update submenu
@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
)
async def update_submenu(
    submenu_data: schemas.SubmenuBase,
    db_submenu: Submenu = Depends(return_submenu_or_404),
    db: AsyncSession = Depends(get_db),
):
    if await crud.count_same_titles(db, submenu_data.title) > 1:
        raise HTTPException(409, detail="submenu with that title already exists")

    db_submenu = await crud.patch_submenu(db, submenu_data, db_submenu)
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=await crud.count_dishes(db, db_submenu)
    )


# Delete submenu
@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
)
async def delete_submenu(
    db_submenu: Submenu = Depends(return_submenu_or_404),
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_submenu(db, db_submenu)
    return {"status": True, "message": "The submenu has been deleted"}
