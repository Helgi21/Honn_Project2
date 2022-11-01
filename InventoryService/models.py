from pydantic import BaseModel

class InventoryModel(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int