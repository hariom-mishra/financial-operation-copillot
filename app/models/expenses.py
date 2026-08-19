from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class BaseExpenses(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime

class AddExpenses(BaseExpenses):
    pass

class UpdateExpenses(BaseModel):
    """All fields optional — only provided fields will be updated."""
    amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class ExpenseResponse(BaseExpenses):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class GetExpenses(BaseModel):
    category: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class SearchExpenses(BaseModel):
    keyword: str

class CategorySummary(BaseModel):
    category: str
    total: float
    count: int

class SummaryResponse(BaseModel):
    total_spent: float
    expense_count: int
    by_category: List[CategorySummary]
