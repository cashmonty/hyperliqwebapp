from flask import Flask, jsonify, render_template
import threading
import time
import csv
from hyperliquid.info import Info

app = Flask(__name__)
info = Info(base_url="https://api.hyperliquid.xyz")

# Global dictionaries to store user state data and track changes
user_states = {}
previous_states = {}
state_changes = {}

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
    wallets = read_wallet_addresses('hyperliquiddepositors.csv')
    for wallet in wallets:
        try:
            current_state = info.user_state(wallet)
            if wallet not in previous_states or current_state != previous_states[wallet]:
                state_changes[wallet] = current_state
            previous_states[wallet] = current_state
        except Exception as e:
            state_changes[wallet] = {"error": str(e)}
        time.sleep(0.005)  # Wait for 5 milliseconds

# Run the fetching task in a separate thread
threading.Thread(target=fetch_user_states, daemon=True).start()

@app.route('/state_changes')
def get_state_changes():
    global state_changes
    changes = state_changes.copy()  # Copy the changes to send
    state_changes.clear()  # Clear the changes after sending
    return jsonify(changes)
@app.route('/')
def index():
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
