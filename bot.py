import requests

class Bot:
    def __init__(self, api_url):
        self.api_url = api_url
    def get_user(self, user_id):
        response = requests.get(f"{self.api_url}/users/{user_id}")
        return response.json()
    def get_guild(self, guild_id):
        response = requests.get(f"{self.api_url}/guilds/{guild_id}")

# Uncontinued
