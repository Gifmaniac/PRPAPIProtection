import os
import sys
from flask import Flask, request, jsonify

# Ensure the repo root is on sys.path so sibling packages can be imported when running
# this script from its own folder.
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from services.PRPDetectionService import detect_currency_mismatch, detect_insufficient_balance, detect_bola_attempt
from security.PRPLoggingConfig import *

app = Flask(__name__)

# Current logged in user (for demonstration purposes)
current_user_id = "1"

# Fake account database
accounts = [
    {"id": 1, "user_id": 1, "currency": "ETH", "balance": 2.5},
    {"id": 2, "user_id": 2, "currency": "BTC", "balance": 1.0},
]

# Fake product pairs
product_pairs = [
    {"id": 1, "base_currency": "ETH", "quote_currency": "EUR"},
    {"id": 2, "base_currency": "BTC", "quote_currency": "EUR"},
]

# Vulnerable endpoint for trading
@app.route('/trade/<product_pair_id>/<int:source_account_id>', methods=['POST'])
def trade(product_pair_id, source_account_id):
     data = request.get_json()
     amount = data.get("amount")

     account = next((acc for acc in accounts if acc["id"] == source_account_id), None)
     if account is None:
         return jsonify({"error": "Source account not found"}), 404 
     
     if product_pair_id not in [str(pair["id"]) for pair in product_pairs]:
         return jsonify({"error": "Product pair not found"}), 404
     
     return jsonify({"message": "Trade executed successfully", 
                     "product_pair_id": product_pair_id, 
                     "source_account_id": source_account_id,
                     "amount": amount
                     }), 200

# secure endpoint for trading
@app.route('/secure_trade/<product_pair_id>/<int:source_account_id>', methods=['POST'])
def secure_trade(product_pair_id, source_account_id):     
     data = request.get_json()
     amount = data.get("amount")

     account = next((acc for acc in accounts if acc["id"] == source_account_id), None)
     if account is None:
         return jsonify({"error": "Source account not found"}), 404 
     
     if product_pair_id not in [str(pair["id"]) for pair in product_pairs]:
         return jsonify({"error": "Product pair not found"}), 404
     
     #check the required currency for the trade based on the product pair
     required_currency = [pair["base_currency"] for pair in product_pairs if str(pair["id"]) == product_pair_id][0]

     # check if the account belongs to the current user
     if account["user_id"] != int(current_user_id):
         return jsonify({"error": "Unauthorized access to the account"}), 403
     
     # check if the account currency matches the required currency for the trade
     if account["currency"] != required_currency:
         return jsonify({"error": "Account currency does not match the required currency for the trade"}), 400
    
    # check if the account has sufficient balance for the trade
     if account["balance"] <= 0:
        return jsonify({"error": "Insufficient balance for the trade"}), 400  
     
     #trade execution logic would go here
     return jsonify({"message": "Trade executed successfully",   
                        "product_pair_id": product_pair_id, 
                        "source_account_id": source_account_id,
                        "amount": amount}), 200

@app.route('/secure_trade_logging/<product_pair_id>/<int:source_account_id>', methods=['POST'])
def secure_trade_with_Logging(product_pair_id, source_account_id):     
     data = request.get_json()
     amount = data.get("amount")

     account = next((acc for acc in accounts if acc["id"] == source_account_id), None)
     if account is None:
         return jsonify({"error": "Source account not found"}), 404 
     
     if product_pair_id not in [str(pair["id"]) for pair in product_pairs]:
         return jsonify({"error": "Product pair not found"}), 404
     
     #check the required currency for the trade based on the product pair
     required_currency = [pair["base_currency"] for pair in product_pairs if str(pair["id"]) == product_pair_id][0]

     # check if the account belongs to the current user
     if account["user_id"] != int(current_user_id):
         detect_bola_attempt(current_user_id, source_account_id, account["user_id"])
         return jsonify({"error": "Unauthorized access to the account"}), 403
     
     # check if the account currency matches the required currency for the trade
     if account["currency"] != required_currency:
         detect_currency_mismatch(account["currency"], required_currency)
         return jsonify({"error": "Account currency does not match the required currency for the trade"}), 400
    
    # check if the account has sufficient balance for the trade
     if account["balance"] <= 0:
        detect_insufficient_balance(account["balance"], amount)
        return jsonify({"error": "Insufficient balance for the trade"}), 400  
     
     #trade execution logic would go here
     return jsonify({"message": "Trade executed successfully",   
                        "product_pair_id": product_pair_id, 
                        "source_account_id": source_account_id,
                        "amount": amount}), 200


if __name__ == '__main__':    
    app.run(debug=True)