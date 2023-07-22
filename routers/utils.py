import sys
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from .menu.crud import get_menu_by_id
sys.path.append('.')
from database import SessionLocal, engine, get_db

def check_menu_id(menu_id: UUID, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')