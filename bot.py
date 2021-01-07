import asyncio
import discord
import discord.ext
from discord.ext import commands
import json
import random
import requests
import os
from riotwatcher import LolWatcher, ApiError


# Wichs Codierung
# ä=Ã¼
# ö=Ã¶


os.system("git pull https://github.com/antonstech/simplediscordbot")


def start():
    tokengesetzt = input("Ist dein Token gesetzt? (j/n) ")
    if tokengesetzt == "j":
        pass
    else:
        bottoken = {"token": input("Dein Bot Token: ")}
        with open("token.json", "w") as f:
            json.dump(bottoken, f)

    prefixgesetzt = input("Ist dein Bot Prefix gesetzt? (j/n) ")
    if prefixgesetzt == "j":
        pass
    else:
        botprefix = {"prefix": input("Dein Bot Prefix: ")}
        with open("prefix.json", "w") as f:
            json.dump(botprefix, f)


with open('./prefix.json', 'r') as f:
    json_stuff = json.load(f)
    prefix = json_stuff["prefix"]

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

start()


@client.event
async def on_ready():
    print("Yess der bot läuft :)".format(client))
    print("Du bist eingeloggt als {0.user} auf discord.py Version {1}".format(client, discord.__version__))
    print("Der Bot ist zurzeit auf folgenden Server:")
    for guild in client.guilds:
        print("-" + guild.name)
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("SimpleBot by antonstech"), status=discord.Status.online)
        await asyncio.sleep(360)
        await client.change_presence(activity=discord.Game("Moin Meister"), status=discord.Status.online)
        await asyncio.sleep(360)


# Benutzerinfo
def benutzerinfo():
    @client.command()
    async def benutzerinfo(ctx, member: discord.Member):
        embed = discord.Embed(title='Benutzerinfo für {}'.format(member.name),
                              description='Benutzerinfo für {}'.format(
                                  member.mention),
                              color=0x69E82C)
        embed.add_field(name='Server beigetreten',
                        value=member.joined_at.strftime('%d/%m/%Y'),
                        inline=True)
        embed.add_field(name='Discord beigetreten',
                        value=member.created_at.strftime('%d/%m/%Y'),
                        inline=True)
        embed.add_field(name=f"Rollen ({len(member.roles)})", value=" ".join([role.mention for role in member.roles]))

        rollen = ''
        for role in member.roles:
            if not role.is_default():
                rollen += '{} \r\n'.format(role.mention)
        embed.add_field(name='Höchste Rolle', value=member.top_role.mention, inline=True),
        embed.add_field(name="Benutzer ID", value=member.id, inline=True),
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text='Benutzerinfo')
        await ctx.send(embed=embed)


benutzerinfo()


def wetter():
    api_key = "7d518678abe248fc7de360ba82f9375b"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    @client.command()
    async def wetter(ctx, *, city: str):
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang=de"
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                derzeitige_temperatur = y["temp"]
                derzeitige_temperatur_celsius = str(round(derzeitige_temperatur - 273.15))
                druck = y["pressure"]
                luftfeuchtigkeit = y["humidity"]
                fuehlt_sich_an_wie = y["feels_like"]
                fuehlt_sich_an_wie_celsius = str(round(fuehlt_sich_an_wie - 273.15))
                z = x["weather"]
                wetter_beschreibung = z[0]["description"]
                embed = discord.Embed(title=f"Wetter in {city_name}",
                                      color=ctx.guild.me.top_role.color,
                                      timestamp=ctx.message.created_at, )
                embed.add_field(name="Beschreibung", value=f"**{wetter_beschreibung}**", inline=False)
                embed.add_field(name="Temperatur(C)", value=f"**{derzeitige_temperatur_celsius}°C**", inline=False)
                embed.add_field(name="Fühlt sich an wie(C)", value=f"**{fuehlt_sich_an_wie_celsius}°C**", inline=False)
                embed.add_field(name="Luftfeuchtigkeit(%)", value=f"**{luftfeuchtigkeit}%**", inline=False)
                embed.add_field(name="Luftdruck(hPa)", value=f"**{druck}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_footer(text=f"Angefragt von {ctx.author.name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Stadt wurde nicht gefunden.")


wetter()


# Ping
@client.command(invoke_without_command=True)
async def ping(ctx):
    await ctx.send("Der Ping beträgt derzeit " f"{round(client.latency * 1000)}ms")


def clear():
    def ist_gepinnt(mess):
        return not mess.pinned

    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1, check=ist_gepinnt)

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("Du hast keine Berechtigung dazu!")


clear()


def hilfe():
    @client.group(invoke_without_command=True)
    async def hilfe(ctx):
        embed = discord.Embed(title="Hilfe",
                              description="Benutze hilfe (command) für mehr Informationen zu einem Command.",
                              color=ctx.author.color)
        embed.add_field(name="Moderation:", value="clear")
        embed.add_field(name="nützlich:", value="wetter, benutzerinfo , ping")
        embed.add_field(name="fun", value="give")
        embed.set_footer(text='Bei sonstigen Fragen einfach DCGALAXY#9729 anschreiben')
        await ctx.send(embed=embed)

    @hilfe.command()
    async def wetter(ctx):
        embed = discord.Embed(title="clear",
                              description="Mit wetter kannst du dir das Wetter so wie einige Infos dazu anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="wetter (Stadt)")
        embed.add_field(name="Beispiel:", value="wetter München")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def clear(ctx):
        embed = discord.Embed(title="wetter",
                              description="Mit clear kannst du eine beliebige Anzahl an Nachrichten aus einem Channel löschen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="clear (Anzahl)")
        embed.add_field(name="Beispiel:", value="clear 15")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def benutzerinfo(ctx):
        embed = discord.Embed(title="benutzerinfo",
                              description="Mit benutzerinfo kannst du dir einige Infos über einen Nutzer anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="benutzerinfo (Benutzer)")
        embed.add_field(name="Beispiel:", value="benutzerinfo DCGALAXY")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def ping(ctx):
        embed = discord.Embed(title="ping",
                              description="Mit ping kannst du dir die Discord WebSocket protocol latency anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="ping")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def give(ctx):
        embed = discord.Embed(title="ping",
                              description="Mit give wird eine Minecraft Konsole simuliert",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="give (item) (spieler)")
        await ctx.send(embed=embed)


hilfe()


def give():
    @client.group(invoke_without_command=True)
    async def give(ctx):
        embed = discord.Embed(title="Minecraft Konsole",
                              description="gieb das Item und dann den Discord Namen ein".format(),
                              colour=ctx.author.color)
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/top-crop/width/300/height/300?cb=20190903234415")
        await ctx.send(embed=embed)

    @give.command()
    async def diamonds(ctx, member: discord.Member):
        randomnum = random.randint(0, 64)
        embed = discord.Embed(title="Minecraft Konsole",
                              description="`/give {0} minecraft:diamonds {1}`".format(member.name, randomnum),
                              colour=ctx.author.color)
        embed.set_thumbnail(url="https://freepngimg.com/thumb/minecraft/11-2-minecraft-diamond-png.png")
        await ctx.send(embed=embed)

    @give.command()
    async def schwert(ctx, member: discord.Member):
        randomnum = random.randint(0, 64)
        embed = discord.Embed(title="Minecraft Konsole",
                              description="`/give {0} minecraft:diamond_sword {1}`".format(member.name, randomnum),
                              colour=ctx.author.color)
        embed.set_thumbnail(url="https://assets.stickpng.com/images/580b57fcd9996e24bc43c301.png")
        await ctx.send(embed=embed)

    @give.command()
    async def opgoldapfel(ctx, member: discord.Member):
        randomnum = random.randint(0, 64)
        embed = discord.Embed(title="Minecraft Konsole",
                              description="`/give {0} enchanted_golden_apple {1}`".format(member.name, randomnum),
                              colour=ctx.author.color)
        embed.set_thumbnail(
            url="https://static.wikia.nocookie.net/hypixel-skyblock/images/4/4d/Enchanted_Golden_Apple.gif/revision/latest/smart/width/200/height/200?cb=20200619230630")
        await ctx.send(embed=embed)


give()

with open('token.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

client.run(token)
