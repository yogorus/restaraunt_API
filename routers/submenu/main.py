import sys
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas
# from .utils import validate_menu_id

sys.path.append("..")
from database import SessionLocal, engine, get_db
from routers.menu.crud import get_menu_by_id

router = APIRouter(
    prefix=('/api/v1/menus')
)

# Get list of all submenus
@router.get('/{menu_id}/submenus', status_code=200)
# @validate_menu_id
def read_submenus(menu_id: UUID, response: Response, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db, menu_id)
    
    if menu:
        submenus = crud.get_submenus(db, menu)
        
        data = [
            {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': submenu.dishes_count()
            }
            for submenu in submenus
        ]
        return data
    
    response.status_code = 404
    return {'detail': 'menu not found'}        
    
# Create submenu (decorator doesn't work here)
@router.post('/{menu_id}/submenus', status_code=201)
def create_submenu(menu_id: UUID, submenu: schemas.SubmenuBase, 
                   response: Response, db: Session = Depends(get_db)):
    
    menu = get_menu_by_id(db, menu_id)
    if menu:
        
        if crud.count_same_titles(db, submenu.title) >= 1:
            response.status_code = 409
            return {'detail': 'submenu with that title already exists!'}
        
        submenu = crud.create_submenu(db, menu_id, submenu)
        return {
            'id': submenu.id,
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': submenu.dishes_count()
        }
    
    response.status_code = 404
    return {'detail': 'menu not found'}
    
# Get submenu by id
@router.get('/{menu_id}/submenus/{submenu_id}', status_code=200)
def read_submenu(menu_id: UUID, submenu_id: UUID, 
                 response: Response, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db, menu_id)
    if menu:
        submenu = crud.get_submenu_by_id(db, submenu_id)
        
        if submenu:
            data = {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': submenu.dishes_count()
            }
            return data
        
        response.status_code = 404
        return {'detail': 'submenu not found'}
    
    response.status_code = 404
    return {'detail': 'menu not found'}

# Update submenu
@router.patch('/{menu_id}/submenus/{submenu_id}')
def update_submenu(menu_id: UUID, submenu_id: UUID, 
                   submenu_data: schemas.SubmenuBase,
                   response: Response, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db, menu_id)
    if menu:
        db_submenu = crud.get_submenu_by_id(db, submenu_id)
        
        if db_submenu:
            if crud.count_same_titles(db, submenu_data.title) > 1:
                response.status_code = 409
                return {'detail': 'submenu with that title already exists'}
            

            # if submenu_data.title in titles:
            
            new_submenu = crud.patch_submenu(db, submenu_data, db_submenu)
            data = {
                'id': new_submenu.id,
                'title': new_submenu.title,
                'description': new_submenu.description,
                'dishes_count': new_submenu.dishes_count()
            }
            return data
        
        response.status_code = 404
        return {'detail': 'submenu not found'}

    response.status_code = 404
    return {'detail': 'submenu not found'}

# Delete submenu
@router.delete('/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: UUID, submenu_id: UUID, 
                   response: Response, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, submenu_id)
    
    if db_submenu:
        crud.delete_submenu(db, db_submenu)
        return {
            "status": True,
            "message": "The submenu has been deleted"
        }
    
    response.status_code = 404
    return{'detail': 'submenu not found'}
