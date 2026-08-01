from fastapi import FastAPI

app = FastAPI(
    title="HunterV API",
    description="AI-Assisted Bug Hunting Framework",
    version="0.1.0"
)

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