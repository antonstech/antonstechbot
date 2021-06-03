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
import mysql.connector
from botlibrary import constants

try:
    VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
except:
    VERSION = "7.1.1"
    print("Bitte installiert dir GIT!!!")

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


def mysqlsetup():
    print("MySql Setup")
    print("For Help read the Wiki on Github")
    print("IMPORTANT!!!!")
    yesorno = input(
        "A NEW MySQL database AND table is created, which is then also used by the bot after a restart!!!  (y/n): ")
    if yesorno == "j":
        config = {"enable": True, "host": input("Host: "), "user": input("Username: "),
                  "passwort": input("Passwort: "), "Database": input("Datenbank: "),
                  "tablename": input("Name of the table: "), "port": input("Port: ")}
        with open("config/mysql.json", "w+") as file:
            json.dump(config, file, indent=2)
        with open('config/mysql.json', 'r') as f:
            json_stuff = json.load(f)
            host = json_stuff["host"]
            user = json_stuff["user"]
            passwort = json_stuff["passwort"]
            datenbank = json_stuff["datenbank"]
            table_name = json_stuff["tablename"]
            port = json_stuff["port"]
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=passwort,
            database="mysql",
            port=port)
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE " + datenbank)
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=passwort,
            database=datenbank,
            port=port)
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE " + table_name + " (time timestamp null, content text null, attachment text null, membername varchar(255) null, memberid bigint null, guildid bigint null, guildname varchar(255) null, channelid bigint null, channelname varchar(255) null, id bigint not null primary key)")
    else:
        pass


def tokens():
    print("Important: This Script creates a new config.json")
    config = {'token': input("Your Bot Token: "), 'default_prefix': input("The default Bot Prefix: "),
              "riotapi": input("Your Riot Games Api Token: "), "osuapi": input("Your Osu Api Token: "),
              "ipdata": input("Your ipdata.co Token: "), "cocapi": input("Your ClashOfClans Api Token: ")}
    with open('config/config.json', 'w+') as file:
        json.dump(config, file, indent=2)


def mysqldisable():
    if os.path.exists("config/mysql.json"):
        os.rename("config/mysql.json", "config/disabled_mysql.json")
        print("MySQL is now deactivated!")
        print("You have to restart that Bot that the Changes are working!")
    else:
        if os.path.exists("config/disabled_mysql.json"):
            print("MySQL is already deactivated")
        else:
            print("Something went wrong here but there is help:")
            print("https://github.com/antonstech/antonstechbot/wiki/Support")


def mysqlenable():
    if os.path.exists("config/disabled_mysql.json"):
        os.rename("config/disabled_mysql.json", "config/mysql.json")
        print("MySQL is now ACTIVATED!")
        print("You have to restart that Bot that the Changes are working!")
    else:
        if os.path.exists("config/mysql.json"):
            print("MySQL is already activated")
        else:
            print("Something went wrong here but there is help:")
            print("https://github.com/antonstech/antonstechbot/wiki/Support")


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
config = FunctionItem("Edit Config", tokens)
updaten = FunctionItem("Bot Updaten", update_bot)
tokencheck = FunctionItem("Token-Checker", tokenchecker)
infos = FunctionItem("Information about the Bot & Code", browser)
mysqlsetup = FunctionItem("MySQL Setup", mysqlsetup)
mysqldisable = FunctionItem("Deactivate MySQL", mysqldisable)
mysqlenable = FunctionItem("Activate MySQL", mysqlenable)
submenu = ConsoleMenu("MySQL Menu")
mysqlmenu = SubmenuItem("MySQL Menu", submenu, menu)
updatemenu = ConsoleMenu("Menu to Update Things")
updateeee = SubmenuItem("Updaten", updatemenu, menu)
pipupdate = CommandItem("Update pip Modules", "pip3 install --upgrade --force-reinstall -r requirements.txt")

menu.append_item(starten)
menu.append_item(config)
menu.append_item(mysqlmenu)
menu.append_item(updateeee)
menu.append_item(tokencheck)
menu.append_item(infos)
submenu.append_item(mysqlsetup)
submenu.append_item(mysqldisable)
submenu.append_item(mysqlenable)
updatemenu.append_item(updaten)
updatemenu.append_item(pipupdate)

menu.show()
