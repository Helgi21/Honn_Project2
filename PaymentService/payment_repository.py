import json

class PaymentRepository:
    __PAYMENTS_FILE = "../persistance/payments.json"

    def create_payment(self, id: int, valid_bolean: bool):
        self.__file_exists()
        with open(self.__PAYMENTS_FILE, 'r+') as f:
            payments = json.load(f)

            payment = {'order_id': id, 'payment_result': valid_bolean}
            payments.append(payment)

            f.seek(0)
            f.truncate()
            f.write(json.dumps(payments))

    def __file_exists(self) -> None:
        try:
            open(self.__PAYMENTS_FILE, "r").close()
        except FileNotFoundError:
            # Creates a new file
            with open(self.__PAYMENTS_FILE, 'w') as f:
                f.write("[]")