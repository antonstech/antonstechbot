import json


def start():
    print("Wichtig: Dieses Script erstellt eine neue config.json")
    config = {'token': input("Dein Bot Token: "), 'prefix': input("Dein Bot Prefix: "),
              "riotapi": input("Dein Riot Games Api Token: "), "osuapi": input("Dein Osu Api Token: "), "ipdata": input("Dein ipdata.co Token: ")}
    with open('config.json', 'w+') as file:
        json.dump(config, file, indent=2)


start()
