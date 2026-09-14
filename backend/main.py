import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import profile, skillgap, roadmap, roles, progress

app = FastAPI(
    title="SkillGap AI API",
    description="ML-powered personalized skill recommendation and roadmap system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api")
app.include_router(skillgap.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(progress.router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SkillGap AI API"}


@app.get("/")
def root():
    return {"message": "SkillGap AI API — visit /docs for interactive API documentation"}
