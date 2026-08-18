from fastapi import APIRouter

router = APIRouter(prefix="/finops", tags=["Financial Operations"])

@router.get("/health")
def check_health():
    return {"status": "OK"}