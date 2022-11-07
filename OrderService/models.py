from pydantic import BaseModel
from typing import Optional, Union


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
    discount: Union[float,None]
    creditCard: CardModel
