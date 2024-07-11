import aiohttp
import asyncio
import json
from events import events

DISCORD_GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

class Bot:
    def __init__(self, api_url, command_prefix='!'):
        self.api_url = api_url
        self.events = events()
        self.token = None
        self.session = None
        self.ws = None
        self.prefix = command_prefix
        self.intents = INTENTS.get(intents, 513)
        self.commands = {}

    def event(self, func):
        return self.events.event(func)

    def command(self, name=None):
        def decorator(func):
            self.commands[name or func.__name__] = func
            return func
        return decorator

    async def start(self, token):
        self.token = token
        self.session = aiohttp.ClientSession()
        await self.connect_to_discord_gateway()

    async def close(self):
        await self.session.close()

    async def connect_to_discord_gateway(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(DISCORD_GATEWAY_URL) as ws:
                self.ws = ws
                await self.identify()
                async for message in ws:
                    await self.handle_gateway_message(message)

    async def identify(self):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513,  # GUILD_MESSAGES and GUILD_MEMBERS
                "properties": {
                    "$os": "linux",
                    "$browser": "my_library",
                    "$device": "my_library"
                }
            }
        }
        await self.ws.send_json(payload)

    async def handle_gateway_message(self, message):
        message = json.loads(message)
        if message['t'] == 'READY':
            await self.events.emit('on_ready')
        elif message['t'] == 'MESSAGE_CREATE':
            await self.events.emit('on_message', message['d'])
            await self.handle_message_create(message['d'])
        elif message['t'] == 'GUILD_MEMBER_ADD':
            await self.events.emit('on_member_join', message['d'])
        elif message['t'] == 'GUILD_MEMBER_REMOVE':
            await self.events.emit('on_member_leave', message['d'])

    async def handle_message_create(self, message):
        content = message['content']
        if content.startswith(self.prefix):
            cmd_name, *args = content[len(self.prefix):].split()
            if cmd_name in self.commands:
                await self.commands[cmd_name](self, message, *args)

    def run(self, token):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start(token))
        except KeyboardInterrupt:
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    async def get_user(self, user_id):
        async with self.session.get(f"{self.api_url}/users/{user_id}") as response:
            user = await response.json()
            await self.events.emit('on_user_fetched', user)
            return user

    async def get_guild(self, guild_id):
        response = await self.session.get(f"{self.api_url}/api/guilds/{guild_id}", headers={"Authorization": f"Bot {self.token}"})
        guild = await response.json()
        await self.events.emit('on_guild_fetched', guild)
        return guild

    async def get_channel(self, channel_id):
        response = await self.session.get(f"{self.api_url}/api/channels/{channel_id}", headers={"Authorization": f"Bot {self.token}"})
        channel = await response.json()
        await self.events.emit('on_channel_fetched', channel)
        return channel

    async def get_message(self, message_id):
        response = await self.session.get(f"{self.api_url}/api/messages/{message_id}", headers={"Authorization": f"Bot {self.token}"})
        message = await response.json()
        await self.events.emit('on_message_fetched', message)
        return message
