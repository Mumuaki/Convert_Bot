import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        API_KEY = "9ab469bab9053a8de34a5186"  # ← вставь свой API-ключ
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base.upper()}"

        try:
            response = requests.get(url)
            data = response.json()
        except Exception as e:
            raise APIException(f"Ошибка при запросе к API: {str(e)}")

        if 'conversion_rates' not in data:
            raise APIException("Некорректный ответ от сервера API")

        rates = data['conversion_rates']

        if quote.upper() not in rates:
            raise APIException(f"Валюта {quote} не поддерживается API")

        rate = rates[quote.upper()]
        converted = amount * rate
        return converted
