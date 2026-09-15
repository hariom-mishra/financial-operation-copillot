from langchain_core.tools import tool
from services.expense_services import ExpenseServices
from core.db import session
from models.expenses import GetExpenses, AddExpenses, ExpenseCategory
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


class ExpenseToolkit:
    @tool
    async def get_expenses( 
        user_id: int,
        limit: int = 10, 
        offset: int = 0,
        category: Optional[ExpenseCategory] = None,
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch user's expenses with optional filters such as category and date range.
        Dates should be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).
        """
        async with session() as db:
            service = ExpenseServices(db)
            parsed_from = datetime.fromisoformat(from_date) if from_date else None
            parsed_to = datetime.fromisoformat(to_date) if to_date else None
            get_expenses_params = GetExpenses(
                limit=limit,
                offset=offset,
                category=category,
                from_date=parsed_from,
                to_date=parsed_to
            )

            res = await service.get_expenses(user_id=int(user_id), params=get_expenses_params)
            return [
                {
                    "id": exp.id,
                    "amount": exp.amount,
                    "category": exp.category,
                    "description": exp.description,
                    "date": exp.date.isoformat() if hasattr(exp.date, "isoformat") else str(exp.date),
                }
                for exp in res
            ]

    @tool
    async def add_expense(
        user_id: int,
        amount: float,
        category: ExpenseCategory,
        description: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a user's expense.
        Category must be one of: Food, Transportation, Housing, Utilities, Entertainment, Health, Shopping, Others.
        Date is optional (defaults to current date and time).
        """
        async with session() as db:
            service = ExpenseServices(db)
            parsed_date = datetime.fromisoformat(date) if date else datetime.now(timezone.utc)
            expense = AddExpenses(
                amount=amount,
                category=category,
                description=description,
                date=parsed_date
            )
            res = await service.add_expense(expense=expense, user_id=int(user_id))
            return {
                "id": res.id,
                "amount": res.amount,
                "category": res.category,
                "description": res.description,
                "date": res.date.isoformat() if hasattr(res.date, "isoformat") else str(res.date),
                "status": "success"
            }

    @tool
    async def get_expense_summary(
        user_id: int,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user's expense spending summary (total spent, count, and category breakdown).
        Dates are optional.
        """
        async with session() as db:
            service = ExpenseServices(db)

            res = await service.get_summary(
                user_id=int(user_id),
                from_date=from_date,
                to_date=to_date
            )

            return res




