from fastapi import FastAPI
from .routers import users
from .database import engine, Base

# Create the database tables (if needed, typically run once to sync schema)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api")