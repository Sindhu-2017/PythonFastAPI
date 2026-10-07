from datetime import date
from pydantic import BaseModel,Field

class IncomeCreate(BaseModel):
    income_date : date
    source :str = Field(min_length =2 ,max_length = 100)
    income_type : str = Field(min_length =2 ,max_length = 100)
    amount :float =Field(gt=0)
    tax_percentage :float =Field(ge=0)
    expense_amount : float =Field(ge =0)
    description : str | None = Field ( default = None , max_length = 255)

class IncomeUpdate(BaseModel):
    income_date : date
    source :str = Field(min_length =2 ,max_length = 100)
    income_type : str = Field(min_length =2 ,max_length = 100)
    amount :float =Field(gt=0)
    tax_percentage :float =Field(ge=0)
    expense_amount : float =Field(ge =0)
    description : str | None = Field ( default = None , max_length = 255)