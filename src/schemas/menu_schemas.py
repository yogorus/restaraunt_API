"""Pydantic Menu models for data validation"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.submenu_schemas import SubmenuGeneral


# from ..submenu import schemas as submenu
class MenuBase(BaseModel):
    """Input pydantic schema"""

    title: str
    description: str
    id: UUID | None = None


class Menu(MenuBase):
    """Schema after creation"""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class MenuOutput(Menu):
    """Output schema for Menus"""

    submenus_count: int | None = None
    dishes_count: int | None = None


class MenuGeneral(Menu):
    """Menu schema of menu with all children"""

    submenus: list[SubmenuGeneral]
