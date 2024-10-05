from fastapi import FastAPI
from database import engine
from models import models
from router.movies import router

app = FastAPI()
app.include_router(router)
models.Base.metadata.create_all(bind=engine)


