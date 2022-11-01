from pydantic import BaseModel


class CardModel(BaseModel): 
    cardNumber: int
    expirationMonth: int
    expirationYear: int
    cvc: int

class OrderModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    discount: float
    creditCard: CardModel
