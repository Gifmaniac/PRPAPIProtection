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
    

    
if __name__ == '__main__':
    app.run(debug=True)
