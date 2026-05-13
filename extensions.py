import requests
import json


class APIException(Exception):
    """Кастомное исключение для ошибок пользователя"""
    pass


class CurrencyConverter:
    """Класс для конвертации валют"""
    
    CURRENCIES = {
        "евро": "EUR",
        "доллар": "USD",
        "рубль": "RUB"
    }
    
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        """
        Возвращает сумму в целевой валюте.
        
        :param base: валюта, цену которой узнаём
        :param quote: валюта, в которой узнаём цену
        :param amount: количество
        :return: конвертированная сумма
        :raises APIException: при ошибках ввода или запроса
        """
        base = base.lower()
        quote = quote.lower()
        
        if base == quote:
            raise APIException("Нельзя переводить одинаковые валюты.")
        
        try:
            base_ticker = CurrencyConverter.CURRENCIES[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту «{base}»")
        
        try:
            quote_ticker = CurrencyConverter.CURRENCIES[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту «{quote}»")
        
        try:
            amount_value = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество «{amount}»")
        
        # Запрос к API
        url = f"https://api.exchangerate-api.com/v4/latest/{base_ticker}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = json.loads(response.text)
            rate = data["rates"][quote_ticker]
            total = rate * amount_value
            return round(total, 2)
        except KeyError:
            raise APIException("Ошибка при получении курса валют")
        except requests.RequestException:
            raise APIException("Ошибка соединения с сервисом курсов валют")