# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from uuid import UUID
# from . import crud, schemas

# from src.database import get_db
# from src.models import Dish, Submenu
# from src.routers.submenu.crud import get_submenu_by_id
# from src.routers.utils import (
#     return_submenu_or_404,
#     return_dish_or_404,
# )

# router = APIRouter(prefix=("/api/v1/menus"))
# base_url = "/{menu_id}/submenus/{submenu_id}/dishes"
# # dependencies = [Depends(check_menu_id), Depends(check_submenu_id)]


# def common_params(menu_id: UUID, submenu_id: UUID):
#     return {"menu_id": menu_id, "submenu_id": submenu_id}


# CommonDep = Annotated[dict, Depends(common_params)]


# # Get list of all dishes
# # Code is designed to throw an error if parent menu and submenu doesn't exist,
# but test expects an empty output and 200 status code,
# so no dependencies in this route
# @router.get(f"{base_url}/", response_model=list[schemas.Dish])
# async def read_dishes(commons: CommonDep, db: AsyncSession = Depends(get_db)):
#     db_submenu = await get_submenu_by_id(db, commons["submenu_id"])
#     return await crud.get_dishes(db_submenu) if db_submenu else []


# # Create Dish
# @router.post(
#     f"{base_url}/",
#     status_code=201,
#     response_model=schemas.Dish,
# )
# async def create_dish(
#     dish: schemas.DishBaseModel,
#     db_submenu: Submenu = Depends(return_submenu_or_404),
#     db: AsyncSession = Depends(get_db),
# ):
#     if await crud.count_same_titles(db, dish.title) >= 1:
#         raise HTTPException(409, detail="submenu with that title already exists")

#     db_dish = await crud.create_dish(db, dish, db_submenu.id)  # type: ignore
#     return db_dish


# # # Read dish by id
# @router.get(
#     f"{base_url}/{{dish_id}}",
#     response_model=schemas.Dish,
# )
# def read_dish(
#     db_dish: Dish = Depends(return_dish_or_404), db: AsyncSession = Depends(get_db)
# ):
#     return db_dish


# # # Patch dish
# @router.patch(
#     f"{base_url}/{{dish_id}}",
#     response_model=schemas.Dish,
# )
# async def patch_dish(
#     dish_data: schemas.DishBaseModel,
#     db_dish: Dish = Depends(return_dish_or_404),
#     db: AsyncSession = Depends(get_db),
# ):
#     if await crud.count_same_titles(db, dish_data.title) > 1:
#         raise HTTPException(
#             status_code=409, detail="dish with that title already exists"
#         )
#     return await crud.update_dish(db, db_dish, dish_data)


# @router.delete(
#     f"{base_url}/{{dish_id}}",
# )
# async def delete_dish(
#     db_dish: Dish = Depends(return_dish_or_404), db: AsyncSession = Depends(get_db)
# ):
#     await crud.delete_dish(db, db_dish)
#     return {"status": True, "message": "The dish has been deleted"}
