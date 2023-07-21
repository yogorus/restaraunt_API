from fastapi import FastAPI

from database import engine, SessionLocal
import models

import routers.menu.main

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.include_router(routers.menu.main.router, tags=['menu'])