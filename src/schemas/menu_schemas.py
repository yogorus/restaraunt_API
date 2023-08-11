"""Pydantic Menu models for data validation"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict


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
