# from pydantic import BaseModel, ConfigDict
# from sqlalchemy import Column
# from uuid import UUID


# class SubmenuBase(BaseModel):
#     title: str
#     description: str


# class SubmenuForeignKey(SubmenuBase):
#     menu_id: UUID

#     # class Confing:
#     #     orm_mode = True


# class Submenu(SubmenuBase):
#     id: UUID

#     model_config = ConfigDict(from_attributes=True)


# class SubmenuOutput(Submenu):
#     dishes_count: int
