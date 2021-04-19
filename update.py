import subprocess
import time

try:
    VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
except:
    print("Du scheinst kein Git installiert zu haben :(")
    print("Hier findest du raus, wie du es installieren kannst:")
    print("https://github.com/git-guides/install-git")
    time.sleep(25)


print("Checke auf Updates...")


def updaten():
    command = subprocess.check_output("git pull ", shell=True)
    if str("Already up to date.") in str(command):
        print(f"Der Bot is bereits auf der neusten Version({VERSION})!")
        raise Exception("Der Bot wurde geupdatet.")
    else:
        print(f"Der Bot wurde auf die Neuste Version geupdatet")

    time.sleep(5)


updaten()
