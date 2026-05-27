import os
import sys
import flask
from flask import Flask, request, jsonify
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
from services.PRPDetectionService import detect_ban_user, detect_excessive_access
from security.PRPLoggingConfig import *

app = Flask(__name__)

users = [
    {
        "id": 1,
        "Role": "Super Admin",
        "permissions": ["DELETE_ACCOUNT", "VIEW_USERS"]
    },
    {
        "id": 2,
        "Role": "Support Admin",
        "permissions": ["VIEW_USERS", "VIEW_USERS_MESSAGE", "TEMP_BAN_USER", "DELETE_ACCOUNT"]
    }
]

current_user_id = 2

# Vulnerable endpoint for deleting a user
@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    current_user = next(
        (u for u in users if u["id"] == current_user_id),
        None
    )

    required_permission = "DELETE_ACCOUNT"

    if detect_excessive_access(current_user["id"], current_user["permissions"], required_permission, request.path) :

        return jsonify({
            "error": "Access denied"
        }), 403
    
    detect_ban_user(current_user["id"], request.path, user_id)
    return jsonify({
        "message": f"User {user_id} deleted successfully"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
