import json
from models import ProductModel
class ProductRepository:
    __PRODUCTS_FILE = "../persistance/products.json"

    def create_product(self, product: ProductModel):
        self.__file_exists()
        with open(self.__PRODUCTS_FILE, 'r+') as f:
            products = json.load(f)
            new_product_id = 1
            if len(products) != 0:
                new_product_id = products[-1]['productId'] + 1
            product.productId = new_product_id
            product.reserved = 0
            products.append(product.dict())
            f.seek(0)
            f.truncate()
            f.write(json.dumps(products))
        return new_product_id

    def get_product(self, product_id: int):
        self.__file_exists()
        with open(self.__PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
            for product in products:
                if product['productId'] == product_id:
                    # Excluding ProductId
                    return {
                        "merchantId": product['merchantId'],
                        "productName": product['productName'],
                        "price": product['price'],
                        "quantity": product['quantity'],
                        "reserved": product['reserved']
                    }
            return None
    
    def __file_exists(self) -> None:
        try:
            open(self.__PRODUCTS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__PRODUCTS_FILE, 'w') as f:
                f.write("[]")