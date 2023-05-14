import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
if API_KEY is None:
    raise ValueError("API_KEY нет в .env файле")
CRYPTO_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMS = {
    'start': 1,
    'limit': 100,
    'convert': 'USD'
}
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def get_cryptocurrencies():
    try:
        response = requests.get(CRYPTO_URL, headers=HEADERS, params=PARAMS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error fetching data from API: {err}")
        return []
    data = json.loads(response.text)['data']
    result = []
    for currency in data:
        result.append({
            'name': currency['name'],
            'symbol': currency['symbol'],
            'price': currency['quote']['USD']['price'],
            'market_cap': currency['quote']['USD']['market_cap']
        })
    return result

def search_cryptocurrency(data, search_name):
    search_name = search_name.lower()
    for currency in data:
        if search_name == currency['name'].lower():
            return currency
    return None

def print_currency(currency):
    print(f"\n\t{currency['name']} ({currency['symbol']})")
    print(f"Цена:\t\t${currency['price']}")
    print(f"Рын.капит-ция:\t{currency['market_cap']}")
    print("\n*************************************")

def print_all_currencies(data):
    for currency in data:
        print_currency(currency)

def main():
    data = get_cryptocurrencies()
    while True:
        search = input("\n<название криптовалюты> | <all> | <exit> : ")
        if search == "exit":
            break
        elif search == "all":
            print("\n*****************************************")
            print_all_currencies(data)
        else:
            result = search_cryptocurrency(data, search)
            if result:
                print("\n*****************************************")
                print_currency(result)
            else:
                print("Криптовалюта не найдена.")

if __name__ == '__main__':
    main()

