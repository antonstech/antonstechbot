import asyncio
import json
import time

import discord
import discord.ext
import requests
from discord.ext import commands
import os

from botlibrary.utils import get_variable
from botlibrary import constants

# Wichs Codierung
# ä=Ã¼
# ö=Ã¶

# assign constant variables
constants.assignVariables()

VERSION = constants.VERSION

bot_prefix = constants.bot_prefix

client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())


def tokenchecker():
    riotapi = constants.lol_token
    base_riot_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/DCGALAXY?api_key="
    rioturl = base_riot_url + riotapi
    response = requests.get(rioturl)
    if response.status_code == 200:
        pass
    else:
        print("Der Riot-API Key hat nicht funktioniert :((")
        print(
            "Bitte checke ob der Key in der config.json richtig gesetzt ist und schau auf "
            "https://developer.riotgames.com/api-status/ nach ob es nicht vllt an Riot selber liegt")
        riotnotworkingexe = input("Willst du trotzdem starten? (j/n): ")
        if riotnotworkingexe == "j":
            pass
        else:
            raise Exception("Der Riot-API Key hat nicht funktioniert.")

    osuapi = constants.osu_token
    base_osu_url = "https://osu.ppy.sh/api/get_user_best?u=Aftersh0ock&k="
    osuurl = base_osu_url + osuapi
    osuresponse = requests.get(osuurl)
    if osuresponse.status_code == 200:
        pass
    else:
        print("Der Osu-API Key hat nicht funktioniert :((")
        print(
            "Bitte checke ob der Key in der config.json richtig gesetzt ist und schau auf https://status.ppy.sh nach ob es nicht vllt an Osu selber liegt")
        osunotworkingexe = input("Willst du trotzdem starten? (j/n): ")
        if osunotworkingexe == "j":
            pass
        else:
            raise Exception("Der Osu-API Key hat nicht funktioniert.")
    token = constants.bot_token
    headers = {
        "Authorization": "Bot " + token
    }
    response = requests.get('https://discordapp.com/api/v8/auth/login', headers=headers)
    if response.status_code == 200:
        pass
    else:
        raise Exception("Der Discord Bot Token funktioniert nicht!")
    ipdata = constants.ipdata_token
    baseipurl = "https://api.ipdata.co/8.8.8.8"
    ipurl = baseipurl + "?api-key=" + ipdata
    ipresponse = requests.get(ipurl)
    if ipresponse.status_code == 200:
        pass
    else:
        print("Der IPData-API Key hat nicht funktioniert :((")
        print(
            "Bitte checke ob der Key in der config.json richtig gesetzt ist und schau auf https://status.ipdata.co nach ob es nicht vllt an Osu selber liegt")
        ipdatanotworkingexe = input("Willst du trotzdem starten? (j/n): ")
        if ipdatanotworkingexe == "j":
            pass
        else:
            raise Exception("Der IPData Key hat nicht funktioniert.")
    url = constants.coc_url
    headers = {"Authorization": "Bearer " + constants.coc_token}
    cocresponse = requests.get(url, headers=headers)
    if cocresponse.status_code == 200:
        pass
    else:
        print("Der Coc API Token hat nicht funktioniert :((")
        print(
            "Bitte checke ob der Token in der config.json richtig gesetzt ist und schau nach ob es nicht vllt an Supercell selber liegt")
        cocnotworkingexe = input("Willst du trotzdem starten? (j/n): ")
        if cocnotworkingexe == "j":
            pass
        else:
            raise Exception("Der CoC API-Key hat nicht funktioniert.")


tokenchecker()


@client.event
async def on_ready():
    global guild
    print("Yess der bot läuft :)".format(client))
    print("Du hast derzeit Release " + str(VERSION) + " installiert")
    print("Du bist eingeloggt als {0.user} auf discord.py Version {1}".format(client, discord.__version__))
    if os.path.exists("config/mysql.json"):
        print("MySQL-Logging ist AKTIVIERT")
    else:
        print("MySQL-Logging ist DEAKTIVIERT")
    print("Der Bot ist zurzeit auf folgenden " + str(len(client.guilds)) + " Servern:")
    for guild in client.guilds:
        print("- " + str(guild.name))
    if os.path.exists("temp/guildlist.json"):
        pass
    else:
        os.mkdir("temp")
        newjsonfile = open("temp/guildlist.json", "w")
        newjsonfile.write("{}")
        newjsonfile.close()
    with open("temp/guildlist.json") as thejsonfile:
        file = json.load(thejsonfile)

    for guild in client.guilds:
        try:
            if file[str(guild.id)]:
                continue
        except KeyError:
            pass

        file[str(guild.id)] = False

    with open("temp/guildlist.json", "w") as thejsonfile:
        json.dump(file, thejsonfile, indent=2)
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("https://git.io/antonsbot"),
                                     status=discord.Status.online)
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game(f"antonstechbot auf Version {VERSION}"))
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Game(bot_prefix + "hilfe auf " + str(len(client.guilds)) + " Servern"))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game("ein heißes Spiel mit der Stiefschwester"))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(f"mit {len(set(client.get_all_members()))} Leuten"))
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="auf deine Nachrichten"))
        await asyncio.sleep(60)

"""
##############################################################################################################################################################
                                                            Ole rewrite paradise
                                                            https://github.com/DestinyofYeet <3
##############################################################################################################################################################
"""


def owner_only(func):
    async def wrapper(self, *args, **kwargs):
        ctx = get_variable('ctx')
        info = await client.application_info()
        if ctx.author.id == info.owner.id:
            return await func(self, *args, **kwargs)
        else:
            await ctx.channel.send("Nur der Owner kann diesen Command benutzen!")

    return wrapper


@client.command(name="reload")
@owner_only
async def reload_cog(ctx, cogName):
    try:
        await unload_cog(ctx, cogName)
        await load_cog(ctx, cogName)
    except Exception as e:
        await ctx.channel.send(f"Während dem versuch die Erweiterung {cogName} neu zu laden ist etwas schiefgelaufen!")


@client.command(name="unload")
@owner_only
async def unload_cog(ctx, cogName):
    try:
        client.unload_extension(f"cogs.{cogName}")
        await ctx.channel.send(f"Erfolgreich erweiterung {cogName} entladen!")
    except Exception as e:
        await ctx.channel.send(f"Fehler, entweder ist die erweiterung schon entladen, oder sie wurde nicht gefunden!")


@client.command(name="load")
@owner_only
async def load_cog(ctx, cogName):
    try:
        client.load_extension(f"cogs.{cogName}")
        await ctx.channel.send(f"Erfolgreich erweiterung {cogName} geladen!")
    except Exception as e:
        await ctx.channel.send(f"Fehler, entweder ist die erweiterung schon geladen, oder sie wurde nicht gefunden.")


with open('config/config.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

# load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename not in ["errorstuff.py"]:
        client.load_extension(f"cogs.{filename[:-3]}")

# run bot
client.run(token)
