import asyncio
import json
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

default_prefix = constants.bot_prefix


def get_default_prefix(client, message):
    with open("config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.AutoShardedBot(command_prefix=get_default_prefix, intents=discord.Intents.all())
client.remove_command('help')


def tokenchecker():
    riotapi = constants.lol_token
    base_riot_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/DCGALAXY?api_key="
    rioturl = base_riot_url + riotapi
    response = requests.get(rioturl)
    if response.status_code == 200:
        pass
    else:
        print("The Riot-API Key does not work :((")
        print(
            "Please check if the key in config.json is set correctly and look at "
            "https://developer.riotgames.com/api-status/ to see if it is not perhaps due to Riot itself")
        riotnotworkingexe = input("Do you still want to start? (y/n): ")
        if riotnotworkingexe == "y":
            pass
        else:
            raise Exception("The Riot-API Key does not work.")

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
    print("Yess the Bot is running :)".format(client))
    print("You have installed Release " + str(VERSION))
    print("You are logged in as {0.user} via discord.py Version {1}".format(client, discord.__version__))
    if os.path.exists("config/mysql.json"):
        print("MySQL-Logging ist ACTIVATED")
    else:
        print("MySQL-Logging ist DEACTIVATED")
    print("The Bot is on the following " + str(len(client.guilds)) + " Servers:")
    for guild in client.guilds:
        print("- " + str(guild.name))
    if os.path.exists("temp/guildlist.json"):
        pass
    else:
        try:
            os.mkdir("temp")
        except:
            pass
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

    if os.path.exists("config/prefixes.json"):
        pass
    else:
        with open("config/prefixes.json", "w") as f:
            f.write("{}")
        with open("config/prefixes.json") as thejsonfile:
            prefixes = json.load(thejsonfile)

        for guild in client.guilds:
            prefixes[str(guild.id)] = default_prefix

        with open("config/prefixes.json", "w") as thejsonfile:
            json.dump(prefixes, thejsonfile, indent=2)
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("https://git.io/antonsbot"),
                                     status=discord.Status.online)
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game(f"antonstechbot on Version {VERSION}"))
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Game(default_prefix + "help on " + str(len(client.guilds)) + " Servers"))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game("ein heißes Spiel mit der Stiefschwester"))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(f"with {len(set(client.get_all_members()))} Dudes"))
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="your Messages"))
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
            await ctx.channel.send("Only the Owner can use this Command!")

    return wrapper


@client.command(name="reload")
async def reload_cog(ctx, cogName):
    info = await client.application_info()
    if ctx.author.id == info.owner.id:
        if cogName == "*":
            for cogreloadfilename in os.listdir("./cogs"):
                if cogreloadfilename.endswith(".py") and cogreloadfilename not in ["errorstuff.py"]:
                    client.reload_extension(f"cogs.{cogreloadfilename[:-3]}")
            await ctx.send("Successfully reloaded all extensions!")
        else:
            try:
                client.reload_extension(f"cogs.{cogName}")
                await ctx.send(f"Successfully reloaded extension {cogName}!")
            except:
                await ctx.channel.send(
                    f"While trying to reload the extension {cogName} something went wrong!")
    else:
        await ctx.channel.send("Only the Owner of the Bot can use this Command")


@client.command(name="unload")
@owner_only
async def unload_cog(ctx, cogName):
    try:
        client.unload_extension(f"cogs.{cogName}")
        await ctx.channel.send(f"Successfully unloaded extension {cogName}!")
    except Exception as e:
        await ctx.channel.send(f"Error, either the extension is already unloaded, or it was not found!")


@client.command(name="load")
@owner_only
async def load_cog(ctx, cogName):
    try:
        client.load_extension(f"cogs.{cogName}")
        await ctx.channel.send(f"Successfully loaded extension {cogName}!")
    except Exception as e:
        await ctx.channel.send(f"Error, either the extension is already loaded or it was not found.")


with open('config/config.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

# load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename not in ["errorstuff.py"]:
        client.load_extension(f"cogs.{filename[:-3]}")
print("All Extensions loaded!")


client.run(token)