# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from uuid import UUID
# from . import crud, schemas

# from src.database import get_db
# from src.routers.submenu.crud import get_submenu_by_id
# from src.routers.utils import check_menu_id, check_submenu_id, check_dish_id

# router = APIRouter(prefix=("/api/v1/menus"))
# base_url = "/{menu_id}/submenus/{submenu_id}/dishes"
# dependencies = [Depends(check_menu_id), Depends(check_submenu_id)]


# def common_params(menu_id: UUID, submenu_id: UUID):
#     return {"menu_id": menu_id, "submenu_id": submenu_id}


# CommonDep = Annotated[dict, Depends(common_params)]


# # Get list of all dishes
# # Code is designed to throw an error if parent menu and submenu doesn't exist, but test expects an empty output and 200 statud code, so no dependencies in this route
# @router.get(f"{base_url}/", response_model=list[schemas.Dish])
# def read_dishes(commons: CommonDep, db: Session = Depends(get_db)):
#     db_submenu = get_submenu_by_id(db, commons["submenu_id"])
#     return crud.get_dishes(db_submenu) if db_submenu else []


# # Create Dish
# @router.post(
#     f"{base_url}/",
#     status_code=201,
#     dependencies=dependencies,
#     response_model=schemas.Dish,
# )
# def create_dish(
#     commons: CommonDep, dish: schemas.DishBaseModel, db: Session = Depends(get_db)
# ):
#     if crud.count_same_titles(db, dish.title) >= 1:
#         raise HTTPException(409, detail="submenu with that title already exists")

#     db_submenu = crud.create_dish(db, dish, commons["submenu_id"])
#     return db_submenu


# # Read dish by id
# @router.get(
#     f"{base_url}/{{dish_id}}",
#     dependencies=dependencies + [Depends(check_dish_id)],
#     response_model=schemas.Dish,
# )
# def read_dish(commons: CommonDep, dish_id: UUID, db: Session = Depends(get_db)):
#     db_dish = crud.get_dish_by_id(db, dish_id)
#     return db_dish


# # Patch dish
# @router.patch(
#     f"{base_url}/{{dish_id}}",
#     dependencies=dependencies + [Depends(check_dish_id)],
#     response_model=schemas.Dish,
# )
# def patch_dish(
#     commons: CommonDep,
#     dish_id: UUID,
#     dish_data: schemas.DishBaseModel,
#     db: Session = Depends(get_db),
# ):
#     db_dish = crud.get_dish_by_id(db, dish_id)

#     if crud.count_same_titles(db, dish_data.title) > 1:
#         raise HTTPException(
#             status_code=409, detail="dish with that title already exists"
#         )
#     return crud.update_dish(db, db_dish, dish_data)


# @router.delete(
#     f"{base_url}/{{dish_id}}",
#     dependencies=dependencies + [Depends(check_dish_id)],
# )
# def delete_dish(commons: CommonDep, dish_id: UUID, db: Session = Depends(get_db)):
#     db_dish = crud.get_dish_by_id(db, dish_id)
#     crud.delete_dish(db, db_dish)
#     return {"status": True, "message": "The dish has been deleted"}
