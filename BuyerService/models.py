from pydantic import BaseModel
from typing import Optional

class BuyerModel(BaseModel):
    buyerId: Optional[int]
    name: str
    ssn: str
    email: str
    phoneNumber: str