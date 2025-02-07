API_KEY = "9ac8f4e4a4ea29455558a681"
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Token da API Tiingo
TIINGO_TOKEN = "26d22c5ff18d0d9308bf9b7532627c3547eee407"

def get_stock_price(ticker):
    """Obtém o preço de fechamento da ação a partir da API Tiingo."""
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={TIINGO_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data[0] if data else {"error": f"Dados não encontrados para {ticker}"}
    else:
        return {"error": f"Erro ao buscar {ticker}: {response.status_code}"}

def get_usd_brl():
    """Obtém a cotação do USD/BRL usando o exchangerate-api."""
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "conversion_rates" in data:
        return {"USD/BRL": data["conversion_rates"]["BRL"]}
    else:
        return {"error": "Erro ao obter cotação do USD/BRL"}

@app.route('/api/market', methods=['GET'])
def get_market_data():
    """Retorna os preços das ações e a cotação do dólar."""
    stocks = {
        "Apple (AAPL)": get_stock_price("AAPL"),
        "Nvidia (NVDA)": get_stock_price("NVDA"),
        "Petrobras (PBR)": get_stock_price("PBR"),
        "USD/BRL": get_usd_brl()
    }
    return jsonify(stocks)

if __name__ == '__main__':
    app.run(debug=True)
