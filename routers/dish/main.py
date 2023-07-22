import sys
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas

sys.path.append("..")
from database import get_db
from routers.submenu.crud import get_submenu_by_id
from routers.utils import check_menu_id, check_submenu_id

router = APIRouter(
    prefix=('/api/v1/menus')
)
base_url = '/{menu_id}/submenus/{submenu_id}'
dependencies = [Depends(check_menu_id), Depends(check_submenu_id)]

def common_params(menu_id: UUID, submenu_id: UUID):
    return {"menu_id": menu_id, 'submenu_id': submenu_id}

CommonDep = Annotated[dict, Depends(common_params)]

# Get list of all dishes
@router.get(f'{base_url}/', dependencies=dependencies)
def read_dishes(commons: CommonDep, db: Session = Depends(get_db)):
    db_submenu = get_submenu_by_id(db, commons['submenu_id'])
    return crud.get_dishes(db_submenu)
# Create Dish
@router.post(f'{base_url}/', dependencies=dependencies)
def create_dish(commons: CommonDep, dish: schemas.SubmenuBaseModel, db: Session = Depends(get_db)):
    price = float(dish.price)
    return price