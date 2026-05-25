import sys
import os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
from services.PRPDetectionService import detect_brute_force_attempt_login, detect_brute_force_attempt_login_locked, detect_repeated_brute_force_attempt_login
from security.PRPLoggingConfig import *
from flask import Flask, request, jsonify


app = Flask(__name__)

users = [
    {"email": "admin@test.com", "password": "admin123"}
]

# Vulnerable endpoint for login
@app.route('/vulnarable/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
    
    
# Secure endpoint for login
@app.route('/secure/login', methods=['POST'])
def secure_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = next((u for u in users if u["email"] == email), None)
    if user and user["password"] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

failed_login_attempts = {}

# Secure endpoint for login with logging
@app.route('/secure_with_logging/login', methods=['POST'])
def secure_login_with_logging():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    ip_address = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    endpoint = request.path

    user = next((u for u in users if u["email"] == email), None)
    if user and user["password"] == password:
        return jsonify({"message": "Login successful"}), 200
    
    failed_login_attempts[email] = ( failed_login_attempts.get(email, 0) + 1 )
    
    if failed_login_attempts.get(email, 0) >= 3:
        detect_repeated_brute_force_attempt_login(email, endpoint, ip_address, user_agent, failed_login_attempts[email])
    else:
        detect_brute_force_attempt_login(email, endpoint, ip_address, user_agent, failed_login_attempts[email])
        return jsonify({"error": "Invalid email or password"}), 401    
    
    if failed_login_attempts[email] >= 5:
        detect_brute_force_attempt_login_locked(email)
        return jsonify({"error": "Account temporarily locked"}), 403

if __name__ == '__main__':
    app.run(debug=True)
