from flask import Flask, jsonify, request
import random

app = Flask(__name__)

def generate_users(num_users):
    users = {}
    for i in range(1, num_users + 1):
        user_id = str(i)
        username = f"user{i}"
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        users[user_id] = {'id': user_id, 'username': username, 'ip': ip}
    return users

users = generate_users(420000000)
guilds = {}
channels = {}
messages = {}

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/guilds/<guild_id>', methods=['GET'])
def get_guild(guild_id):
    guild = guilds.get(guild_id)
    if guild:
        return jsonify(guild)
    return jsonify({'error': 'Guild not found'}), 404

@app.route('/api/channels/<channel_id>', methods=['GET'])
def get_channel(channel_id):
    channel = channels.get(channel_id)
    if channel:
        return jsonify(channel)
    return jsonify({'error', 'Channel not found'}), 404

@app.route('/api/messages/<message_id>', methods=['GET'])
def get_message(message_id):
    message = messages.get(message_id):
    if message:
        return jsonify(message)
    return jsonify({'error', 'Message not found'}), 404

@app.route('/api/users', methods=['GET'])
def search_users():
    username = request.args.get('username')
    for user in users.values():
        if user['username'] == username:
            return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
