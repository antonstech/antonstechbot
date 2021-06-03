import subprocess
import time

try:
    VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
except:
    print("It seems like you haven't installed git :(")
    print("See here how you can install it:")
    print("https://github.com/git-guides/install-git")
    time.sleep(25)


print("Checke auf Updates...")


def updaten():
    command = subprocess.check_output("git pull ", shell=True)
    if str("Already up to date.") in str(command):
        print(f"The Bot is already on the newest Version({VERSION})!")
        time.sleep(5)
    else:
        raise Exception("Der Bot wurde geupdatet.")


updaten()
