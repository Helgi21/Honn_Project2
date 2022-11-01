from models import OrderModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

router = APIRouter()

class BuyerRepository:
    
    def create_buyer(self, buyer):
        pass
    
    def get_buyer(self, buyer_id):
        pass
    
    def __file_exists(self) -> None:
        try:
            open(self.__ORDERS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__ORDERS_FILE, 'w') as f:
                f.write("[]")