## `🎶` TwitchTunes [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mmattDonk/TwitchTunes/master.svg)](https://results.pre-commit.ci/latest/github/mmattDonk/TwitchTunes/master)

#### A Python Twitch bot that lets viewers add Spotify songs to your Spotify queue.

## `💻` Prerequisites

1. Python
   - [Windows](https://www.python.org/downloads/)
     - Choco: `choco install python`
   - [Mac](https://www.python.org/downloads/)
     - Brew: `brew install python3` and `brew install pip3`
   - [Ubuntu Guide](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)
2. A Twitch bot account
3. A Spotify account (Spotify Premium is required, this is an API limitation.)

### `✨` Useful things to have before running `setup.py`

1. [Bot Token](https://twitchapps.com/tmi/)
2. [Twitch Application](https://dev.twitch.tv/console/apps/create)
   - Create a `Chat Bot` application
   - the OAuth redirect URLs NEED to be `http://localhost:17563/` and `http://localhost:17563`
3. [Spotify Application](https://developer.spotify.com/dashboard/applications)
   - Set the Website and Redirect URLs to `http://localhost:8080`

### `⚙` Setup

1. Run the `setup.py` script. **<!! RUN `setup.py` ONCE, IF YOU NEED ADDITIONAL FILES, CHECK THE [WIKI](https://github.com/mmattDonk/TwitchTunes/wiki) !!>**
2. Follow all the instructions!

### `❗` How to request songs

1. !sr {song name}
   - You can also use a Spotify URL or URI
     - You can get a URI by searching a song on Spotify, then holding down the `Ctrl` key while right clicking on the song, and then selecting "Copy Spotify URI" from the Share menu.
2. If your streamer sets up channel points:
   - Redeem the TwitchTunes channel point reward!
     - In the that shows up, just send a spotify link!

### `💎` Other Commands:

- Variables:

  - `{user}` - Twitch Username

  - `{song}` - Can be a song name, a Spotify URI, or a Spotify URL (for the blacklist commands, it can only be a URI or URL)

- Commands:

  - `!ping` - Checks if the bot is online + shows what version

  - `!blacklistuser {user}` - Blacklists a user from using the bot

  - `!unblacklistuser {user}` - Unblacklists a user from using the bot

  - `!blacklist {song}` - Blacklists a song from being played

  - `!unblacklist {song}` - Unblacklists a song from being played

  - `!np` - Shows the current song

  - `!songrequest {song}` - Requests a song to be played

  - `!lastsong` - Shows the last 10 songs that were played! (we still can't get the Spotify queue from the API https://community.spotify.com/t5/Closed-Ideas/Developer-Web-API-playback-queue-route/idc-p/5387376#M261127 i hate spotify web api...)
