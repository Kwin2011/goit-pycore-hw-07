import requests

@staticmethod
def get_exchange_rates():

    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        rates = ""
        for item in data:
            ccy = item["ccy"]
            buy = item["buy"]
            sale = item["sale"]
            rates += f"{ccy}: Buy = {buy}, Sale = {sale}\n"
        
        return rates if rates else "No exchange rate data available."
    except requests.RequestException as e:
        return f"Error retrieving exchange rates: {e}"
