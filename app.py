from flask import Flask, jsonify
import yfinance as yf
import requests

app = Flask(__name__)

def get_usd_brl():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return data['USDBRL']['bid']

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    return hist['Close'].iloc[-1]

@app.route('/cotacoes', methods=['GET'])
def get_quotes():
    usd_brl = get_usd_brl()
    nvidia_price = get_stock_price("NVDA")
    apple_price = get_stock_price("AAPL")
    petr4_price = get_stock_price("PETR4.SA")
    vale3_price = get_stock_price("VALE3.SA")

    quotes = {
        "USD-BRL": usd_brl,
        "NVDA": nvidia_price,
        "AAPL": apple_price,
        "PETR4": petr4_price,
        "VALE3": vale3_price
    }

    return jsonify(quotes)

if __name__ == '__main__':
    app.run(debug=True)