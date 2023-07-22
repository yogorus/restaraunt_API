from fastapi import FastAPI

from database import engine, SessionLocal
import models

import routers.menu.main
import routers.submenu.main

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

menu_router = routers.menu.main.router
submenu_router = routers.submenu.main.router

app.include_router(menu_router, tags=['menu'])
app.include_router(submenu_router, tags=['submenu'])