from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseUser(BaseModel):
    email: str
    password: str

class SignUpUser(BaseUser):
    name: str

class LoginUser(BaseUser):
    pass

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    name: str
    model_config = ConfigDict(
        from_attributes=True
    )

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    data: dict

class AccessTokenResponse(BaseModel):
    access_token: str

class GetUsersParams(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = 0
    role: Optional[str] = None

