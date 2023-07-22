from pydantic import BaseModel
from uuid import UUID

class SubmenuBase(BaseModel):
    title: str
    description: str

class Submenu(SubmenuBase):
    id: UUID
    
    class Confing:
        orm_mode = True