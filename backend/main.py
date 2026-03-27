"""
main.py — EconVerse FastAPI Backend
Run: uvicorn backend.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routes.world_routes import router as world_router
from .routes.country_routes import router as country_router

app = FastAPI(
    title="EconVerse API",
    description="World simulation engine — create worlds, build countries, simulate turns.",
    version="0.1.0",
)

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(world_router)
app.include_router(country_router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    index = os.path.join(frontend_path, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"message": "EconVerse API running. Visit /docs for API reference."}

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
