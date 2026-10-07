from datetime import date
from pydantic import BaseModel, Field

class IncomeCreate(BaseModel):

    income_date: date
    source: str = Field(min_length=2, max_length=100)
    income_type: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0)
    tax_percentage: float = Field(default=0, ge=0, le=100)
    expense_amount: float = Field(default=0, ge=0)
    description: str | None = None

class IncomeUpdate(BaseModel):

    income_date: date
    source: str = Field(min_length=2, max_length=100)
    income_type: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0)
    tax_percentage: float = Field(default=0, ge=0, le=100)
    expense_amount: float = Field(default=0, ge=0)
    description: str | None = None