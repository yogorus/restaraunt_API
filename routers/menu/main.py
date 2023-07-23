import sys
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas

sys.path.append("..")
from database import get_db
from routers.utils import check_menu_id

router = APIRouter(prefix=("/api/v1/menus"))


# List all menus
@router.get("/")
def read_menus(db: Session = Depends(get_db)):
    db_menus = crud.get_menus(db)
    data = [
        {
            "id": db_menu.id,
            "title": db_menu.title,
            "description": db_menu.description,
            "submenus_count": db_menu.submenus_count(),
            "dishes_count": db_menu.dishes_count(),
        }
        for db_menu in db_menus
    ]
    return data


# Create Menu
@router.post("/", status_code=201)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    db_menu = crud.create_menu(db=db, menu=menu)
    data = {
        "id": db_menu.id,
        "title": db_menu.title,
        "description": db_menu.description,
        "submenus_count": db_menu.submenus_count(),
        "dishes_count": db_menu.dishes_count(),
    }
    return data


# Get menu by id
@router.get("/{menu_id}", dependencies=[Depends(check_menu_id)])
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id)

    data = {
        "id": db_menu.id,
        "title": db_menu.title,
        "description": db_menu.description,
        "submenus_count": db_menu.submenus_count(),
        "dishes_count": db_menu.dishes_count(),
    }
    return data


# Delete menu by id
@router.delete("/{menu_id}", dependencies=[Depends(check_menu_id)])
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id)

    crud.delete_menu(db, db_menu)
    return {"status": True, "message": "The menu has been deleted"}


# Patch menu by id
@router.patch("/{menu_id}", dependencies=[Depends(check_menu_id)])
def patch_menu(menu_id: UUID, menu: schemas.MenuBase, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, menu_id)
    return crud.patch_menu(db, data=menu, db_menu=db_menu)
