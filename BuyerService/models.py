from pydantic import BaseModel

class BuyerModel(BaseModel):
    name: str
    ssn: int
    email: str
    phone: str