from sqlalchemy.ext.asyncio import AsyncSession
from repo.expense_repo import ExpenseRepo
from models.expenses import GetExpenses, AddExpenses, UpdateExpenses
from core.exceptions import ExpenseException
from typing import Optional
from datetime import datetime

class ExpenseServices:
    def __init__(self, db: AsyncSession):
        self.repo = ExpenseRepo(db)
    
    async def get_expenses(self, user_id: int, params: GetExpenses):
        try:
            return await self.repo.get_expenses(
                user_id=user_id,
                limit=params.limit,
                offset=params.offset,
                category=params.category,
                from_date=params.from_date,
                to_date=params.to_date
                )
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def add_expense(self, expense: AddExpenses, user_id: int):
        try:
            return await self.repo.add_expense(expense, user_id)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def search_expenses(self, user_id: int, keyword: str, limit: int = 20, offset: int = 0):
        try:
            return await self.repo.search_expenses(user_id, keyword, limit, offset)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def get_summary(self, user_id: int, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None):
        try:
            return await self.repo.get_summary(user_id, from_date, to_date)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def update_expense(self, expense_id: int, user_id: int, data: UpdateExpenses):
        try:
            return await self.repo.update_expense(expense_id, user_id, data)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))

    async def delete_expense(self, expense_id: int, user_id: int):
        try:
            return await self.repo.delete_expense(expense_id, user_id)
        except ExpenseException as e:
            raise e
        except Exception as e:
            raise ExpenseException(str(e))