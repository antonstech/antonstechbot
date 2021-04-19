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
    VERSION = 6.3
    print("Bitte installiert dir GIT!!!")

constants.assignVariables()

def browser():
    webbrowser.open("https://git.io/antonsbot")
    print("Kein Webbrowser gefunden, geh doch bitte auf https://git.io/antonsbot ")

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
    print("Für Hilfe bitte das Wiki auf Github lesen")
    print("WICHTIG!!!!")
    yesorno = input(
        "Es wird eine NEUE MySQL Datenbank UND Tabelle erzeugt, welche dann anschließend auch nach einem Neustarten vom Bot bentutzt wird!!!  (j/n): ")
    if yesorno == "j":
        config = {"enable": True, "host": input("Host: "), "user": input("Benutzername: "),
                  "passwort": input("Dein Passwort: "), "datenbank": input("Datenbank: "),
                  "tablename": input("Name der Tablle: "), "port": input("Port: ")}
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
            "CREATE TABLE " + table_name + " (time timestamp null, content text null, attachement text null, membername varchar(255) null, memberid bigint null, guildid bigint null, guildname varchar(255) null, channelid bigint null, channelname varchar(255) null, id bigint not null primary key)")
    else:
        pass


def tokens():
    print("Wichtig: Dieses Script erstellt eine neue config.json")
    config = {'token': input("Dein Bot Token: "), 'prefix': input("Dein Bot Prefix: "),
              "riotapi": input("Dein Riot Games Api Token: "), "osuapi": input("Dein Osu Api Token: "),
              "ipdata": input("Dein ipdata.co Token: "), "cocapi": input("Dein ClashOfClans Api Token: ")}
    with open('config/config.json', 'w+') as file:
        json.dump(config, file, indent=2)


def mysqldisable():
    if os.path.exists("config/mysql.json"):
        os.rename("config/mysql.json", "config/disabled_mysql.json")
        print("MySQL ist nun DEAKTIVIEREN!")
        print("Du musst den Bot 1x neustarten damit die Änderung wirksam wird!")
    else:
        if os.path.exists("config/disabled_mysql.json"):
            print("MySQL ist bereits deaktiviert")
        else:
            print("Iwas ist falsch gelaufen. Hier gibt es Hilfe:")
            print("https://github.com/antonstech/antonstechbot/wiki/Support")


def mysqlenable():
    if os.path.exists("config/disabled_mysql.json"):
        os.rename("config/disabled_mysql.json", "config/mysql.json")
        print("MySQL ist nun AKTIVIERT!")
        print("Du musst den Bot 1x neustarten damit die Änderung wirksam wird!")
    else:
        if os.path.exists("config/mysql.json"):
            print("MySQL ist bereits aktiviert")
        else:
            print("Iwas ist falsch gelaufen. Hier gibt es Hilfe:")
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

starten = FunctionItem("Bot starten", run_bot)
config = FunctionItem("Config bearbeiten", tokens)
updaten = FunctionItem("Bot Updaten", update_bot)
tokencheck = FunctionItem("Token-Checker", tokenchecker)
infos = FunctionItem("Infos über den Bot&Code", browser)
mysqlsetup = FunctionItem("MySQL Setup", mysqlsetup)
mysqldisable = FunctionItem("MySQL deaktivieren", mysqldisable)
mysqlenable = FunctionItem("MySQL aktivieren", mysqlenable)
submenu = ConsoleMenu("MySQL Menü")
mysqlmenu = SubmenuItem("MySQL Menü", submenu, menu)
updatemenu = ConsoleMenu("Menü um Sachen zu updaten")
updateeee = SubmenuItem("Updaten", updatemenu, menu)
pipupdate = CommandItem("pip Module updaten", "pip3 install --upgrade --force-reinstall -r requirements.txt")

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
