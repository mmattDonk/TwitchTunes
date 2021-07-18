import datetime
from aiohttp import request
import twitchio
from twitchio.ext import commands

import os

import dotenv

import json
import re

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

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

        self.token = os.environ.get("SPOTIFY_AUTH")
        self.version = "1.1"

    async def event_ready(self):
        print(f"TwitchTunes ({self.version}) Ready, logged in as: {self.nick}")

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
    async def songrequest_command(self, ctx, *, song: str):
        song_uri = "not found"

        if song.startswith("spotify:track:"):
            song_uri = song

        if re.match(URL_REGEX, song):
            await ctx.send("Please send a song name/song URI instead!")

        else:
            if song_uri == "not found":
                GET_SONG_URL = (
                    f"https://api.spotify.com/v1/search?q={song}&type=track&market=US"
                )
                async with request(
                    "GET",
                    GET_SONG_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}",
                    },
                ) as resp:
                    data = await resp.json()
                    if resp.status == 200:
                        song_uri = data["tracks"]["items"][0]["uri"]

                    else:
                        await ctx.send("Couldn't find that song :/")

            if song_uri != "not found":
                QUEUE_URL = f"https://api.spotify.com/v1/me/player/queue?uri={song_uri}"
                async with request(
                    "POST",
                    QUEUE_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}",
                    },
                ) as resp:
                    if resp.status == 204:
                        await ctx.send(f"@{ctx.author.name}, your song has been added!")
                    else:
                        await ctx.send(f"Error: {resp.status}")


bot = Bot()
bot.run()
