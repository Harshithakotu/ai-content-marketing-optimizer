from fastapi import APIRouter
from pydantic import BaseModel
from app.services.recommender import optimize_content

router = APIRouter(prefix="/optimize", tags=["Optimization"])

class OptimizationInput(BaseModel):
    text: str

@router.post("/")
def optimize(payload: OptimizationInput):
    optimized = optimize_content(payload.text)
    return {
        "original": payload.text,
        "optimized": optimized
    }
