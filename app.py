from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilita CORS para evitar bloqueios no frontend

# API Keys
TIINGO_TOKEN = "26d22c5ff18d0d9308bf9b7532627c3547eee407"
EXCHANGE_RATE_API_KEY = "9ac8f4e4a4ea29455558a681"

def get_stock_price(ticker):
    """Obtém o preço de fechamento da ação pela API Tiingo."""
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={TIINGO_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return {"close": data[0]["close"]}
        return {"error": f"Dados não encontrados para {ticker}"}
    return {"error": f"Erro ao buscar {ticker}: {response.status_code}"}

def get_usd_brl():
    """Obtém a cotação do USD/BRL da Exchangerate-API."""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "conversion_rates" in data and "BRL" in data["conversion_rates"]:
            return {"USD/BRL": round(data["conversion_rates"]["BRL"], 2)}
        return {"error": "Taxa de câmbio BRL não encontrada."}
    return {"error": f"Erro ao buscar USD/BRL: {response.status_code}"}

@app.route('/api/market', methods=['GET'])
def get_market_data():
    """Retorna os preços das ações e a cotação do dólar."""
    stocks = {
        "Apple (AAPL)": get_stock_price("AAPL"),
        "Nvidia (NVDA)": get_stock_price("NVDA"),
        "Petrobras (PETR4.SA)": get_stock_price("PETR4.SA"),
        "Vale (VALE3.SA)": get_stock_price("VALE3.SA"),
        "USD/BRL": get_usd_brl()
    }
    return jsonify(stocks)

if __name__ == '__main__':
    app.run(debug=True)
