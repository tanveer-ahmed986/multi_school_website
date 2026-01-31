"""
Multi-School Website Platform - FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import public, auth, content, schools

app = FastAPI(
    title="Multi-School Website Platform API",
    description="Backend API for multi-tenant school websites.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(public.router)
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(schools.router)


@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "ok", "service": "multi-school-api"}
