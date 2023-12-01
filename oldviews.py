from flask import Flask, jsonify
import threading
import time
import csv
from hyperliquid.info import Info
from hyperliquid.utils import constants

app = Flask(__name__)
info = Info(base_url="https://api.hyperliquid.xyz")

# Global dictionary to store user state data
user_states = {}

def read_wallet_addresses(csv_file):
    wallets = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if your CSV has one
        for row in reader:
            wallet_address = row[0]
            wallets.append(wallet_address)
    return wallets

def fetch_user_states():
    wallets = read_wallet_addresses('hyperliquidleaders.csv')
    for wallet in wallets:
        try:
            user_state_data = info.user_state(wallet)
            user_states[wallet] = user_state_data
        except Exception as e:
            user_states[wallet] = {"error": str(e)}
        time.sleep(0.005)  # Wait for 5 milliseconds

# Run the fetching task in a separate thread
threading.Thread(target=fetch_user_states, daemon=True).start()

@app.route('/user_states')
def get_user_states():
    return jsonify(user_states)

if __name__ == '__main__':
    app.run(debug=True)
