# ⚠ Known Issue: The Spotify OAuth token only lasts 1 hour, I am working on this issue and will fix ASAP (https://github.com/mmattbtw/TwitchTunes/issues/7)
## `🎶` TwitchTunes
#### A Python Twitch bot that lets viewers add Spotify songs to your Spotify queue. 


### `⚙` Setup
1. Duplicate `config_example.json`
    1. change name to `config.json`
    2. fill out the values
2. Install Python
    * Windows: python.org/downloads
    * MacOS: python.org/downloads
        * Brew: `brew install python3` & `brew install pip3`
4. Install Python dependencies
    1. just run `pip install -r requirements.txt` in your console in this folder.
5. Duplicate `.env.example` file
    1. copy `.env.example` to `.env`
    2. fill out the values
6. Run `bot.py`

### `❗` How to request songs
1. !sr {song name}
    * You can also use a Spotify URI
        * You can get a URI by searching a song on Spotify, then holding down the `Ctrl` key while right clicking on the song, and then selecting "Copy Spotify URI" from the Share menu.
