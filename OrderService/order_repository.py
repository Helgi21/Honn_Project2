from models import OrderModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

router = APIRouter()

class OrderRepository:
    __ORDERS_FILE = "../persistance/orders.json"
    
    def create_order(self, order: OrderModel):
        self.__validate()
        with open(self.__ORDERS_FILE, 'r+') as f:
            orders = json.load(f)
            # create order id
            if len(orders) == 0:
                new_order_id = 1
            else:
                new_order_id = orders[-1]['id'] + 1

            # set order id
            order['order_id'] = new_order_id
            orders.append(order)
            # clear file to overwrite (does not do it automatically as the file is opened with 'r+' instead of 'w')
            f.seek(0)
            f.truncate()

            f.write(json.dumps(orders))
        return new_order_id

    def get_order(self, id: int):
        self.__file_exists()
        response = None
        
        with open(self.__ORDERS_FILE, "r") as f:
            #Check if order exists, then return it with total price and only the last 4 digits of the credit card
            orders = json.load(f)
            for order in orders:
                if order["id"] == id: 
                    inventory_response = requests.get(f'/inventory/{order.product_id}')   
                    procuct_price = inventory_response.json()['price']             
                    response = {
                        'id': order['id'],
                        'merchant_id': order.merchant_id,
                        'buyer_id': order.buyer_id,
                        'card_number': order.card_number.replace(order.card_number[0:12], "************"),
                        'total_price': procuct_price * (1 - order.discount)
                    }
                    break
            if response is None:
                raise HTTPException(status_code=404, detail="Order does not exist")
            else:
                return response

    def __validate(self, order: OrderModel):
        # Check if merchant exists, carry on if it does/ 400 if not with "Merchant does not exist" message
        merch_resp = requests.get(f'/merchants/{order.merchant_id}')
        if merch_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Merchant does not exist")+

        # Check if merchant allows discount
        if merch_resp.json()['allows_discount'] == False and order.discount > 0:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")
        
        # Check if buyer exists, carry on if it does/ 400 if not with "Buyer does not exist" message
        buyer_resp = requests.get(f'/buyers/{order.buyer_id}')
        if buyer_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        
        # Check if product exists, carry on if it does/ 400 if not with "Product does not exist" message
        product_resp = requests.get(f'/products/{order.product_id}')
        if product_resp.status_code == 404:
            raise HTTPException(status_code=400, detail="Product does not exist")
        
        # check if product in stock
        inventory_resp = requests.get(f'/inventory/{order.product_id}')
        if inventory_resp.json()['quantity'] == 0:
            raise HTTPException(status_code=400, detail="Product is out of stock")
        
        # Tcheck if product belongs to merchant
        if inventory_resp.json()['merchant_id'] != order.merchant_id:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")
            
        # if discount is not 0 or null, check if merchant allows discounts
        if order.discount != 0 or order.discount != None and merch_resp.json()['allowsDiscount'] == False:
            raise HTTPException(status_code=400, detail="Merchant does not allow discounts")

    def __file_exists(self) -> None:
        try:
            open(self.__ORDERS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__ORDERS_FILE, 'w') as f:
                f.write("[]")
