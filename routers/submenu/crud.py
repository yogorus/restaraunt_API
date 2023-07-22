import sys
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas
sys.path.append("..")
from models import Submenu

from routers.menu.crud import get_menu_by_id

def get_submenus(db: Session):
    return db.query(Submenu).all()

def get_submenu_by_id(db: Session, id: UUID):
    return db.query(Submenu).filter(Submenu.id == id).first()

def create_submenu(db: Session, submenu: schemas.SubmenuBase):
    pass