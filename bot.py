import requests
from events import events

class Bot:
    def __init__(self, api_url):
        self.api_url = api_url
        self.events = events()

    def event(self, func):
        return self.events.event(func)

    async def ready(self):
        await self.events.emit('on_ready')

    async def message(self, message):
        await self.events.emit('on_message', message)

    async def member_join(self, member):
        await self.events.emit('on_member_join', member)

    async def member_leave(self, member):
        await self.events.emit('on_member_leave', member)

    async def get_user(self, user_id):
        response = requests.get(f"{self.api_url}/api/users/{user_id}")
        user = response.json()
        await self.events.emit('on_user_fetched', user)
        return user

    async def get_guild(self, guild_id):
        response = requests.get(f"{self.api_url}/api/guilds/{guild_id}")
        guild = response.json()
        await self.events.emit('on_guild_fetched', guild)
        return guild

    async def get_channel(self, channel_id):
        response = requests.get(f"{self.api_url}/api/channels/{channel_id}")
        channel = response.json()
        await self.events.emit('on_channel_fetched', channel)
        return channel

    async def get_message(self, message_id):
        response = requests.get(f"{self.api_url}/api/messages/{message_id}")
        message = response.json()
        await self.events.emit('on_message_fetched', message)
        return message
