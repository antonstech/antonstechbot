from consolemenu import *
from consolemenu.items import *
import os
import subprocess
import webbrowser
import time
import requests
import json
from colorama import *

VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()

menu = ConsoleMenu(f"antonstechbot Version {VERSION} by antonstech",
                   "https://git.io/antonsbot")

def browser():
    webbrowser.open("https://git.io/antonsbot")
    print("Kein Webbrowser gefunden, geh doch bitte auf https://git.io/antonsbot ")

    time.sleep(5)

def tokenchecker():
    ### Riot
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        riotapi = json_stuff["riotapi"]
    base_riot_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/DCGALAXY?api_key="
    rioturl = base_riot_url + riotapi
    response = requests.get(rioturl)
    if response.status_code == 200:
        print(Fore.GREEN + "Riot Games API Key ✅")
    else:
        print(Fore.RED + "Riot Games API Key ❌")
    ### Osu
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        osuapi = json_stuff["osuapi"]
    base_osu_url = "https://osu.ppy.sh/api/get_user_best?u=Aftersh0ock&k="
    osuurl = base_osu_url + osuapi
    osuresponse = requests.get(osuurl)
    if osuresponse.status_code == 200:
        print(Fore.GREEN + "Osu API Key ✅")
    else:
        print(Fore.RED + "Osu API Key ❌")
    ### Discord
    with open('config.json', 'r') as f:
        json_stuff = json.load(f)
        token = json_stuff["token"]
    headers = {
        "Authorization": "Bot " + token
    }
    response = requests.get('https://discordapp.com/api/v8/auth/login', headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + "Discord Token ✅")
    else:
        print(Fore.RED + "Discord Token ❌")
    print(Style.RESET_ALL)
    ### ipdata
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        ipdata = json_stuff["ipdata"]
    baseipurl = "https://api.ipdata.co/8.8.8.8"
    ipurl = baseipurl + "?api-key=" + ipdata
    ipresponse = requests.get(ipurl)
    if ipresponse.status_code == 200:
        print(Fore.GREEN + "ipdata API Key ✅")
    else:
        print(Fore.RED + "ipdata API Key ❌")
    time.sleep(7)

starten = FunctionItem("Bot starten", os.system, ["python3 bot.py"])
config = FunctionItem("Config bearbeiten", os.system, ["python3 config.py"])
updaten = FunctionItem("Bot Updaten", os.system, ["python3 update.py"])
tokencheck = FunctionItem("Token-Checker", tokenchecker)
infos = FunctionItem("Infos über den Bot&Code", browser)

menu.append_item(starten)
menu.append_item(config)
menu.append_item(updaten)
menu.append_item(tokencheck)
menu.append_item(infos)

menu.show()
