import json
import logging
import os
import sys

from rich.logging import RichHandler
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope

log_level = logging.DEBUG if "dev".lower() in sys.argv else logging.INFO


log = logging.getLogger()


logging.basicConfig(
    level=log_level,
    format="%(name)s - %(message)s",
    datefmt="%X",
    handlers=[RichHandler()],
)


def path_exists(filename):
    return os.path.join(".", f"{filename}")


if not os.path.exists(path_exists("config.json")):
    print("\n--------------------------")
    print("\nwhat's your Twitch Bot's name?")
    bot_name = input(
        "Type your Bot's name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nwhat will your prefix be? (example: !, ?, $)")
    prefix = input("Type your prefix, then press `ENTER`. (You can change this later) ")
    print("\n--------------------------")
    print("\nwhat's your Twitch Channel's name?")
    channel = input(
        "Type your Channel's name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")

    with open("config.json", "a") as config_file:
        config_file.write(
            json.dumps({"nickname": bot_name, "prefix": prefix, "channels": [channel]})
        )

if not os.path.exists(path_exists(".env")):
    print("\n⚠⚠⚠⚠⚠ WARNING: DO NOT SHOW THE FOLLOWING ON STREAM. ⚠⚠⚠⚠⚠" * 10)
    input("\nPress `ENTER` if this is not showing on stream.")

    print("\n" * 100)
    print("Cool, now let's get to the boring stuff...")
    print("\n--------------------------")
    print("\nlet's set up the bot's token")
    token = input(
        "You can get this token from a site like https://twitchapps.com/tmi/.\nJust copy and paste the OAuth token into here.\nType token, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Twitch Client ID")
    client_id = input(
        "You can get this by going to https://dev.twitch.tv/console/apps/create, signing in, creating a 'Chat Bot' application (the OAuth redirect URLs NEED to be 'http://localhost:17563/' and 'http://localhost:17563')\nNow just copy and paste the Client ID into here.\nType the Client ID, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Twitch Client Secret")
    client_secret = input(
        'You can get this by scrolling down on your application, and clicking the "New Secret" button.\nNow just copy and paste the Client Secret into here.\nType the Client Secret, then press `ENTER`. (You can change this later) '
    )
    print("\n--------------------------")
    channel_points_reward = input(
        "If you are going to use TwitchTunes with channel points, then what is your Channel Point reward name?\nType the Channel Point reward name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlets setup the Spotify Client ID")
    spotify_client_id = input(
        "You can get this by going to https://developer.spotify.com/dashboard/applications, signing in, then creating an application.\nJust paste in the Client ID into here now.\nType Spotify's Client ID, then press `ENTER`. (You can change this later)"
    )
    print("\n--------------------------")
    print("\nlet's setup the Spotify Client Secret")
    spotify_secret = input(
        "You can get this by going to that application page, then clicking the 'SHOW CLIENT SECRET' button.\nNow just paste the Client Secret here.\nType Spotify Client Secret, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Spotify Website/Redirect URI")
    input(
        "All you have to do, is hit the settings button, then in BOTH the Website field, AND the Redirect URIs field, but 'http://localhost:8080'\nPress `ENTER` once you have completed this step."
    )

    with open(".env", "a") as env_file:
        env_file.write(
            f"TOKEN={token}\n"
            + "# Twitch IRC token\n"
            + f"client_id={client_id}\n"
            + "# Twitch Client ID from dev.twitch.tv\n"
            + f"client_secret={client_secret}\n"
            + "# Twitch Client Secret from dev.twitch.tv\n"
            + f"channel_points_reward={channel_points_reward}\n"
            + "# Channel Point reward name\n"
            + f"\nspotify_client_id={spotify_client_id}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + f"spotify_secret={spotify_secret}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + "spotify_redirect_uri=http://localhost:8080\n"
            + "# Set your 'redirect_uri' and 'website' on your Spotify application to 'http://localhost:8080' (Don't change the spotify_redirect_uri in .env)"
        )

if not os.path.exists(path_exists("blacklist.json")):
    with open("blacklist.json", "a") as blacklist_file:
        blacklist_file.write(json.dumps({"blacklist": []}))

if not os.path.exists(path_exists("blacklist_user.json")):
    with open("blacklist_user.json", "a") as blacklist_user_file:
        blacklist_user_file.write(json.dumps({"users": []}))


log.info("\n\nStarting 🎶TwitchTunes")

from pathlib import Path

import dotenv
from twitchio.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)
import asyncio
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
        redirect_uri="http://localhost:8080",
        scope=[
            "user-modify-playback-state",
            "user-read-currently-playing",
            "user-read-playback-state",
            "user-read-recently-played",
        ],
    )
)


def read_json(filename):
    with open(f"{filename}.json") as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


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
        self.version = "1.4.0"

    async def event_ready(self):
        log.info("\n" * 100)
        log.info(f"TwitchTunes ({self.version}) Ready, logged in as: {self.nick}")

    def is_owner(self, ctx):
        return ctx.author.id == "640348450"

    # This is an owner only command for an inside joke in a certain channel, just ignore this :)
    @commands.command(name="s3s")
    async def s3s(self, ctx):
        if self.is_owner(ctx) and ctx.channel.name == "tajj":
            same_3_songs = [
                "spotify:track:7jVH8CXr0MSpGheHOjN4NA",
                "spotify:track:0BRbI3ZMPXuj9yA7ChDGOW",
                "spotify:track:0S8pAna5CIUy0g9XM5hBeF",
            ]
            for song in same_3_songs:
                sp.add_to_queue(song)
                await asyncio.sleep(0.1)
            await ctx.send("forsenPls same 3 songs forsenPls")

    @commands.command(name="ping", aliases=["ding"])
    async def ping_command(self, ctx):
        await ctx.send(
            f":) 🎶 TwitchTunes v{self.version} (Spotify Song Requests) is online!"
        )

    @commands.command(name="blacklistuser")
    async def blacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod or self.is_owner(ctx):
            file = read_json("blacklist_user")
            if user not in file["users"]:
                file["users"].append(user)
                write_json(file, "blacklist_user")
                await ctx.send(f"{user} added to blacklist")
            else:
                await ctx.send(f"{user} is already blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

    @commands.command(name="unblacklistuser")
    async def unblacklist_user(self, ctx, *, user: str):
        user = user.lower()
        if ctx.author.is_mod or self.is_owner(ctx):
            file = read_json("blacklist_user")
            if user in file["users"]:
                file["users"].remove(user)
                write_json(file, "blacklist_user")
                await ctx.send(f"{user} removed from blacklist")
            else:
                await ctx.send(f"{user} is not blacklisted")
        else:
            await ctx.send("You don't have permission to do that.")

    @commands.command(name="blacklist", aliases=["blacklistsong", "blacklistadd"])
    async def blacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod or self.is_owner(ctx):
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if song_uri not in jscon["blacklist"]:
                if re.match(URL_REGEX, song_uri):
                    data = sp.track(song_uri)
                    song_uri = data["uri"]
                    song_uri = song_uri.replace("spotify:track:", "")

                track = sp.track(song_uri)

                track_name = track["name"]

                jscon["blacklist"].append(song_uri)

                write_json(jscon, "blacklist")

                await ctx.send(f"Added {track_name} to blacklist.")

            else:
                await ctx.send("Song is already blacklisted.")

        else:
            await ctx.send("You are not authorized to use this command.")

    @commands.command(
        name="unblacklist", aliases=["unblacklistsong", "blacklistremove"]
    )
    async def unblacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod or self.is_owner(ctx):
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if re.match(URL_REGEX, song_uri):
                data = sp.track(song_uri)
                song_uri = data["uri"]
                song_uri = song_uri.replace("spotify:track:", "")

            if song_uri in jscon["blacklist"]:
                jscon["blacklist"].remove(song_uri)
                write_json(jscon, "blacklist")
                await ctx.send("Removed that song from the blacklist.")

            else:
                await ctx.send("Song is not blacklisted.")
        else:
            await ctx.send("You are not authorized to use this command.")

    @commands.command(name="np", aliases=["nowplaying", "song"])
    async def np_command(self, ctx):
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

    @commands.command(
        name="lastsong", aliases=["previoussongs", "last", "previousplayed"]
    )
    async def queue_command(self, ctx):
        queue = sp.current_user_recently_played(limit=10)
        songs = []

        for song in queue["items"]:
            # if the song artists include more than one artist: add all artist names to an artist list variable
            if len(song["track"]["artists"]) > 1:
                artists = [artist["name"] for artist in song["track"]["artists"]]
                song_artists = ", ".join(artists)
            # if the song artists only include one artist: add the artist name to the artist list variable
            else:
                song_artists = song["track"]["artists"][0]["name"]

            songs.append(song["track"]["name"] + " - " + song_artists)

        await ctx.send("Recently Played: " + " | ".join(songs))

    @commands.command(name="songrequest", aliases=["sr", "addsong"])
    async def songrequest_command(self, ctx, *, song: str):
        song_uri = None
        if ctx.author.is_mod or self.is_owner(ctx):
            if (
                song.startswith("spotify:track:")
                or not song.startswith("spotify:track:")
                and re.match(URL_REGEX, song)
            ):
                song_uri = song
                await self.chat_song_request(ctx, song_uri, song_uri, album=False)

            else:
                await self.chat_song_request(ctx, song, song_uri, album=False)
        else:
            await ctx.send(f"@{ctx.author.name}, you don't have permission to do that.")
            return

    # @commands.command(name="skip")
    # async def skip_song_command(self, ctx):
    #     sp.next_track()
    #     await ctx.send(f":) 🎶 Skipping song...")

    # @commands.command(name="albumqueue")
    #     if ctx.author.is_mod or ctx.author.is_subscriber or self.is_owner(ctx):
    # async def albumqueue_command(self, ctx, *, album: str):
    #         album_uri = None

    #         if (
    #             album.startswith("spotify:album:")
    #             or not album.startswith("spotify:album:")
    #             and re.match(URL_REGEX, album)
    #         ):
    #             album_uri = album
    #         await self.album_request(ctx, album_uri)
    #     else:
    #         await ctx.send(f"🎶You don't have permission to do that! (Album queue is Sub Only!)")

    """
        DO NOT USE THE API REQUEST IT WONT WORK.
        the logic should still work iwth using the spotipy library, so thats why I'm keeping it, but don't do an API request
        - like this.
    """
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

    async def chat_song_request(self, ctx, song, song_uri, album: bool):
        blacklisted_users = read_json("blacklist_user")["users"]
        if ctx.author.name.lower() in blacklisted_users:
            await ctx.send("You are blacklisted from requesting songs.")
        else:
            jscon = read_json("blacklist")

            if song_uri is None:
                data = sp.search(song, limit=1, type="track", market="US")
                song_uri = data["tracks"]["items"][0]["uri"]

            elif re.match(URL_REGEX, song_uri):
                data = sp.track(song_uri)
                song_uri = data["uri"]
                song_uri = song_uri.replace("spotify:track:", "")

            song_id = song_uri.replace("spotify:track:", "")

            if not album:
                data = sp.track(song_id)
                song_name = data["name"]
                song_artists = data["artists"]
                song_artists_names = [artist["name"] for artist in song_artists]
                duration = data["duration_ms"] / 60000

            if song_uri != "not found":
                if song_id in jscon["blacklist"]:
                    await ctx.send("That song is blacklisted.")

                elif duration > 17:
                    await ctx.send("Send a shorter song please! :)")
                else:
                    sp.add_to_queue(song_uri)
                    await ctx.send(
                        f"@{ctx.author.name}, Your song ({song_name} by {', '.join(song_artists_names)}) [ {data['external_urls']['spotify']} ] has been added to the queue!"
                    )


def song_request(data, song, song_uri, album: bool):
    jscon = read_json("blacklist")
    if song_uri is None:
        data = sp.search(song, limit=1, type="track", market="US")
        song_uri = data["tracks"]["items"][0]["uri"]
    elif re.match(URL_REGEX, song_uri):
        data = sp.track(song_uri)
        song_uri = data["uri"]
        song_uri = song_uri.replace("spotify:track:", "")
    song_id = song_uri.replace("spotify:track:", "")
    if not album:
        data = sp.track(song_id)
        duration = data["duration_ms"] / 60000
    if song_uri != "not found":
        if song_id in jscon["blacklist"] or duration > 17:
            return
        else:
            sp.add_to_queue(song_uri)


def callback_channel_points(uuid, data: dict) -> None:
    if (
        data["data"]["redemption"]["reward"]["title"].lower()
        != os.environ.get("channel_points_reward").lower()
    ):
        return

    log.debug(data)

    song: str = data["data"]["redemption"]["user_input"]
    ctx = None
    blacklisted_users = read_json("blacklist_user")["users"]
    if data["data"]["redemption"]["user"]["login"] in blacklisted_users:
        return
    if (
        song.startswith("spotify:track:")
        or not song.startswith("spotify:track:")
        and re.match(URL_REGEX, song)
    ):
        song_uri = song
        song_request(ctx, song_uri, song_uri, album=False)
    else:
        song_request(ctx, song, song_uri=None, album=False)


if os.environ.get("channel_points_reward"):
    channel_points_reward = os.environ.get("channel_points_reward")
    twitch = Twitch(os.environ.get("client_id"), os.environ.get("client_secret"))
    twitch.authenticate_app([])
    target_scope: list = [AuthScope.CHANNEL_READ_REDEMPTIONS]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    # add User authentication
    twitch.set_user_authentication(token, target_scope, refresh_token)

    user_id: str = twitch.get_users(logins=config["channels"])["data"][0]["id"]

    pubsub = PubSub(twitch)
    uuid = pubsub.listen_channel_points(user_id, callback_channel_points)
    pubsub.start()

bot = Bot()
bot.run()
