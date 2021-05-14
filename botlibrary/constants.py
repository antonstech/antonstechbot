import subprocess
import json

global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token, reddit_url, coc_token, coc_url, bitrate, cat_api, anime, earth2, earth2landicon


def assignVariables():
    global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token, reddit_url, coc_token, coc_url, bitrate, cat_api, anime, earth2, earth2landicon
    try:
        VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
    except:
        VERSION = 6.4

# Here are just the Urls of the APIs so i can switch them out fast if they change

    reddit_url = "https://meme-api.herokuapp.com/gimme"
    cat_api = "https://api.thecatapi.com/v1/images/search"
    anime = "https://api.trace.moe/search?anilistInfo&url="
    earth2 = "https://earth2stats.net/api/get_countries/199"
    earth2landicon = "https://earth2stats.net/country/"

# Here is the Audio Bitrate for Creating new Voicechannels via the privatechannels Function
    bitrate = 96000

# And here i am reading out the API Tokens and other Stuff stored in json Files

    with open('config/config.json', 'r') as f:
        json_stuff = json.load(f)

        bot_prefix = json_stuff["default_prefix"]

        bot_token = json_stuff["token"]

        ipdata_token = json_stuff["ipdata"]
        ipdata_url = "https://api.ipdata.co/"

        osu_token = json_stuff["osuapi"]
        osu_url = "https://osu.ppy.sh/api/get_user?u="

        lol_token = json_stuff["riotapi"]
        lol_url = "https://euw1.api.riotgames.com/lol/"

        coc_token = json_stuff["cocapi"]
        coc_url = "https://api.clashofclans.com/v1/"
