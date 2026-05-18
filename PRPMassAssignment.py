from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Jhon", "email": "jhon@example.com", "balance": 1000.0},
]

# Vulnerable endpoint for updating user information
@app.route('/user/vulnerable_update/<int:user_id>', methods=['POST'])
def update_user_email(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.update(request.json)
    return jsonify({"message": "User updated successfully",
                    "updated_user": user}), 200


# Secure endpoint for updating user information
@app.route('/user/secure_update/<int:user_id>', methods=['POST'])
def secure_update_user_email(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Only allow updating the email field
    if "email" in request.json:
        user["email"] = request.json["email"]
        return jsonify({"message": "User email updated successfully",
                        "updated_user": user}), 200
    else:
        return jsonify({"error": "Only email field can be updated",
                        "updated_user": user}), 400


if __name__ == '__main__':
    app.run(debug=True) 