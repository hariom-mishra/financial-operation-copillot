from langchain_core.tools import tool
from services.expense_services import ExpenseServices
from core.db import session
from models.expenses import GetExpenses, AddExpenses, ExpenseCategory
from datetime import datetime


class ExpenseToolkit:
    @tool
    async def get_expenses( 
        user_id,
        limit: int = 10, 
        offset: int = 0,
        category: ExpenseCategory | None = None,
        from_date: datetime | None = None, 
        to_date: datetime | None = None
        ):
        """
        Fetch user's expenses using filters such as category and date range.
        """
        async with session() as db:
            service = ExpenseServices(db)
            get_expenses = GetExpenses(
                limit=limit,
                offset=offset,
                category=category,
                from_date=from_date,
                to_date=to_date
            )

            res = await service.get_expenses(user_id=user_id, params=get_expenses)
            return res

    @tool
    async def add_expense(
        user_id: int,
        amount: float,
        category: ExpenseCategory,
        description: str| None,
        date: datetime
    ):
        "add user's expense"
        async with session() as db:
            service = ExpenseServices(db)
            expense = AddExpenses(
                amount=amount,
                category=category,
                description=description,
                date=date
            )
            res = await service.add_expense(expense=expense, user_id=user_id)
            return res

    @tool
    async def get_expense_summary(
        user_id: str,
        from_date: str | None,
        to_date: str | None
    ):
        "get user's expense summary"
        async with session() as db:
            service = ExpenseServices(db)

            res = await service.get_summary(
                user_id=user_id,
                from_date=from_date,
                to_date=to_date
            )

            return res




