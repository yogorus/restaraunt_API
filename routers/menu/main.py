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

# List all menus
@router.get('/')
def read_menus(db: Session = Depends(get_db)):
    db_menus = crud.get_menus(db)
    data = [
        {
            "id": db_menu.id,
            "title": db_menu.title,
            "description": db_menu.description,
            "submenus_count": db_menu.submenus_count(),
            "dishes_count": db_menu.dishes_count()
        }
        for db_menu in db_menus
    ]
    
    return data

# Create Menu
@router.post('/', response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuBase, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)
    
# Get menu by id
@router.get('/{id}', status_code=200)
def read_menu(id: UUID, response: Response, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    
    if db_menu:
        data = {
            "id": db_menu.id,
            "title": db_menu.title,
            "description": db_menu.description,
            "submenus_count": db_menu.submenus_count(),
            "dishes_count": db_menu.dishes_count()
        }
        return data
    
    response.status_code = 404
    return {'detail': 'menu not found'}

# Delete menu by id
@router.delete('/{id}', status_code=200)
def delete_menu(id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    if db_menu:
        crud.delete_menu(db, db_menu)
        return {
            "status": True,
            "message": "The menu has been deleted"
        }
    
    return HTTPException(status_code=404, detail='menu not found')

# Patch menu by id
@router.patch('/{id}', status_code=200)
def patch_menu(id: UUID, menu: schemas.MenuBase, response: Response, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_id(db, id)
    if db_menu:
        return crud.patch_menu(db, data=menu, db_menu=db_menu)
    
    response.status_code = 404
    return {'detail': 'menu not found'}
