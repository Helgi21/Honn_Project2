from pydantic import BaseModel
from typing import Optional

class MerchantModel(BaseModel):
    merchantId: Optional[int]
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool