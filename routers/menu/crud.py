import sys
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas
sys.path.append("..")
from models import Menu

def get_menus(db: Session) -> list[Menu]:
    return db.query(Menu).all()

def get_menu_by_id(db: Session, id: UUID) -> Menu:
    return db.query(Menu).filter(Menu.id == id).first()

def create_menu(db: Session, menu: schemas.MenuBase) -> Menu:
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def patch_menu(db: Session, data: schemas.MenuBase, db_menu: Menu) -> Menu:
    db_menu = db_menu
    db_menu.title = data.title # type: ignore
    db_menu.description = data.description # type: ignore
    db.commit()
    db.refresh(db_menu)
    return db_menu
    
def delete_menu(db: Session, db_menu: Menu):
    db.delete(db_menu)
    db.commit()
