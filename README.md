## `🎶` TwitchTunes
#### A Python Twitch bot that lets viewers add Spotify songs to your Spotify queue. 


## `💻` Prerequisites
1. Python
    - [Windows](https://www.python.org/downloads/)
        * Choco: `choco install python`
    - [Mac](https://www.python.org/downloads/)
        * Brew: `brew install python3` and `brew install pip3`
    - [Ubuntu Guide](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)
2. A Twitch bot account
3. A Spotify account (I think Premium is required, not sure.)

### `✨` Useful things to have before running `setup.py`
1. [Bot Token](https://twitchapps.com/tmi/)
2. [Twitch Application](https://dev.twitch.tv/console/apps/create)
    * Create a `Chat Bot` application
    * the OAuth redirect URL can just be `http://localhost`
3. [Spotify Application](https://developer.spotify.com/dashboard/applications)
    * Set the Website and Redirect URLs to `http://localhost:8080`

### `⚙` Setup
1. Run the `setup.py` script. **<!! RUN `setup.py` ONCE, IF YOU NEED ADDITIONAL FILES, CHECK THE [WIKI](https://github.com/mmattDonk/TwitchTunes/wiki) !!>**
2. Follow all the instructions!

### `❗` How to request songs
1. !sr {song name}
    * You can also use a Spotify URL or URI
        * You can get a URI by searching a song on Spotify, then holding down the `Ctrl` key while right clicking on the song, and then selecting "Copy Spotify URI" from the Share menu.

### `💎` Other Commands:
 - Variables:
    
    * `{user}` - Twitch Username

    * `{song}` - Can be a song name, a Spotify URI, or a Spotify URL (for the blacklist commands, it can only be a URI or URL)

 - Commands:

    * `!ping` - Checks if the bot is online + shows what version

    * `!blacklistuser {user}` - Blacklists a user from using the bot

    * `!unblacklistuser {user}` - Unblacklists a user from using the bot

    * `!blacklist {song}` - Blacklists a song from being played

    * `!unblacklist {song}` - Unblacklists a song from being played

    * `!np` - Shows the current song

    * `!songrequest {song}` - Requests a song to be played 

### `🙌` Code Contributors

<table>
<tr>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a href=https://github.com/mmattbtw>
            <img src=https://avatars.githubusercontent.com/u/30363562?v=4 width="100;"  style="border-radius:50%;align-items:center;justify-content:center;overflow:hidden;padding-top:10px" alt=matt/>
            <br />
            <sub style="font-size:14px"><b>matt</b></sub>
        </a>
    </td>
    <td align="center" style="word-wrap: break-word; width: 150.0; height: 150.0">
        <a href=https://github.com/MrAuro>
            <img src=https://avatars.githubusercontent.com/u/35087590?v=4 width="100;"  style="border-radius:50%;align-items:center;justify-content:center;overflow:hidden;padding-top:10px" alt=Auro/>
            <br />
            <sub style="font-size:14px"><b>Auro</b></sub>
        </a>
    </td>
</tr>
</table>
