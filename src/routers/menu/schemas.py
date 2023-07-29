from pydantic import BaseModel, ConfigDict
from uuid import UUID


# from ..submenu import schemas as submenu
class MenuBase(BaseModel):
    title: str
    description: str


class Menu(MenuBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class MenuOutput(Menu):
    submenus_count: int
    dishes_count: int
