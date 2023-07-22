import sys
from fastapi import Response, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas

sys.path.append('..')
from routers.menu.crud import get_menu_by_id
from database import get_db
from models import Menu, Submenu

# TODO: Write decorator that will work on every route

# Decorator to check if menu_id in path argument is valid
def validate_menu_id(func):
    def wrapper(menu_id: UUID, response: Response, db: Session = Depends(get_db)):
        menu = get_menu_by_id(db, menu_id)
        if menu:
            return func(menu_id, response, db)
        else:
            response.status_code = 404
            return {'detail': 'Menu not found'}
    return wrapper

    
