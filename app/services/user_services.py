from repo.user_repo import UserRepo
from models.users import SignUpUser, LoginUser, GetUsersParams
from core.exceptions import UserExistsException, UserNotFoundException, InvalidCredentialsException, ExpenseException
from core.security import create_access_token, verify_password, create_refresh_token, decode_token

class UserService:
    def __init__(self, db):
        self.user_repo = UserRepo(db)

    async def register_user(self, user: SignUpUser):
        try:
            user_exists = await self.user_repo.get_user_by_email(user.email)
            if user_exists:
                raise UserExistsException(f"User with email {user.email} already exists")
            
            new_user = await self.user_repo.create_user(user)
            return new_user
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def login_user(self, user: LoginUser):
        try:
            user_exists = await self.user_repo.get_user_by_email(user.email)
            if not user_exists:
                raise UserNotFoundException(f"User with email {user.email} does not exist")
            
            if not verify_password(user.password, user_exists.hashed_password):
                raise InvalidCredentialsException("Invalid credentials")
            
            access_token = create_access_token(user_exists)
            refresh_token = create_refresh_token(user_exists)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "data": {   
                    "id": user_exists.id,
                    "email": user_exists.email,
                    "name": user_exists.name
                }
            }
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def refresh_access_token(self, refresh_token: str):
        try:
            payload = decode_token(refresh_token)
            if not payload:
                raise InvalidCredentialsException("Invalid token")
        
            user_id = payload.get("user_id")

            user_exists = await self.user_repo.get_user_by_id(user_id)
            if not user_exists:
                raise UserNotFoundException("User not found")
        
            new_access_token = create_access_token(user_exists)
            return {
                "access_token": new_access_token
            }
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_users(self, params: GetUsersParams):
        try:
            return await self.user_repo.get_users(params)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_user_by_id(self, user_id: int):
        try:
            return await self.user_repo.get_user_by_id(user_id)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))