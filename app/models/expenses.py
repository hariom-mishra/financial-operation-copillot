from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class BaseExpenses(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: str

class AddExpenses(BaseExpenses):
    pass


class ExpenseResponse(BaseExpenses):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class GetExpenses(BaseModel):
    category: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class SearchExpenses(BaseModel):
    keyword: str

