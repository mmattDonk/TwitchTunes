import os

os.system("pip install -U -r requirements.txt")
print("\n\nStarting 🎶TwitchTunes")

from aiohttp import request

from twitchio.ext import commands
from twitchio.ext import pubsub

import dotenv

import json

import time

import re

from threading import Timer

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
        redirect_uri="http://localhost:8080",
        scope=[
            "user-modify-playback-state",
            "user-read-currently-playing",
            "user-read-playback-state",
        ],
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
        self.version = "1.2.5"
        self.queue = []

    async def event_ready(self):
        print("\n" * 100)
        print(f"TwitchTunes ({self.version}) Ready, logged in as: {self.nick}")
        print(
            "Ignore the 'AttributeError: 'NoneType' object has no attribute '_ws'' error, this is an issue with the library."
        )

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        await ctx.send(
            f":) 🎶 TwitchTunes v{self.version} (Spotify Song Requests) is online!"
        )

    @commands.command(name="np", aliases=["nowplaying", "song"])
    async def np_command(self, ctx):
        await self.np(ctx)

    async def np(ctx):
        data = sp.currently_playing()
        song_artists = data["item"]["artists"]
        song_artists_names = [artist["name"] for artist in song_artists]

        min_through = int(data["progress_ms"] / (1000 * 60) % 60)
        sec_through = int(data["progress_ms"] / (1000) % 60)
        time_through = f"{min_through} mins, {sec_through} secs"

        min_total = int(data["item"]["duration_ms"] / (1000 * 60) % 60)
        sec_total = int(data["item"]["duration_ms"] / (1000) % 60)
        time_total = f"{min_total} mins, {sec_total} secs"

        await ctx.send(
            f"🎶Now Playing - {data['item']['name']} by {', '.join(song_artists_names)} | Link: {data['item']['external_urls']['spotify']} | {time_through} - {time_total}"
        )

    def np_song_length(self):
        data = sp.currently_playing()
        ms = data["item"]["duration_ms"]
        ms_through = data["progress_ms"]

        subtract = ms - ms_through

        return subtract / 1000

    @commands.command(name="queue")
    async def queue_command(self, ctx):
        if self.queue:
            await ctx.send(f"🎶The queue contains: {', '.join(self.queue)}")
        else:
            await ctx.send(f"🎶The queue is empty!")

    @commands.command(name="clearqueue")
    async def clearqueue_command(self, ctx):
        if ctx.author.is_mod:
            if self.queue != []:
                self.queue.clear()
                await ctx.send(f"🎶The queue has been cleared!")
            else:
                await ctx.send(f"🎶The queue is already empty!")
        else:
            await ctx.send(f"🎶You don't have permission to do that!")

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

    # @commands.command(name="skip")
    # async def skip_song_command(self, ctx):
    #     sp.next_track()
    #     await ctx.send(f":) 🎶 Skipping song...")

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
            # sp.add_to_queue(song_uri)
            self.queue.append(
                f"{song_name} by {', '.join(song_artists_names)} [{ctx.author.name}]"
            )

            await self.queue_up_song(ctx, song_uri)

            await ctx.send(
                f"Your song ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ] has been added to {ctx.channel.name}'s queue!"
            )

    async def queue_up_song(self, ctx, song_uri):
        song_id = song_uri.replace("spotify:track:", "")

        data = sp.track(song_id)
        song_name = data["name"]
        song_artists = data["artists"]
        song_artists_names = [artist["name"] for artist in song_artists]
        seconds = self.np_song_length()
        queue_str = (
            f"{song_name} by {', '.join(song_artists_names)} [{ctx.author.name}]"
        )

        if queue_str == self.queue[0]:
            print(self.queue[0])
            print(queue_str)
            sp.add_to_queue(song_uri)
            sp.next_track()

        else:
            t = Timer(seconds, self.add_to_queue(song_uri))
            t.start()

    def add_to_queue(self, song_uri):
        sp.add_to_queue(song_uri)

        # self.queue.remove(
        #     f"{song_name} by {', '.join(song_artists_names)} [{ctx.author.name}]"
        # )


bot = Bot()
bot.run()
