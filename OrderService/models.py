from pydantic import BaseModel
from typing import Optional


class CardModel(BaseModel): 
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int

class OrderModel(BaseModel):
    orderId: Optional[int]
    productId: int
    merchantId: int
    buyerId: int
    discount: float|None
    creditCard: CardModel
