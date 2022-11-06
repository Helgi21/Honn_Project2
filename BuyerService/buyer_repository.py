from models import BuyerModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

router = APIRouter()

class BuyerRepository:
    __BUYERS_FILE = '../persistance/buyers.json'
    def create_buyer(self, buyer: BuyerModel):
        self.__file_exists()
        with open(self.__BUYERS_FILE, 'r+') as f:
            buyers = json.load(f)
            new_buyer_id = 1
            if len(buyers) != 0:
                new_buyer_id = buyers[-1]['buyerId'] + 1
            buyer.buyerId = new_buyer_id
            buyers.append(buyer.dict())
            f.seek(0)
            f.truncate()
            f.write(json.dumps(buyers))
        return new_buyer_id
    
    def get_buyer(self, buyer_id: int):
        self.__file_exists()
        with open(self.__BUYERS_FILE, 'r') as f:
            buyers = json.load(f)
            for buyer in buyers:
                if buyer['buyerId'] == buyer_id:
                    return {
                        "name": buyer['name'],
                        "ssn": buyer['ssn'],
                        "email": buyer['email'],
                        "phoneNumber": buyer['phoneNumber']
                    }
            raise HTTPException(status_code=404, detail="Buyer does not exist")
    
    def __file_exists(self) -> None:
        try:
            open(self.__BUYERS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__BUYERS_FILE, 'w') as f:
                f.write("[]")