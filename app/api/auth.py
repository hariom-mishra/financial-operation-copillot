from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])
#singup
@router.post("/signup")
def signup():
    pass
#login
@router.post("/login")
def login():
    pass
