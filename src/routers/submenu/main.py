from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.schemas.submenu_schemas import SubmenuBase, SubmenuOutput
from src.services.submenu.submenu_service import SubmenuService

router = APIRouter(prefix=('/api/v1/menus'))


def common_params(menu_id: UUID, submenu_id: UUID):
    return {'menu_id': menu_id, 'id': submenu_id}


CommonDep = Annotated[dict, Depends(common_params)]


# Get list of all submenus
@router.get('/{menu_id}/submenus/', response_model=list[SubmenuOutput])
async def read_submenus(menu_id: UUID, submenu: SubmenuService = Depends()):
    """All submenus route"""
    return await submenu.get_submenus(count_children=True, menu_id=menu_id)


# Create submenu
@router.post('/{menu_id}/submenus/', status_code=201, response_model=SubmenuOutput)
async def create_submenu(
    menu_id: UUID, submenu_data: SubmenuBase, submenu: SubmenuService = Depends()
):
    """Create submenu route"""
    return await submenu.create_submenu(
        submenu_data, count_children=True, menu_id=menu_id
    )


# Get submenu by id
@router.get('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOutput)
async def read_submenu(commons: CommonDep, submenu: SubmenuService = Depends()):
    """Read submenu by id"""
    return await submenu.get_submenu(count_children=True, **commons)


# Update submenu
@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOutput)
async def update_submenu(
    commons: CommonDep, submenu_data: SubmenuBase, submenu: SubmenuService = Depends()
):
    """Update submenu route"""
    return await submenu.update_submenu(submenu_data, count_children=True, **commons)


# Delete submenu
@router.delete(
    '/{menu_id}/submenus/{submenu_id}',
)
async def delete_submenu(commons: CommonDep, submenu: SubmenuService = Depends()):
    """Delete submenu route"""
    await submenu.delete_obj(**commons)
    return {'status': True, 'message': 'The submenu has been deleted'}
