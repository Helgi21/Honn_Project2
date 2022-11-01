from pydantic import BaseModel

class MerchantModel(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool