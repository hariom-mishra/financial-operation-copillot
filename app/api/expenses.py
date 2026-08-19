from fastapi import APIRouter, Depends
from models.expenses import GetExpenses, ExpenseResponse, AddExpenses, UpdateExpenses, SummaryResponse
from services.expense_services import ExpenseServices
from core.db import get_db
from typing import List, Optional
from datetime import datetime
from core.dependency import get_current_user
from core.exceptions import ExpenseException

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# ── Add expense ──────────────────────────────────────────────────────────────
@router.post("/add", response_model=ExpenseResponse)
async def add_expense(
    expense: AddExpenses,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    try:
        service = ExpenseServices(db)
        return await service.add_expense(expense=expense, user_id=current_user.id)
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))


# ── List expenses (with optional filters) ────────────────────────────────────
@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    params: GetExpenses = Depends(),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = ExpenseServices(db)
        return await service.get_expenses(current_user.id, params)
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))


# ── Search expenses by keyword ────────────────────────────────────────────────
@router.get("/search", response_model=List[ExpenseResponse])
async def search_expenses(
    keyword: str,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = ExpenseServices(db)
        return await service.search_expenses(
            user_id=current_user.id,
            keyword=keyword,
            limit=limit,
            offset=offset
        )
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))


# ── Spending summary ──────────────────────────────────────────────────────────
@router.get("/summary", response_model=SummaryResponse)
async def spending_summary(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = ExpenseServices(db)
        return await service.get_summary(
            user_id=current_user.id,
            from_date=from_date,
            to_date=to_date
        )
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))


# ── Update expense ────────────────────────────────────────────────────────────
@router.put("/update/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    data: UpdateExpenses,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = ExpenseServices(db)
        return await service.update_expense(
            expense_id=expense_id,
            user_id=current_user.id,
            data=data
        )
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))


# ── Delete expense ────────────────────────────────────────────────────────────
@router.delete("/delete/{expense_id}")
async def delete_expense(
    expense_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        service = ExpenseServices(db)
        return await service.delete_expense(
            expense_id=expense_id,
            user_id=current_user.id
        )
    except ExpenseException as e:
        raise e
    except Exception as e:
        raise ExpenseException(str(e))
