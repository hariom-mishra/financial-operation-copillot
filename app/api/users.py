from fastapi import APIRouter, Depends, HTTPException
from models.users import GetUsersParams, UserResponse
from typing import List
from core.db import get_db
from services.user_services import UserService
from core.exceptions import ExpenseException
from core.dependency import RoleChecker

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse], admin_user = RoleChecker(["admin"]))
async def get_users(params: GetUsersParams = Depends(), db = Depends(get_db)):
    try:
        service = UserService(db)
        return await service.get_users(params)
    except ExpenseException as e:
        raise
