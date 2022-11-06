from models import OrderModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

router = APIRouter()

class OrderRepository:
    __ORDERS_FILE = "../persistance/orders.json"
    
    def create_order(self, order: OrderModel):
        if order.discount == None:
            order.discount = 0
        self.__validate(order)
        self.__file_exists()
        with open(self.__ORDERS_FILE, 'r+') as f:
            orders = json.load(f)
            # create order id
            new_order_id = 0
            if len(orders) != 0:
                new_order_id = orders[-1]['orderId'] + 1

            # set order id
            order.orderId = new_order_id
            order.creditCard.cardNumber = order.creditCard.cardNumber.replace(
                order.creditCard.cardNumber[0:12], "************"
            )
            orders.append(order.dict())
            # clear file to overwrite (does not do it automatically as the file is opened with 'r+' instead of 'w')
            f.seek(0)
            f.truncate()
            f.write(json.dumps(orders))
        return new_order_id

    def get_order(self, id: int):
        self.__file_exists()
        
        with open(self.__ORDERS_FILE, "r") as f:
            #Check if order exists, then return it with total price and only the last 4 digits of the credit card
            orders = json.load(f)
            print(orders)
            for order in orders:
                if order["orderId"] == id: 
                    prod_response = requests.get(f'http://localhost:8004/products/{order["productId"]}')  
                    procuct_price = prod_response.json()['price']             
                    return {
                        'productId': order['productId'],
                        'merchantId': order['merchantId'],
                        'buyerId': order['buyerId'],
                        'cardNumber': order['creditCard']['cardNumber'],
                        'totalPrice': round(procuct_price * (1 - order['discount']), 2)
                    }
            raise HTTPException(status_code=404, detail="Order does not exist")

    def __validate(self, order: OrderModel):
        # Check if merchant exists, carry on if it does/ 400 if not with "Merchant does not exist" message
        merch_resp = requests.get(f'http://localhost:8001/merchants/{order.merchantId}')
        if merch_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Merchant does not exist")

        # Check if merchant allows discount
        if merch_resp.json()['allowsDiscount'] == False and order.discount > 0:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")
        
        # Check if buyer exists, carry on if it does/ 400 if not with "Buyer does not exist" message
        buyer_resp = requests.get(f'http://localhost:8002/buyers/{order.buyerId}')
        if buyer_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        
        # Check if product exists, carry on if it does/ 400 if not with "Product does not exist" message
        product_resp = requests.get(f'http://localhost:8004/products/{order.productId}')
        if product_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Product does not exist")
        
        if (product_resp.json()['quantity'] - product_resp.json()['reserved']) < 1:
            raise HTTPException(status_code=400, detail="Product is out of stock")
        
        # check if product belongs to merchant
        if product_resp.json()['merchantId'] != order.merchantId:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

    def __file_exists(self) -> None:
        try:
            open(self.__ORDERS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__ORDERS_FILE, 'w') as f:
                f.write("[]")
