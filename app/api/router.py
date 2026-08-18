from fastapi import APIRouter
from api.expenses import router as expense_router
from api.auth import router as auth_router
from api.users import router as user_router

router = APIRouter(prefix="/v1", tags=["Financial Operations"])

router.include_router(expense_router)
router.include_router(auth_router)
router.include_router(user_router)


@router.get("/health")
def check_health():
    return {"status": "OK"}