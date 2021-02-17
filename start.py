from consolemenu import *
from consolemenu.items import *
import os
import subprocess

menu = ConsoleMenu("simplediscordbot by antonstech",
                   "https://git.io/simplediscordbot")

def updaten():
    command = subprocess.check_output("git pull https://github.com/antonstech/simplediscordbot")
    if str("Already up to date.") in str(command):
        print("Der Bot is bereits auf der neusten Version!")
    else:
        print("Der Bot wurde geupdatet")



starten = FunctionItem("Bot starten", os.system, ["python3 bot.py"])
config = FunctionItem("Config bearbeiten", os.system, ["python3 setup.py"])
updaten = FunctionItem("Bot Updaten", updaten)
infos = FunctionItem("Infos über den Bot&Code", print, ["https://git.io/simplediscordbot"])

menu.append_item(starten)
menu.append_item(config)
menu.append_item(updaten)
menu.append_item(infos)

menu.show()

