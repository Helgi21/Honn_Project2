from models import ProductModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

class ProductRepository:
    __PRODUCTS_FILE = "../persistance/products.json"

    def create_product(self, product: ProductModel):
        self.__validate()
        self.__file_exists()
        with open(self.__PRODUCTS_FILE, "r+") as f:
            products = json.load(f)
            
            new_product_id = 0
            if len(products) == 0:
                new_product_id = products[-1]["id"] + 1

            product["id"] = new_product_id
            products.append(product)

            f.seek(0)
            f.truncate()

            f.write(json.dumps(products))
        return new_product_id


    def get_product(self, id: int):
        self.__file_exists()
        response = None

        with open(self.__PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
            for product in products:
                if product["id"] == id:
                    return {
                        "id": product.id,
                        "merchantId": product.merchant_id,
                        "productName": product.product_name,
                        "price": product.price,
                        "quantity": product.quantity
                    }

            raise HTTPException(status_code=404, detail="Product not found")

    def __file_exists(self) -> None:
        try:
            open(self.__PRODUCTS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__PRODUCTS_FILE, 'w') as f:
                f.write("[]")