from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, schemas

from src.database import get_db
from src.routers.utils import check_menu_id, check_submenu_id
from src.routers.menu.crud import get_menu_by_id

router = APIRouter(prefix=("/api/v1/menus"))


# Get list of all submenus
@router.get("/{menu_id}/submenus", dependencies=[Depends(check_menu_id)])
def read_submenus(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = get_menu_by_id(db, menu_id)
    db_submenus = crud.get_submenus(db, db_menu)

    submenus = [
        schemas.SubmenuOutput(
            **submenu.__dict__, dishes_count=crud.count_dishes(db, submenu)
        )
        for submenu in db_submenus
    ]
    return submenus


# Create submenu
@router.post(
    "/{menu_id}/submenus", status_code=201, dependencies=[Depends(check_menu_id)]
)
def create_submenu(
    menu_id: UUID,
    submenu: schemas.SubmenuBase,
    db: Session = Depends(get_db),
):
    if crud.count_same_titles(db, submenu.title) >= 1:
        raise HTTPException(409, detail="submenu with that title already exists")

    db_submenu = crud.create_submenu(db, menu_id, submenu)
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=crud.count_dishes(db, db_submenu)
    )


# Get submenu by id
@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    dependencies=[Depends(check_menu_id), Depends(check_submenu_id)],
)
def read_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, submenu_id)
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=crud.count_dishes(db, db_submenu)
    )


# Update submenu
@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    dependencies=[Depends(check_menu_id), Depends(check_submenu_id)],
)
def update_submenu(
    submenu_id: UUID,
    menu_id: UUID,
    submenu_data: schemas.SubmenuBase,
    db: Session = Depends(get_db),
):
    db_submenu = crud.get_submenu_by_id(db, submenu_id)

    if crud.count_same_titles(db, submenu_data.title) > 1:
        raise HTTPException(409, detail="submenu with that title already exists")

    db_submenu = crud.patch_submenu(db, submenu_data, db_submenu)
    return schemas.SubmenuOutput(
        **db_submenu.__dict__, dishes_count=crud.count_dishes(db, db_submenu)
    )


# Delete submenu
@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    dependencies=[Depends(check_menu_id), Depends(check_submenu_id)],
)
def delete_submenu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_by_id(db, submenu_id)

    crud.delete_submenu(db, db_submenu)
    return {"status": True, "message": "The submenu has been deleted"}
