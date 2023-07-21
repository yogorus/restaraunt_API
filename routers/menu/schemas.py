from pydantic import BaseModel
from uuid import UUID

# from ..submenu import schemas as submenu
class MenuBase(BaseModel):
    title: str
    description: str

class Menu(MenuBase):
    id: UUID
    
    class Confing:
        orm_mode = True