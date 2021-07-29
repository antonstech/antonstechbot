import configparser
import subprocess

global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token, reddit_url, coc_token, coc_url, cat_api, anime, earth2, earth2landicon, host, user, password, database, port, logging_enable, channel_enable


def assignVariables():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token, reddit_url, coc_token, coc_url, cat_api, anime, earth2, earth2landicon, host, user, password, database, port, logging_enable, channel_enable
    try:
        VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
    except:
        VERSION = "8.1"

    # Here are just the Urls of the APIs so i can switch them out fast if they change

    reddit_url = "https://meme-api.herokuapp.com/gimme"
    cat_api = "https://api.thecatapi.com/v1/images/search"
    anime = "https://api.trace.moe/search?anilistInfo&url="
    earth2 = "https://earth2stats.net/api/get_countries/199"
    earth2landicon = "https://earth2stats.net/country/"

    bot_settings = config["Discord-Bot"]
    api_tokens = config["API-Tokens"]
    database_stuff = config["Database"]

    # And here i am reading out the API Tokens and other Stuff stored in json Files

    bot_prefix = bot_settings["default_prefix"]
    bot_token = bot_settings["token"]

    ipdata_token = api_tokens["ipdata"]
    ipdata_url = "https://api.ipdata.co/"

    osu_token = api_tokens["osuapi"]
    osu_url = "https://osu.ppy.sh/api/get_user?u="

    lol_token = api_tokens["riotapi"]
    lol_url = "https://euw1.api.riotgames.com/lol/"

    coc_token = api_tokens["cocapi"]
    coc_url = "https://api.clashofclans.com/v1/"

    # And here the Database Connection Values

    host = database_stuff["host"]
    user = database_stuff["user"]
    password = database_stuff["password"]
    database = database_stuff["database"]
    port = database_stuff["port"]

    # And here the Settings for the 2 Optional Features

    logging_enable = database_stuff["logging-enable"]
    channel_enable = database_stuff["channel-enable"]