from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas
import asyncio

from src.database import get_db
from src.routers.utils import check_menu_id


router = APIRouter(prefix=("/api/v1/menus"))


# List all menus
@router.get("/")
async def read_menus(db: Session = Depends(get_db)):
    db_menus = await crud.get_menus(db)
    menus = []
    for db_menu in db_menus:
        count_children = await asyncio.gather(crud.count_children(db, db_menu))
        menus.append(
            schemas.MenuOutput(
                **db_menu.__dict__,
                submenus_count=count_children["submenus_count"],
                dishes_count=count_children["dishes_count"]
            )
        )
    return menus


# Create Menu
@router.post("/", status_code=201)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    db_menu = crud.create_menu(db=db, menu=menu)

    count_children = crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"]
    )


# Get menu by id
@router.get("/{menu_id}", dependencies=[Depends(check_menu_id)])
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id)

    count_children = crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"]
    )


# Delete menu by id
@router.delete("/{menu_id}", dependencies=[Depends(check_menu_id)])
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id)

    crud.delete_menu(db, db_menu)
    return {"status": True, "message": "The menu has been deleted"}


# Patch menu by id
@router.patch("/{menu_id}", dependencies=[Depends(check_menu_id)])
def patch_menu(
    menu_id: UUID, menu_data: schemas.MenuBase, db: Session = Depends(get_db)
):
    db_menu = crud.get_menu_by_id(db, menu_id)
    db_menu = crud.patch_menu(db, menu_data, db_menu)

    count_children = crud.count_children(db, db_menu)
    return schemas.MenuOutput(
        **db_menu.__dict__,
        submenus_count=count_children["submenus_count"],
        dishes_count=count_children["dishes_count"]
    )
