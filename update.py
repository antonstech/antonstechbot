import subprocess
import time

VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()

print("Checke auf Updates...")


def updaten():
    command = subprocess.check_output("git pull ", shell=True)
    if str("Already up to date.") in str(command):
        print(f"Der Bot is bereits auf der neusten Version({VERSION})!")
    else:
        print(f"Der Bot wurde auf die Neuste Version geupdatet")

    time.sleep(5)


updaten()
