from stock_price_tracker import StockPriceTracker
import requests
import json

class StockPortfolioTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def add_stock(self, symbol, quantity, purchase_price):
        try:
            response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}")
            data = json.loads(response.text)
            current_price = float(data["Global Quote"]["05. price"])
            self.portfolio[symbol] = {
                "quantity": quantity,
                "purchase_price": purchase_price,
                "current_price": current_price
            }
            print(f"Added {symbol} to portfolio.")
        except Exception as e:
            print(f"Error adding {symbol}: {e}")

    def remove_stock(self, symbol):
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"Removed {symbol} from portfolio.")
        else:
            print(f"{symbol} not found in portfolio.")

    def track_performance(self):
        for symbol, stock in self.portfolio.items():
            try:
                response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}")
                data = json.loads(response.text)
                current_price = float(data["Global Quote"]["05. price"])
                stock["current_price"] = current_price
                gain_loss = (current_price - stock["purchase_price"]) * stock["quantity"]
                print(f"{symbol}:")
                print(f"  Quantity: {stock['quantity']}")
                print(f"  Purchase Price: ${stock['purchase_price']:.2f}")
                print(f"  Current Price: ${current_price:.2f}")
                print(f"  Gain/Loss: ${gain_loss:.2f}")
                print(f"  Percentage Change: {(gain_loss / (stock['purchase_price'] * stock['quantity'])) * 100:.2f}%")
            except Exception as e:
                print(f"Error tracking {symbol}: {e}")

def main():
    api_key = "YOUR_API_KEY"
    tracker = StockPortfolioTracker(api_key)

    while True:
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Track performance")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            purchase_price = float(input("Enter purchase price: "))
            tracker.add_stock(symbol, quantity, purchase_price)
        elif choice == "2":
            symbol = input("Enter stock symbol: ")
            tracker.remove_stock(symbol)
        elif choice == "3":
            tracker.track_performance()
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()


