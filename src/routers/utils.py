from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from .menu.crud import get_menu_by_id
from .submenu.crud import get_submenu_by_id
from .dish.crud import get_dish_by_id

from src.database import get_db


def check_menu_id(menu_id: UUID, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")


def check_submenu_id(submenu_id: UUID, db: Session = Depends(get_db)):
    submenu = get_submenu_by_id(db, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")


def check_dish_id(dish_id: UUID, db: Session = Depends(get_db)):
    dish = get_dish_by_id(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
