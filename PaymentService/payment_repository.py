from fastapi import APIRouter, Depends, HTTPException
import json
import requests

class PaymentRepository:
    __PAYMENTS_FILE = "../persistance/orders.json"

    def __file_exists(self) -> None:
        try:
            open(self.__PAYMENTS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__PAYMENTS_FILE, 'w') as f:
                f.write("[]")