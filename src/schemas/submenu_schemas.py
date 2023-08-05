"""Submenu pydantic schemas"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubmenuBase(BaseModel):
    """Input schema"""

    title: str
    description: str


class SubmenuForeignKey(SubmenuBase):
    """Schema that passes parent menu_id"""

    menu_id: UUID

    # class Confing:
    #     orm_mode = True


class Submenu(SubmenuBase):
    """Schema after creation"""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class SubmenuOutput(Submenu):
    """Schema for output"""

    dishes_count: int | None = None
