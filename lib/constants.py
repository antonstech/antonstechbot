import subprocess
import json

global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token


def assignVariables():
    global VERSION, bot_prefix, ipdata_token, ipdata_url, osu_token, osu_url, lol_token, lol_url, bot_token
    VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()

    with open('config/config.json', 'r') as f:
        json_stuff = json.load(f)

        bot_prefix = json_stuff["prefix"]

        bot_token = json_stuff["token"]

        ipdata_token = json_stuff["ipdata"]
        ipdata_url = "https://api.ipdata.co/"

        osu_token = json_stuff["osuapi"]
        osu_url = "https://osu.ppy.sh/api/get_user?u="

        lol_token = json_stuff["riotapi"]
        lol_url = "https://euw1.api.riotgames.com/lol/"
