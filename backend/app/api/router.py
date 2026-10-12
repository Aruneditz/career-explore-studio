from fastapi import APIRouter
from app.api import health, auth, goals, skills, progress, overall_evaluation, final_interview, certificates, ai

api_router = APIRouter()

# Health endpoints
api_router.include_router(health.router)

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Goals & Career Tracks endpoints
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])

# Skills & Topics Workflow endpoints
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])

# Progress & Completion endpoints
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])

# Overall Cross-Skill Evaluation endpoints (Section 20)
api_router.include_router(overall_evaluation.router, prefix="/overall-evaluation", tags=["Overall Evaluation"])

# Capstone Final Interview Preparation endpoints (Sections 21, 22, 23)
api_router.include_router(final_interview.router, prefix="/interview-prep", tags=["Final Interview Preparation"])

# Certificate endpoints (Upgrade #5)
api_router.include_router(certificates.router)

# AI Assistant endpoints (Upgrade #6)
api_router.include_router(ai.router, prefix="/ai", tags=["AI Assistant"])
