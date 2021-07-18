import datetime
from aiohttp import request
import twitchio
from twitchio.ext import commands

import os

import dotenv

import json

with open("config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message):
        print(
            f"[MESSAGE LOGS] ({message.channel.name}) "
            + message.author.name
            + " - "
            + message.content
        )
        await self.handle_commands(message)

    @commands.command(name="ping", aliases=["ding"])
    async def test_command(self, ctx):
        await ctx.send(f"FeelsDankMan 🔔 ding @{ctx.author.name} sr bot online")

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song_uri: str):
        QUEUE_URL = f"https://api.spotify.com/v1/me/player/queue?uri={song_uri}"

        async with request("POST", QUEUE_URL, headers={"Content-Type": "application/json" , "Authorization": f"Bearer {os.environ.get('SPOTIFY_AUTH')}"}) as resp:
            if resp.status == 204:
                await ctx.send(f"@{ctx.author.name}, your song has been added!")
            else:
                await ctx.send(f"Error: {resp.status}")

        


bot = Bot()
bot.run()