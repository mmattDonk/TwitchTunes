"""
RUN THIS FOR FIRST TIME SETUP.
"""
import os

import json


input(
    "Let's install the Python dependencies\n(This will also happen every time you open bot.py, to make sure they are up to date)\nPress `ENTER` to continue. "
)
os.system("pip install -U -r requirements.txt")

print("\n⚠⚠⚠⚠⚠ WARNING: DO NOT SHOW THE FOLLOWING ON STREAM. ⚠⚠⚠⚠⚠" * 10)
input("\nPress `ENTER` if this is not showing on stream.")

print("\n" * 100)
print("Cool, now let's get to the boring stuff...")
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nFirst, let's set up the bot's token")
token = input(
    "You can get this token from a site like https://twitchapps.com/tmi/.\nJust copy and paste the OAuth token into here.\nType token, then press `ENTER`. (You can change this later) "
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nSecond, let's setup the Twitch Client ID")
client_id = input(
    "You can get this by going to https://dev.twitch.tv/console/apps/create, signing in, creating a 'Chat Bot' application (the OAuth redirect URLs can just be 'http://localhost')\nNow just copy and paste the Client ID into here.\nType the Client ID, then press `ENTER`. (You can change this later) "
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nThird, lets setup the Spotify Client ID")
spotify_client_id = input(
    "You can get this by going to https://developer.spotify.com/dashboard/applications, signing in, then creating an application.\nJust paste in the Client ID into here now.\nType Spotify's Client ID, then press `ENTER`. (You can change this later)"
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nFourth, let's setup the Spotify Client Secret")
spotify_secret = input(
    "You can get this by going to that application page, then clicking the 'SHOW CLIENT SECRET' button.\nNow just paste the Client Secret here.\nType Spotify Client Secret, then press `ENTER`. (You can change this later) "
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nFifth, let's setup the Spotify Website/Redirect URI")
input(
    "All you have to do, is hit the settings button, then in BOTH the Website field, AND the Redirect URIs field, but 'http://localhost:8080'\nPress `ENTER` once you have completed this step."
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nSixth, what's your Twitch Bot's name?")
bot_name = input(
    "Type your Bot's name, then press `ENTER`. (You can change this later) "
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nSeventh, what will your prefix be? (example: !, ?, $)")
prefix = input("Type your prefix, then press `ENTER`. (You can change this later) ")
print("\n=-=-=-=-=-=-=-=-=-=")
print("\nEighth, what's your Twitch Channel's name?")
channel = input(
    "Type your Channel's name, then press `ENTER`. (You can change this later) "
)
print("\n=-=-=-=-=-=-=-=-=-=")
print("\n" * 10)

with open(".env", "a") as env_file:
    env_file.write(
        f"TOKEN={token}\n"
        + "# Twitch IRC token\n"
        + f"client_id={client_id}\n"
        + "# Twitch Client ID from dev.twitch.tv\n"
        + f"\nspotify_client_id={spotify_client_id}\n"
        + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
        + f"spotify_secret={spotify_secret}\n"
        + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
        + "spotify_redirect_uri=http://localhost:8080\n"
        + "# Set your 'redirect_uri' and 'website' on your Spotify application to 'http://localhost:8080' (Don't change the spotify_redirect_uri in .env)"
    )

with open("config.json", "a") as config_file:
    config_file.write(
        json.dumps({"nickname": bot_name, "prefix": prefix, "channels": [channel]})
    )

input(
    "All done!, enjoy using your Song Request Bot!\nAll you have to do now, is run the `bot.py` file!"
)
