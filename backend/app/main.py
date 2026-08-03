from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.target import Target

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HunterV API",
    description="AI-Assisted Bug Hunting Framework",
    version="0.1.0"
)

# Import AFTER app creation
from app.api.target_routes import router as target_router

app.include_router(target_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to HunterV!",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }