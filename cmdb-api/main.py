from fastapi import FastAPI
from routes import router as api_router
from database import engine, Base

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include API router with a prefix if necessary
app.include_router(api_router, prefix="/api", tags=["api"])