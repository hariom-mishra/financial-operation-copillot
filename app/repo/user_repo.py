from sqlalchemy.ext.asyncio import AsyncSession
from schema.users import Users
from sqlalchemy import select
from models.users import SignUpUser, GetUsersParams
from core.security import hash_password
from core.exceptions import ExpenseException
from typing import Optional, List

class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: SignUpUser):
        try:
            new_user = Users(
                email=user.email,
                hashed_password=hash_password(user.password),
                name=user.name,
                role= "user" if user.email!= "admin@gmail.com" else "admin"
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_user_by_email(self, email: str) -> Optional[Users]:
        try:
            result = await self.db.execute(select(Users).where(Users.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_user_by_id(self, user_id: int) -> Optional[Users]:
        try:
            result = await self.db.execute(select(Users).where(Users.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_users(self, params: GetUsersParams) -> List[Users]:
        try:
            query = select(Users)
            if params.role:
                query = query.where(Users.role == params.role)
            query = query.limit(params.limit).offset(params.offset)
            res = await self.db.execute(query)
            return res.scalars().all()
        except Exception as e:
            raise ExpenseException(str(e))