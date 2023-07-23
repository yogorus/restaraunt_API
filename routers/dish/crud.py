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


# def create_dish(db: Session, submenu: schemas.Dish, submenu_id: UUID):
#     new_dish = submenu
#     new_dish.price = float(new_dish.price)
#     return schemas.
