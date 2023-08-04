"""Main file for app"""
from fastapi import FastAPI

from src.routers.menu import main as menu

# from .database import engine
# from . import models


# from src.routers.submenu import main as submenu_router
# from src.routers.dish import main as dish_router


# models.Base.metadata.create_all(bind=engine)
# create_db_and_tables()

app = FastAPI()

# menu_router = menu_router.router
# submenu_router = submenu_router.router
# dish_router = dish_router.router

app.include_router(menu.router, tags=['menu'])
# app.include_router(submenu_router, tags=["submenu"])
# app.include_router(dish_router, tags=["dish"])
