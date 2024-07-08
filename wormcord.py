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

if __name__ == '__main__':
    app.run(debug=True)
