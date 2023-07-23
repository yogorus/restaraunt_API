import sys
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas

sys.path.append("..")
from models import Submenu, Menu


def get_submenus(db: Session, menu: Menu) -> list[Submenu]:
    return menu.submenus


def get_submenu_by_id(db: Session, id: UUID) -> Submenu:
    return db.query(Submenu).filter(Submenu.id == id).first()


def create_submenu(db: Session, menu_id: UUID, submenu: schemas.SubmenuBase) -> Submenu:
    new_submenu = schemas.SubmenuForeignKey(**submenu.model_dump(), menu_id=menu_id)
    db_submenu = Submenu(**new_submenu.model_dump())
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def patch_submenu(
    db: Session, data: schemas.SubmenuBase, db_submenu: Submenu
) -> Submenu:
    db_submenu.title = data.title  # type: ignore
    db_submenu.description = data.description  # type: ignore
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, db_submenu: Submenu):
    db.delete(db_submenu)
    db.commit()


def count_same_titles(db: Session, title: str) -> int:
    count = db.query(Submenu).filter(Submenu.title == title).count()
    return count
