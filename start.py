from consolemenu import *
from consolemenu.items import *
import os
import subprocess
import webbrowser
import time

VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()

menu = ConsoleMenu(f"simplediscordbot Version {VERSION} by antonstech",
                   "https://git.io/simplebot")

def browser():
    webbrowser.open("https://git.io/simplebot")
    print("Kein Webbrowser gefunden, geh doch bitte auf https://git.io/simplebot ")

    time.sleep(5)

starten = FunctionItem("Bot starten", os.system, ["python3 bot.py"])
config = FunctionItem("Config bearbeiten", os.system, ["python3 config.py"])
updaten = FunctionItem("Bot Updaten", os.system, ["python3 update.py"])
infos = FunctionItem("Infos über den Bot&Code", browser)

menu.append_item(starten)
menu.append_item(config)
menu.append_item(updaten)
menu.append_item(infos)

menu.show()
