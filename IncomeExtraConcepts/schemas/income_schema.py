from datetime import date
from decimal import Decimal
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict
)

class IncomeCreate(BaseModel):
    income_date : date
    source :str = Field(min_length =2 ,max_length = 100)
    income_type : str = Field(min_length =2 ,max_length = 100)
    amount :Decimal =Field(gt=0)
    tax_percentage :Decimal =Field(ge=0)
    description : str | None = Field ( default = None , max_length = 255)

    @field_validator("source")
    @classmethod
    def validate_source(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("Income source cannot contain numbers")

        return value.strip()

   

class IncomeUpdate(BaseModel):
    income_date : date
    source :str = Field(min_length =2 ,max_length = 100)
    income_type : str = Field(min_length =2 ,max_length = 100)
    amount :Decimal =Field(gt=0)
    tax_percentage :Decimal =Field(ge=0)
    description : str | None = Field ( default = None , max_length = 255)



class IncomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class IncomeActionResponse(BaseModel):
    message: str
    income_id: int

class IncomePatch(BaseModel):
    income_date: date | None = None
    source: str | None = Field(default=None,min_length=2,max_length=100)
    income_type: str | None = Field(default=None,min_length=2,max_length=100)
    amount: Decimal | None = Field(default=None,gt=0)
    tax_percentage: Decimal | None = Field(default=None,ge=0,le=100)
    description: str | None = Field(default=None,max_length=255)

class IncomePagination(BaseModel):
    total_records : int
    page_size :int
    offset : int
    total_pages :int
    page_number :int
    has_previous : bool
    has_next :bool

class IncomePaginatedResponse(BaseModel):
    records : list[IncomeResponse]
    pagination : IncomePagination

class ExpenseCreate(BaseModel):
    expense_name: str = Field(min_length=2, max_length=100)
    amount: Decimal = Field(gt=0)
    description: str | None = None


class ExpenseAttachmentResponse(BaseModel):
    attachment_id: int
    expense_id: int
    file_name: str
    file_path: str

class ExpenseResponse(BaseModel):
    expense_id: int
    expense_name: str
    amount: Decimal
    description: str | None = None

    attachments: list[ExpenseAttachmentResponse] = Field(
        default_factory=list
    )


class IncomeWithExpensesResponse(IncomeResponse):
    expenses: list[ExpenseResponse] = Field(default_factory=list)