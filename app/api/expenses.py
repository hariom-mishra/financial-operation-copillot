from fastapi import APIRouter, Depends
from models.expenses import GetExpenses, ExpenseResponse
from services.expense_services import ExpenseServices
from core.db import get_db
from typing import List

router = APIRouter(prefix="/expenses", tags=["Expenses"])

#add expense
@router.post("/add")
def add_expense():
    pass

#get expense 
@router.get("/", response_model=List[ExpenseResponse])
async def get_expense(params: GetExpenses = Depends(), db = Depends(get_db)):
    service = ExpenseServices(db)
    return await service.get_expenses(params)

#spending summary
@router.get("/summary")
def spending_summary():
    pass

#search expense
@router.get("/search")
def search_expense():
    pass

#update expense
@router.put("/update/{expense_id}")
def update_expense():
    pass

#delete expense
@router.delete("/delete/{expense_id}")
def delete_expense():
    pass
