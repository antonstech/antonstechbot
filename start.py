from consolemenu import *
from consolemenu.items import *
import os
import sys
import subprocess
import webbrowser
import time
import requests
import json
from colorama import *
from botlibrary import constants

try:
    VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
except:
    VERSION = "9.0"
    print("Please install GIT!!!")

constants.assignVariables()


def browser():
    webbrowser.open("https://git.io/antonsbot")
    print("No Webbrowser found please go to https://git.io/antonsbot ")

    time.sleep(5)


def tokenchecker():
    # Riot
    with open('config/config.json', 'r') as f:
        json_stuff = json.load(f)
        riotapi = json_stuff["riotapi"]
    base_riot_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/DCGALAXY?api_key="
    rioturl = base_riot_url + riotapi
    response = requests.get(rioturl)
    if response.status_code == 200:
        print(Fore.GREEN + "Riot Games API Key ✅")
    else:
        print(Fore.RED + "Riot Games API Key ❌")
    # Osu
    with open('config/config.json', 'r') as f:
        json_stuff = json.load(f)
        osuapi = json_stuff["osuapi"]
    base_osu_url = "https://osu.ppy.sh/api/get_user_best?u=Aftersh0ock&k="
    osuurl = base_osu_url + osuapi
    osuresponse = requests.get(osuurl)
    if osuresponse.status_code == 200:
        print(Fore.GREEN + "Osu API Key ✅")
    else:
        print(Fore.RED + "Osu API Key ❌")
    # Discord
    with open('config/config.json', 'r') as f:
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
    # ipdata
    with open('config/config.json', 'r') as f:
        json_stuff = json.load(f)
        ipdata = json_stuff["ipdata"]
    baseipurl = "https://api.ipdata.co/8.8.8.8"
    ipurl = baseipurl + "?api-key=" + ipdata
    ipresponse = requests.get(ipurl)
    if ipresponse.status_code == 200:
        print(Fore.GREEN + "ipdata API Key ✅")
    else:
        print(Fore.RED + "ipdata API Key ❌")
    url = constants.coc_url
    headers = {"Authorization": "Bearer " + constants.coc_token}
    cocresponse = requests.get(url, headers=headers)
    if cocresponse.status_code == 200:
        print(Fore.GREEN + "CoC API Key ✅")
    else:
        print(Fore.RED + "CoC API Key ❌")
    print(Style.RESET_ALL)
    time.sleep(7)


def config():
   print("Okay so to Edit the Config you just simply need to make a new file called 'config.ini' where you just copy the Things from config.ini.example in and then u Edit it")
   print("I also made a Tutorial on Github")


def run_bot():
    if sys.platform == "win32":
        os.system("py -3 bot.py")
    else:
        os.system("python3 bot.py")


def update_bot():
    if sys.platform == "win32":
        os.system("py -3 update.py")
    else:
        os.system("python3 update.py")


menu = ConsoleMenu(f"antonstechbot Version {VERSION} by antonstech",
                   "https://git.io/antonsbot")

starten = FunctionItem("Start Bot", run_bot)
config = FunctionItem("Edit Config", config)
updaten = FunctionItem("Bot Updaten", update_bot)
tokencheck = FunctionItem("Token-Checker", tokenchecker)
infos = FunctionItem("Information about the Bot & Code", browser)
updatemenu = ConsoleMenu("Menu to Update Things")
updateeee = SubmenuItem("Updaten", updatemenu, menu)
pipupdate = CommandItem("Update pip Modules", "pip3 install --upgrade --force-reinstall -r requirements.txt")

menu.append_item(starten)
menu.append_item(config)
menu.append_item(updateeee)
menu.append_item(tokencheck)
menu.append_item(infos)
updatemenu.append_item(updaten)
updatemenu.append_item(pipupdate)

menu.show()
