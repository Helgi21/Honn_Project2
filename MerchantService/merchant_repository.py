from models import MerchantModel
from fastapi import APIRouter, Depends, HTTPException
import json
import requests

router = APIRouter()

class MerchantRepository:
    __MERCHANTS_FILE = "../persistance/merchants.json"
    
    def create_merchant(self, merchant: MerchantModel) -> int:
        self.__file_exists()

        with open(self.__MERCHANTS_FILE, 'r+') as f:
            merchants = json.load(f)
            new_merchant_id = 1
            if len(merchants) != 0:
                new_merchant_id = merchants[-1]['merchantId'] + 1
            merchant.merchantId = new_merchant_id
            merchants.append(merchant.dict())
            f.seek(0)
            f.truncate()
            f.write(json.dumps(merchants))
        return new_merchant_id
    
    def get_merchant(self, merchant_id: int) -> MerchantModel:
        self.__file_exists()

        with open(self.__MERCHANTS_FILE, 'r') as f:
            merchants = json.load(f)
            for merchant in merchants:
                if merchant['merchantId'] == merchant_id:
                    return {
                                "name": merchant['name'],
                                "ssn": merchant['ssn'],
                                "email": merchant['email'],
                                "phoneNumber": merchant['phoneNumber'],
                                "allowsDiscount": merchant['allowsDiscount']
                            }
        raise HTTPException(status_code=404, detail="Merchant not found")
            
    def __file_exists(self) -> None:
        try:
            open(self.__MERCHANTS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__MERCHANTS_FILE, 'w') as f:
                f.write("[]")