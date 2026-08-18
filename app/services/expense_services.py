from sqlalchemy.ext.asyncio import AsyncSession
from repo.expense_repo import ExpenseRepo
from models.expenses import GetExpenses
from core.exceptions import ExpenseException

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
        except Exception as e:
            raise ExpenseException(str(e))

    