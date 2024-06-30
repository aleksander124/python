from fastapi import FastAPI
from routes import router as api_router
from database import engine, Base

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Api for python cmdb",
    description="Api based on postgress database created to store informations about virtualmachines and users",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",         # ReDoc endpoint
    openapi_url="/openapi.json" # OpenAPI schema endpoint
)

# Include API router with a prefix if necessary
app.include_router(api_router, prefix="/api", tags=["api"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)