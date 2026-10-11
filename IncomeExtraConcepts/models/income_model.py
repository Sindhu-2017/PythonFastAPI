from dataclasses import dataclass
from datetime import date

@dataclass
class IncomeModel:
    income_id:int
    income_date :date
    source : str
    income_type : str
    amount : float
    tax_percentage : float
    tax_amount :float
    expense_amount : float
    net_income : float
    cash_in_hand : float
    description : str | None