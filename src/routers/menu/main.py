"""Main Menu Router"""
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from src.schemas import menu_schemas
from src.services.menu.menu_service import MenuService

router = APIRouter(prefix='/api/v1/menus')


# Get all menus
@router.get(
    '/', response_model=list[menu_schemas.MenuOutput], summary='Get list of all menus'
)
async def read_menus(menu: MenuService = Depends()):
    """Return json list of menus"""
    return await menu.get_menus(count_children=True)


# Create Menu
@router.post(
    '/',
    status_code=201,
    response_model=menu_schemas.MenuOutput,
    summary='Create menu with provided title and description',
)
async def create_menu(
    menu_data: menu_schemas.MenuBase,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
):
    """Create Menu and return JSON"""
    return await menu.create_menu(menu_data, background_tasks, count_children=True)


# Get Menu by id
@router.get(
    '/{menu_id}',
    response_model=menu_schemas.MenuOutput,
    summary='Get menu by id provided in URL Path',
    description='Raise 404 if menu not found',
)
async def read_menu(menu_id: UUID, menu: MenuService = Depends()):
    """Return JSON of single menu"""
    return await menu.get_menu(count_children=True, id=menu_id)


# Delete menu by id
@router.delete('/{menu_id}', summary='Delete menu by id')
async def delete_menu(
    menu_id: UUID, background_tasks: BackgroundTasks, menu: MenuService = Depends()
):
    """Delete menu and return json"""
    return await menu.delete_menu(background_tasks, id=menu_id)


# Patch menu by id
@router.patch(
    '/{menu_id}',
    response_model=menu_schemas.MenuOutput,
    summary='Update Menu',
    description='ID should be valid',
)
async def patch_menu(
    menu_id: UUID,
    menu_data: menu_schemas.MenuBase,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
):
    """Update existing Menu and return JSON"""
    return await menu.update_menu(
        menu_data, background_tasks, count_children=True, id=menu_id
    )
