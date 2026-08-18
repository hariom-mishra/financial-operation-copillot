from pydantic import BaseModel

class BaseUser(BaseModel):
    email: str
    password: str

class SignUpUser(BaseUser):
    name: str

class LoginUser(BaseUser):
    pass

class UserResponse(BaseUser):
    id: int
    role: str
    model_config = ConfigDict(
        from_attributes=True
    )


