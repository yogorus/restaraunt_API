from fastapi import FastAPI

from database import engine
import models

import routers.menu.main
import routers.submenu.main
import routers.dish.main

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

menu_router = routers.menu.main.router
submenu_router = routers.submenu.main.router
dish_router = routers.dish.main.router

app.include_router(menu_router, tags=['menu'])
app.include_router(submenu_router, tags=['submenu'])
app.include_router(dish_router, tags=['dish'])