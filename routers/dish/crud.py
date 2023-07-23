import sys
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas

sys.path.append("..")
from models import Submenu, Dish


def count_same_titles(db: Session, title: str) -> int:
    return db.query(Dish).filter(Dish.title == title).count()


def get_dishes(submenu: Submenu) -> list[Dish]:
    return submenu.dishes


def create_dish(db: Session, dish: schemas.DishBaseModel, submenu_id: UUID):
    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def get_dish_by_id(db: Session, dish_id: UUID):
    return db.query(Dish).filter(Dish.id == dish_id).first()


def update_dish(db: Session, db_dish: Dish, dish_data: schemas.DishBaseModel):
    db_dish.title = dish_data.title  # type: ignore
    db_dish.description = dish_data.description  # type: ignore
    db_dish.price = dish_data.price
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, db_dish: Dish):
    db.delete(db_dish)
    db.commit()
