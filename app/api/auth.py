from fastapi import APIRouter, Depends, HTTPException
from models.users import SignUpUser, LoginUser, UserResponse, UserLoginResponse, AccessTokenResponse
from core.db import get_db
from services.user_services import UserService
from core.exceptions import ExpenseException


router = APIRouter(prefix="/auth", tags=["Authentication"])
#singup
@router.post("/signup", response_model=UserResponse)
async def signup(user: SignUpUser, db = Depends(get_db)):
    try:
        services = UserService(db)
        return await services.register_user(user)
    except ExpenseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    

#login
@router.post("/login", response_model=UserLoginResponse)
async def login(user: LoginUser, db = Depends(get_db)):
    try:
        services = UserService(db)
        return await services.login_user(user)
    except ExpenseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_access_token(refresh_token: str, db = Depends(get_db)):
    try:
        services = UserService(db)
        return await services.refresh_access_token(refresh_token)
    except ExpenseException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
