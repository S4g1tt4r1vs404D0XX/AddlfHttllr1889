from flask import Flask, jsonify, request

app = Flask(__name__)

users = {}
guilds = {}
channels = {}
messages = {}

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Uncontinued script, finishing tomorrow!
