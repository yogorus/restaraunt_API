import sys
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas


sys.path.append("...")
from database import SessionLocal, engine, get_db

router = APIRouter(
    prefix=('/api/v1/menus')
)

@router.get('/{menu_id}/submenus')
def read_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    return {'detail': 'works'}