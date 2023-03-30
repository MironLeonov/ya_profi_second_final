from fastapi import FastAPI

from database import Model, engine
from routers import group, participant

Model.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(group.router)
app.include_router(participant.router)
