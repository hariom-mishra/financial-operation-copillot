from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.expenses import GetExpenses, SearchExpenses
from schema.expenses import Expenses
from core.exceptions import ExpenseException
from typing import Optional
from datetime import date

class ExpenseRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_expenses(self, user_id: int, limit: int, offset: int, category: Optional[str], from_date: Optional[date], to_date: Optional[date]):
        try:
            query = select(Expenses)
            query = query.where(Expenses.user_id == user_id)
            if category:
                query = query.where(Expenses.category == category)
            if from_date:
                query = query.where(Expenses.date >= str(from_date))
            if to_date:
                query = query.where(Expenses.date <= str(to_date))
            query = query.limit(limit).offset(offset)
            res = await self.db.execute(query)
            return res.scalars().all()
        except Exception as e:
            raise ExpenseException(str(e))
        