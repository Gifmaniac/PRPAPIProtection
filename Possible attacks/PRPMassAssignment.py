import sys
import os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
from flask import Flask, request, jsonify
from services.PRPDetectionService import detect_mass_assignment_attempt, detect_repeated_mass_assignment_attempt
from security.PRPLoggingConfig import *
    
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

failed_attempts = {}

# Secure endpoint for updating user information with logging
@app.route('/user/secure_update_with_logging/<int:user_id>', methods=['POST'])
def secure_update_user_email_with_logging(user_id):
    requested_fields = list(request.json.keys())

    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if requested_fields != ["email"]:
        failed_attempts[user_id] = failed_attempts.get(user_id, 0) + 1
        
        # Check if this is a repeated attack (3+ attempts)
        if failed_attempts.get(user_id, 0) >= 3:
            detect_repeated_mass_assignment_attempt(user_id, requested_fields, ["email"], failed_attempts[user_id])
        else:
            detect_mass_assignment_attempt(user_id, requested_fields, "email")
        
        return jsonify({"error": "Only email field can be updated",
                            "updated_user": user}), 400
    
    if "email" in request.json:
        user["email"] = request.json["email"]
        return jsonify({"message": "User email updated successfully",
                        "updated_user": user}), 200
    
if __name__ == '__main__':
    app.run(debug=True) 