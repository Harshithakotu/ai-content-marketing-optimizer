from fastapi import APIRouter
from app.services.ab_engine import run_ab_testing

router = APIRouter(prefix="/ab-testing", tags=["AB Testing"])

@router.get("/run")
def run_test():
    results = run_ab_testing()
    return {"results": results}
