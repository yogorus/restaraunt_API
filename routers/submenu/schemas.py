from pydantic import BaseModel
from uuid import UUID

class SubmenuBase(BaseModel):
    title: str
    description: str

class SubmenuForeignKey(SubmenuBase):
    menu_id: UUID
    
    # class Confing:
    #     orm_mode = True

class Submenu(SubmenuBase):
    id: UUID

    class Config:
        orm_mode = True