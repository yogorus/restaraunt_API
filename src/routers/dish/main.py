"""Dish routing"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from src.models import Submenu
from src.schemas.dish_schemas import Dish, DishBaseModel
from src.services.dish.dish_service import DishService
from src.services.utils import return_submenu_or_404

router = APIRouter(prefix='/api/v1/menus')
BASE_URL = '/{menu_id}/submenus/{submenu_id}/dishes'


def common_params(menu_id: UUID, submenu_id: UUID):
    """Url ID's"""
    return {'menu_id': menu_id, 'submenu_id': submenu_id}


CommonDep = Annotated[dict, Depends(common_params)]


# # Get list of all dishes
# # Code is designed to throw an error if parent menu and submenu doesn't exist,
# but test expects an empty output and 200 status code,
# so no dependencies in this route
@router.get(f'{BASE_URL}/', response_model=list[Dish], summary='Get all dishes')
async def read_dishes(
    commons: CommonDep, dish: DishService = Depends(), filter_by_submenu: bool = False
):
    """Route that returns list of dishes"""
    return await dish.get_dishes(filter_by_submenu=filter_by_submenu, **commons)


# # Create Dish
@router.post(
    f'{BASE_URL}/',
    status_code=201,
    response_model=Dish,
    summary='Create dish',
    description="If parent ID's are not valid, an exception would be raised",
)
async def create_dish(
    dish_data: DishBaseModel,
    background_tasks: BackgroundTasks,
    submenu: Submenu = Depends(return_submenu_or_404),
    dish: DishService = Depends(),
):
    """Route that creates dishes"""
    return await dish.create_dish(
        dish_data, background_tasks, submenu_id=submenu.id, menu_id=submenu.menu_id
    )


# # # Read dish by id
@router.get(
    f'{BASE_URL}/{{dish_id}}',
    response_model=Dish,
    summary='Get dish by its ID',
    description="If parent ID's are not valid, an exception would be raised",
)
async def read_dish(
    dish_id: UUID,
    submenu: Submenu = Depends(return_submenu_or_404),
    dish: DishService = Depends(),
):
    """Return dish route"""
    return await dish.get_dish(
        submenu_id=submenu.id, id=dish_id, menu_id=submenu.menu_id
    )


# # Patch dish
@router.patch(
    f'{BASE_URL}/{{dish_id}}',
    response_model=Dish,
    summary='Update dish with provided information',
    description="If parent ID's are not valid, an exception would be raised",
)
async def patch_dish(
    dish_id: UUID,
    dish_data: DishBaseModel,
    background_tasks: BackgroundTasks,
    submenu: Submenu = Depends(return_submenu_or_404),
    dish: DishService = Depends(),
):
    """Update dish route"""
    return await dish.update_dish(
        dish_data,
        background_tasks,
        submenu_id=submenu.id,
        id=dish_id,
        menu_id=submenu.menu_id,
    )


@router.delete(
    f'{BASE_URL}/{{dish_id}}',
    summary='Delete dish by ID',
    description="If parent ID's are not valid, an exception would be raised",
)
async def delete_dish(
    dish_id: UUID,
    background_tasks: BackgroundTasks,
    submenu: Submenu = Depends(return_submenu_or_404),
    dish: DishService = Depends(),
):
    """Delete dish route"""
    return await dish.delete_dish(
        background_tasks, submenu_id=submenu.id, id=dish_id, menu_id=submenu.menu_id
    )
