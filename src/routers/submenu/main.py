"""Submenu routings"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from src.models import Menu
from src.schemas.submenu_schemas import SubmenuBase, SubmenuOutput
from src.services.submenu.submenu_service import SubmenuService
from src.services.utils import return_menu_or_404

router = APIRouter(prefix='/api/v1/menus')


def common_params(menu_id: UUID, submenu_id: UUID):
    """URL ID's"""
    return {'menu_id': menu_id, 'id': submenu_id}


CommonDep = Annotated[dict, Depends(common_params)]


# Get list of all submenus
@router.get(
    '/{menu_id}/submenus/',
    response_model=list[SubmenuOutput],
    summary='Get list of all submenus of parent menu',
    description="If parent submenu doesn't exist, an 404 error would be raised",
)
async def read_submenus(
    menu: Menu = Depends(return_menu_or_404), submenu: SubmenuService = Depends()
) -> list[dict]:
    """All submenus route"""
    return await submenu.get_submenus(count_children=True, menu_id=menu.id)


# Create submenu
@router.post(
    '/{menu_id}/submenus/',
    status_code=201,
    response_model=SubmenuOutput,
    summary='Create submenu',
    description='Menu ID should be valid',
)
async def create_submenu(
    submenu_data: SubmenuBase,
    background_tasks: BackgroundTasks,
    submenu: SubmenuService = Depends(),
    menu: Menu = Depends(return_menu_or_404),
) -> dict:
    """Create submenu route"""
    return await submenu.create_submenu(
        submenu_data, background_tasks, count_children=True, menu_id=menu.id
    )


# Get submenu by id
@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuOutput,
    summary='Get submenu by ID',
    description='Menu ID should be valid',
)
async def read_submenu(
    submenu_id: UUID,
    menu: Menu = Depends(return_menu_or_404),
    submenu: SubmenuService = Depends(),
) -> dict:
    """Read submenu by id"""
    return await submenu.get_submenu(
        count_children=True, menu_id=menu.id, id=submenu_id
    )


# Update submenu
@router.patch(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuOutput,
    summary='Update submenu',
    description='Menu ID and submenu ID should be valid',
)
async def update_submenu(
    submenu_id: UUID,
    submenu_data: SubmenuBase,
    background_tasks: BackgroundTasks,
    submenu: SubmenuService = Depends(),
    menu: Menu = Depends(return_menu_or_404),
) -> dict:
    """Update submenu route"""
    return await submenu.update_submenu(
        submenu_data,
        background_tasks,
        count_children=True,
        id=submenu_id,
        menu_id=menu.id,
    )


# Delete submenu
@router.delete(
    '/{menu_id}/submenus/{submenu_id}',
    summary='Delete submenu by id',
    description='Menu ID and submenu ID should be valid',
)
async def delete_submenu(
    submenu_id: UUID,
    background_tasks: BackgroundTasks,
    menu: Menu = Depends(return_menu_or_404),
    submenu: SubmenuService = Depends(),
) -> dict:
    """Delete submenu route"""
    await submenu.delete_submenu(background_tasks, id=submenu_id, menu_id=menu.id)
    return {'status': True, 'message': 'The submenu has been deleted'}
