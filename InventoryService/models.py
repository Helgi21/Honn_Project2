from pydantic import BaseModel
from typing import Optional


class ProductModel(BaseModel):
    productId: Optional[int] # Not received when creating but used after that
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0 # Default value