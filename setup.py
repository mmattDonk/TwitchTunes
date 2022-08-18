"""
RUN THIS FOR FIRST TIME SETUP.
"""
import json
import os


def path_exists(filename):
    return os.path.join(".", f"{filename}")


input("Let's install the Python dependencies\nPress `ENTER` to continue. ")
os.system("pip install -U -r requirements.txt")

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
print("\n" * 10)

print("....Writing to `.env`")

if not os.path.exists(path_exists(".env")):
    with open(".env", "a") as env_file:
        env_file.write(
            f"TOKEN={token}\n"
            + "# Twitch IRC token\n"
            + f"client_id={client_id}\n"
            + "# Twitch Client ID from dev.twitch.tv\n"
            + f"channel_points_reward={channel_points_reward}\n"
            + "# Channel Point reward name\n"
            + f"\nspotify_client_id={spotify_client_id}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + f"spotify_secret={spotify_secret}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + "spotify_redirect_uri=http://localhost:8080\n"
            + "# Set your 'redirect_uri' and 'website' on your Spotify application to 'http://localhost:8080' (Don't change the spotify_redirect_uri in .env)"
        )

elif os.path.exists(path_exists(".env")):
    with open(".env", "w") as env_file:
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

print("Finished writing to `.env`")

print("....Writing to `config.json`")

if not os.path.exists(path_exists("config.json")):
    with open("config.json", "a") as config_file:
        config_file.write(
            json.dumps({"nickname": bot_name, "prefix": prefix, "channels": [channel]})
        )

elif os.path.exists(path_exists("config.json")):
    with open("config.json", "w") as config_file:
        config_file.write(
            json.dumps({"nickname": bot_name, "prefix": prefix, "channels": [channel]})
        )

print("Finished writing to `config.json`")

print("....Writing to `blacklist.json`")

if not os.path.exists(path_exists("blacklist.json")):
    with open("blacklist.json", "a") as blacklist_file:
        blacklist_file.write(json.dumps({"blacklist": []}))

elif os.path.exists(path_exists("blacklist.json")):
    with open("blacklist.json", "w") as blacklist_file:
        blacklist_file.write(json.dumps({"blacklist": []}))

print("Finished writing to `blacklist.json`")

print("....Writing to `blacklist_user.json`")

if not os.path.exists(path_exists("blacklist_user.json")):
    with open("blacklist_user.json", "a") as blacklist_user_file:
        blacklist_user_file.write(json.dumps({"users": []}))

elif os.path.exists(path_exists("blacklist_user.json")):
    with open("blacklist_user.json", "w") as blacklist_user_file:
        blacklist_user_file.write(json.dumps({"users": []}))

print("Finished writing to `blacklist_user.json`")

print("\n" * 10)

input(
    "All done!, enjoy using your TwitchTunes Bot!\nAll you have to do now, is run the `bot.py` file!"
)
