from pydantic import BaseModel , Field
class IncomeCreate(BaseModel):
    name : str
    basic_income : float = Field(gt=0)
    experience : int =Field (ge=0)

class IncomeResponse(BaseModel):
    id:int
    name:str
    basic_income :float
    experience :int
    hra: float
    da : float
    bonus : float
    gross_income :float
    tax :float
    net_income : float

