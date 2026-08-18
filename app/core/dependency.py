from core.db import get_db
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_token
from core.exceptions import InvalidCredentialsException, TokenNotProvidedException, ExpenseException, UnauthorizedException, UserNotFoundException
from services.user_services import UserService
from schema.users import Users


async def get_current_user(
    db = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(HTTPBearer())
):
    if not token:
        raise TokenNotProvidedException()
    payload = decode_token(token.credentials)
    if not payload:
        raise InvalidCredentialsException()
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(payload["user_id"])
        if not user:
            raise UserNotFoundException()
        return user
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))

class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Users = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise UnauthorizedException("You are not authorized to perform this action")
        return user

    
    