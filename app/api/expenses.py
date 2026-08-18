from fastapi import APIRouter

router = APIRouter(prefix="/expenses", tags=["Expenses"])

#add expense
@router.post("/add")
def add_expense():
    pass

#get expense 
@router.get("/")
def get_expense():
    pass

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
