"""Router to get everything"""
from fastapi import APIRouter, Depends

from src.schemas.menu_schemas import MenuGeneral
from src.services.general.general_service import GeneralService

router = APIRouter(prefix='/api/v1')


@router.get(
    '/all', summary='Get all data from the database', response_model=list[MenuGeneral]
)
async def get_all(general: GeneralService = Depends()):
    """Request to get everything from the database"""
    return await general.get_all()
