import requests
import json


class APIException(Exception):
    def __init__(self, message):
        self.message = message


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{base}'
            response = requests.get(url)
            data = json.loads(response.text)

            if 'rates' in data and quote in data['rates']:
                rate = data['rates'][quote]
                converted_amount = amount * rate
                return converted_amount
            else:
                raise APIException(f"Currency '{quote}' is not supported.")
        except Exception as e:
            raise APIException(f"Error fetching data from the API: {str(e)}")


# Example of usage
try:
    base_currency = "USD"
    quote_currency = "EUR"
    amount = 100
    converted_amount = CurrencyConverter.get_price(base_currency, quote_currency, amount)
    print(f"{amount:.2f} {base_currency} = {converted_amount:.2f} {quote_currency}")
except APIException as e:
    print(f"Error: {e.message}")
