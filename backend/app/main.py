from fastapi import FastAPI

from app.models.target import Target
from app.models.finding import Finding
from app.models.subdomain import Subdomain

app = FastAPI(
    title="HunterV API",
    description="AI-Assisted Bug Hunting Framework",
    version="0.1.0"
)


from app.api.target_routes import router as target_router
from app.api.finding_routes import router as finding_router
from app.api.subdomain_routes import router as subdomain_router
from app.api.recon_job_routes import router as recon_job_router

app.include_router(target_router)
app.include_router(finding_router)
app.include_router(subdomain_router)
app.include_router(recon_job_router)

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