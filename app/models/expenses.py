from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseExpenses(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    date: str

class AddExpenses(BaseExpenses):
    id: int


class ExpensesResponse(BaseExpenses):
    id: int

    model_config = configDict(
        from_attributes=True
    )

class SearchExpenses(BaseModel):
    category: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None