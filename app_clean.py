from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

# Load API key from environment variable
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
if not API_KEY:
    raise ValueError("Please set ALPHA_VANTAGE_API_KEY environment variable")

BASE_URL = "https://www.alphavantage.co/query"

class TradingSimulator:
    def __init__(self):
        self.portfolio = {}  # {symbol: quantity}
        self.balance = 10000.0  # Starting cash
        self.transaction_history = []
        self.price_cache = {}  # Cache prices to avoid repeated API calls
        
    def get_price(self, symbol: str) -> float:
        """Fetch current price from Alpha Vantage"""
        if symbol in self.price_cache:
            return self.price_cache[symbol]
        
        # Determine function based on symbol
        if symbol == "GOLD":
            params = {
                "function": "WTI",
                "apikey": API_KEY
            }
        elif symbol == "SILVER":
            params = {
                "function": "SILVER",
                "apikey": API_KEY
            }
        else:
            # Regular stock
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": API_KEY
            }
        
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            # Handle different response formats
            if "Global Quote" in data:
                price = float(data["Global Quote"].get("05. price", 0))
            elif "data" in data and len(data["data"]) > 0:
                price = float(data["data"][0].get("value", 0))
            else:
                price = 0
                
            if price > 0:
                self.price_cache[symbol] = price
            return price
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return 0
    
    def buy(self, symbol: str, quantity: int) -> Tuple[bool, str]:
        """Buy shares"""
        price = self.get_price(symbol)
        if price == 0:
            return False, f"Could not fetch price for {symbol}"
        
        cost = price * quantity
        if self.balance < cost:
            return False, f"Insufficient funds. Need ${cost:.2f}, have ${self.balance:.2f}"
        
        self.balance -= cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self.transaction_history.append({
            "type": "BUY",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total": cost,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True, f"Bought {quantity} {symbol} @ ${price:.2f} = ${cost:.2f}"
    
    def sell(self, symbol: str, quantity: int) -> Tuple[bool, str]:
        """Sell shares"""
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            held = self.portfolio.get(symbol, 0)
            return False, f"You only own {held} {symbol}"
        
        price = self.get_price(symbol)
        if price == 0:
            return False, f"Could not fetch price for {symbol}"
        
        proceeds = price * quantity
        self.balance += proceeds
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        
        self.transaction_history.append({
            "type": "SELL",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "total": proceeds,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True, f"Sold {quantity} {symbol} @ ${price:.2f} = ${proceeds:.2f}"
    
    def get_portfolio_value(self) -> float:
        """Calculate total portfolio value (holdings + cash)"""
        holdings_value = 0
        for symbol, quantity in self.portfolio.items():
            price = self.get_price(symbol)
            holdings_value += price * quantity
        return self.balance + holdings_value
    
    def get_portfolio_data(self) -> dict:
        """Get portfolio data as JSON"""
        holdings = []
        total_holdings_value = 0
        
        for symbol, quantity in self.portfolio.items():
            price = self.get_price(symbol)
            value = price * quantity
            total_holdings_value += value
            holdings.append({
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "value": value
            })
        
        return {
            "holdings": holdings,
            "cash": self.balance,
            "holdings_value": total_holdings_value,
            "total_value": self.get_portfolio_value()
        }
    
    def get_history(self) -> list:
        """Get transaction history"""
        return self.transaction_history[-20:]  # Last 20 transactions

app = Flask(__name__)
simulator = TradingSimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    return jsonify(simulator.get_portfolio_data())

@app.route('/api/price/<symbol>', methods=['GET'])
def get_price(symbol):
    price = simulator.get_price(symbol.upper())
    return jsonify({"symbol": symbol.upper(), "price": price})

@app.route('/api/buy', methods=['POST'])
def buy():
    data = request.json
    symbol = data.get('symbol', '').upper()
    quantity = int(data.get('quantity', 0))
    success, message = simulator.buy(symbol, quantity)
    return jsonify({
        "success": success,
        "message": message,
        "portfolio": simulator.get_portfolio_data()
    })

@app.route('/api/sell', methods=['POST'])
def sell():
    data = request.json
    symbol = data.get('symbol', '').upper()
    quantity = int(data.get('quantity', 0))
    success, message = simulator.sell(symbol, quantity)
    return jsonify({
        "success": success,
        "message": message,
        "portfolio": simulator.get_portfolio_data()
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({"history": simulator.get_history()})

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
