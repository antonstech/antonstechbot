import json

def start():
    print("Wichtig: Dieses Script erstellt eine neue config.json")
    config = {}
    config['token'] = input("Dein Bot Token: ")
    config['prefix'] = input("Dein Bot Prefix: ")
    config["riotapi"] = input("Dein Riot Games Api Token: ")
    config["osuapi"] = input("Dein Osu Api Token: ")
    with open('config.json', 'w+') as file:
        json.dump(config, file, indent=2)


start()
