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
    amount :float =Field(gt=0)
    tax_percentage :float =Field(ge=0)
    expense_amount : float =Field(ge =0)
    description : str | None = Field ( default = None , max_length = 255)

    @field_validator("source")
    @classmethod
    def validate_source(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError("Income source cannot contain numbers")

        return value.strip()

    @model_validator(mode="after")
    def validate_income(self):

        if self.expense_amount > 0 and not self.description:
            raise ValueError(
                "Description is required when expense amount is greater than 0"
            )

        return self
    

class IncomeUpdate(BaseModel):
    income_date : date
    source :str = Field(min_length =2 ,max_length = 100)
    income_type : str = Field(min_length =2 ,max_length = 100)
    amount :float =Field(gt=0)
    tax_percentage :float =Field(ge=0)
    expense_amount : float =Field(ge =0)
    description : str | None = Field ( default = None , max_length = 255)


class IncomeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    income_date: date
    source: str
    income_type: str
    amount: float
    tax_percentage: float
    tax_amount: float
    expense_amount: float
    net_income: float
    cash_in_hand: float
    description: str | None

class IncomePatch(BaseModel):

    income_date: date | None = None

    source: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    income_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    tax_percentage: Decimal | None = Field(
        default=None,
        ge=0,
        le=100
    )

    expense_amount: Decimal | None = Field(
        default=None,
        ge=0
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )