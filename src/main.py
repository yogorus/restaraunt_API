"""Main file for app"""
from fastapi import FastAPI

from src.routers.dish import main as dish
from src.routers.menu import main as menu
from src.routers.submenu import main as submenu

app = FastAPI()

app.include_router(menu.router, tags=['menu'])
app.include_router(submenu.router, tags=['submenu'])
app.include_router(dish.router, tags=['dish'])
