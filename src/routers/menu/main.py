from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from . import crud, schemas

from src.models import Menu
from src.database import get_db
from src.routers.utils import return_menu_or_404


router = APIRouter(prefix=("/api/v1/menus"))


# List all menus
@router.get("/")
async def read_menus(db: AsyncSession = Depends(get_db)):
    db_menus = await crud.get_menus(db)
    menus = []
    for db_menu in db_menus:
        count_children = await crud.count_children(db, db_menu)
        menus.append(
            schemas.MenuOutput(
                **db_menu.__dict__,
                submenus_count=count_children["submenus_count"],
                dishes_count=count_children["dishes_count"],
            )
        )
    return menus


# Create Menu
@router.post("/", status_code=201)
async def create_menu(menu: schemas.MenuBase, db: AsyncSession = Depends(get_db)):
    db_menu = await crud.create_menu(db, menu)

    count_children = await crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"],
    )


# Get menu by id
@router.get("/{menu_id}")
async def read_menu(
    db_menu: Annotated[Menu, Depends(return_menu_or_404)],
    db: AsyncSession = Depends(get_db),
):
    count_children = await crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"],
    )


# Delete menu by id
@router.delete("/{menu_id}")
async def delete_menu(
    db_menu: Annotated[Menu, Depends(return_menu_or_404)],
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_menu(db, db_menu)
    return {"status": True, "message": "The menu has been deleted"}


# Patch menu by id
@router.patch("/{menu_id}")
async def patch_menu(
    db_menu: Annotated[Menu, Depends(return_menu_or_404)],
    menu_data: schemas.MenuBase,
    db: AsyncSession = Depends(get_db),
):
    db_menu = await crud.patch_menu(db, menu_data, db_menu)

    count_children = await crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"],
    )
