from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field

class IncomeCreate(BaseModel):

    income_date: date
    source: str = Field(min_length=2, max_length=100)
    income_type: str = Field(min_length=2, max_length=50)
    amount: Decimal = Field(gt=0)
    tax_percentage: Decimal = Field(default=Decimal("0"),ge=0,le=100)
    expense_amount: Decimal = Field(default=Decimal("0"),ge=0)
    description: str | None = None

class IncomeUpdate(BaseModel):
    income_date: date
    source: str = Field(min_length=2, max_length=100)
    income_type: str = Field(min_length=2, max_length=50)
    amount: Decimal = Field(gt=0)
    tax_percentage: Decimal = Field(default=Decimal("0"),ge=0,le=100)
    expense_amount: Decimal = Field(default=Decimal("0"),ge=0)
    description: str | None = None


class IncomeResponse(BaseModel):
    income_id: int
    income_date: date
    source: str
    income_type: str
    amount: Decimal
    tax_percentage: Decimal
    tax_amount: Decimal
    expense_amount: Decimal
    net_income: Decimal
    cash_in_hand: Decimal
    description: str | None = None


class IncomeSummary(BaseModel):
    total_income: Decimal
    total_tax: Decimal
    total_expenses: Decimal
    total_net_income: Decimal
    total_cash_in_hand: Decimal