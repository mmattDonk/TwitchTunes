import os

os.system("pip install -U -r requirements.txt")
os.system("clear")

from aiohttp import request

from twitchio.ext import commands
from twitchio.ext import pubsub

import dotenv

import json
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

with open("config.json") as config_file:
    config = json.load(config_file)

dotenv.load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ.get("spotify_client_id"),
        client_secret=os.environ.get("spotify_secret"),
        redirect_uri=os.environ.get("spotify_redirect_uri"),
        scope="user-modify-playback-state",
    )
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=config["prefix"],
            initial_channels=config["channels"],
        )

        self.token = os.environ.get("SPOTIFY_AUTH")
        self.version = "1.2.1"

    async def event_ready(self):
        print(f"TwitchTunes ({self.version}) Ready, logged in as: {self.nick}")

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        await ctx.send(f":) 🎶 TwitchTunes (Spotify Song Requests) is online!")

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song: str):
        song_uri = None

        if (
            song.startswith("spotify:track:")
            or not song.startswith("spotify:track:")
            and re.match(URL_REGEX, song)
        ):
            song_uri = song
            await self.song_request(ctx, song_uri, song_uri, album=False)

        else:
            await self.song_request(ctx, song, song_uri, album=False)

    # async def album_request(self, ctx, song):
    #     song = song.replace("spotify:album:", "")
    #     ALBUM_URL = f"https://api.spotify.com/v1/albums/{song}?market=US"
    #     async with request("GET", ALBUM_URL, headers={
    #                 "Content-Type": "application/json",
    #                 "Authorization": "Bearer " + self.token,
    #             }) as resp:
    #             data = await resp.json()
    #             songs_uris = [artist["uri"] for artist in data['tracks']['items']]

    #             for song_uris in songs_uris:
    #                 await self.song_request(ctx, song, song_uris, album=True)
    #             await ctx.send(f"Album Requested! {data['name']}")
    #             return

    async def song_request(self, ctx, song, song_uri, album: bool):
        if song_uri is None:
            data = sp.search(song, limit=1, type="track", market="US")
            song_uri = data["tracks"]["items"][0]["uri"]

        song_id = song_uri.replace("spotify:track:", "")

        if not album:
            data = sp.track(song_id)
            song_name = data["name"]
            song_artists = data["artists"]
            song_artists_names = [artist["name"] for artist in song_artists]

        if song_uri != "not found":
            print(song_uri)
            sp.add_to_queue(song_uri)
            await ctx.author.send(
                f"Your song ({song_name} by {', '.join(song_artists_names)}) has been added to {ctx.channel.name}'s queue!"
            )


bot = Bot()
bot.run()
