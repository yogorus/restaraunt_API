# from typing import Callable
# from sqlalchemy import select, func
# from sqlalchemy.ext.asyncio import AsyncSession
# from uuid import UUID
# from . import schemas

# from src.models import Submenu, Dish


# async def count_same_titles(db: AsyncSession, title: str) -> int:
#     query = select(func.count(Dish.title).label("title_count")).filter(
#         Dish.title == title
#     )
#     result = await db.execute(query)
#     result = result.first()
#     if result:
#         return result.title_count
#     return 0
#     # return db.query(Dish).filter(Dish.title == title).count()


# async def get_dishes(submenu: Submenu) -> list[Dish]:
#     return submenu.dishes


# async def create_dish(db: AsyncSession, dish: schemas.DishBaseModel, submenu_id: UUID):
#     db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
#     db.add(db_dish)
#     await db.commit()
#     await db.refresh(db_dish)
#     return db_dish


# async def get_dish_by_id(db: AsyncSession, dish_id: UUID) -> Dish | None:
#     query = select(Dish).filter(Dish.id == dish_id)
#     result = await db.execute(query)
#     return result.scalar()
#     # return db.query(Dish).filter(Dish.id == dish_id).first()


# async def update_dish(
#     db: AsyncSession, db_dish: Dish, dish_data: schemas.DishBaseModel
# ):
#     db_dish.title = dish_data.title  # type: ignore
#     db_dish.description = dish_data.description  # type: ignore
#     db_dish.price = dish_data.price
#     await db.commit()
#     await db.refresh(db_dish)
#     return db_dish


# async def delete_dish(db: AsyncSession, db_dish: Dish):
#     await db.delete(db_dish)
#     await db.commit()
