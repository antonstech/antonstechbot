import asyncio
import json
import random
import subprocess
import discord
import discord.ext
import requests
from discord.ext import commands
from riotwatcher import LolWatcher
import datetime
import mysql.connector
import urllib
from urllib import parse
import os

# Wichs Codierung
# ä=Ã¼
# ö=Ã¶

VERSION = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()

with open('./config.json', 'r') as f:
    json_stuff = json.load(f)
    prefix = json_stuff["prefix"]

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


def tokenchecker():
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        riotapi = json_stuff["riotapi"]
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

    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        osuapi = json_stuff["osuapi"]
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
    with open('config.json', 'r') as f:
        json_stuff = json.load(f)
        token = json_stuff["token"]
    headers = {
        "Authorization": "Bot " + token
    }
    response = requests.get('https://discordapp.com/api/v8/auth/login', headers=headers)
    if response.status_code == 200:
        pass
    else:
        raise Exception("Der Discord Bot Token funktioniert nicht!")
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        ipdata = json_stuff["ipdata"]
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


tokenchecker()


@client.event
async def on_ready():
    print("Yess der bot läuft :)".format(client))
    print("Du hast derzeit Release " + str(VERSION) + " installiert")
    print("Du bist eingeloggt als {0.user} auf discord.py Version {1}".format(client, discord.__version__))
    if os.path.exists("mysql.json"):
        print("MySQL-Logging ist AKTIVIERT")
    else:
        print("MySQL-Logging ist DEAKTIVIERT")
    print("Der Bot ist zurzeit auf folgenden " + str(len(client.guilds)) + " Servern:")
    for guild in client.guilds:
        print("-" + str(guild.name))
    client.loop.create_task(status_task())


with open('./config.json', 'r') as f:
    json_stuff = json.load(f)
    prefix = json_stuff["prefix"]


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("https://git.io/antonsbot"),
                                     status=discord.Status.online)
        await asyncio.sleep(60)
        await client.change_presence(
            activity=discord.Game(prefix + "corona auf " + str(len(client.guilds)) + " Servern"))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game("ein heißes Spiel mit der Stiefschwester"))
        await asyncio.sleep(5)
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="auf deine Nachrichten"))
        await asyncio.sleep(60)


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
        embed.add_field(name=f"Rollen ({len(member.roles)})",
                        value=" ".join([role.mention for role in member.roles]))

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
                symbol = z[0]["icon"]
                wetter_beschreibung = z[0]["description"]
                embed = discord.Embed(title=f"Wetter in {city_name}",
                                      color=ctx.guild.me.top_role.color,
                                      timestamp=ctx.message.created_at, )
                embed.add_field(name="Beschreibung", value=f"**{wetter_beschreibung}**", inline=False)
                embed.add_field(name="Temperatur(C)", value=f"**{derzeitige_temperatur_celsius}°C**", inline=False)
                embed.add_field(name="Fühlt sich an wie(C)", value=f"**{fuehlt_sich_an_wie_celsius}°C**",
                                inline=False)
                embed.add_field(name="Luftfeuchtigkeit(%)", value=f"**{luftfeuchtigkeit}%**", inline=False)
                embed.add_field(name="Luftdruck(hPa)", value=f"**{druck}hPa**", inline=False)
                embed.set_thumbnail(url="http://openweathermap.org/img/wn/" + symbol + ".png")
                embed.set_footer(text=f"Angefragt von {ctx.author.name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Stadt wurde nicht gefunden.")


wetter()


def LeagueofLegendsstats():
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        riotapi = json_stuff["riotapi"]
    api_key = riotapi
    base_url = "https://euw1.api.riotgames.com/lol/"

    @client.group(invoke_without_command=True)
    async def lol(ctx):
        embed = discord.Embed(title="League of Legends Statistiken", color=ctx.author.color)
        embed.add_field(name="Alle Befehle:", value="Mach help lol um dir alle Befehle anzeigen zu lassen",
                        inline=False)
        embed.set_thumbnail(
            url="https://www.riotgames.com/darkroom/original/462106d7bcc8d74a57a49411b70c4a92"
                ":d4bed097ee383e5afad037edb5e5786e/lol-logo-rendered-hi-res.png")
        embed.set_footer(text='antonstech/antonstechbot ({})'.format(VERSION), icon_url='https://i.imgur.com'
                                                                                        '/gFHBoZA.png')
        await ctx.send(embed=embed)

    @lol.command()
    async def level(ctx, *, name: str):
        spielername = name
        complete_url = base_url + "summoner/v4/summoners/by-name/" + spielername + "?api_key=" + api_key
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if 0 < x["summonerLevel"] < 3000:
            async with channel.typing():
                y = x
                spielerlevel = y["summonerLevel"]
                profilbild = y["profileIconId"]
                embed = discord.Embed(title=f"Leauge of Legends Statistiken für {spielername}",
                                      color=ctx.author.color,
                                      timestamp=ctx.message.created_at, )
                embed.add_field(name="Level des Spielers:", value=f"**{spielerlevel}**", inline=False)
                embed.set_thumbnail(
                    url='http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/' + str(profilbild) + '.png')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Spieler wurde nicht gefunden.")

    @lol.command()
    async def rang(ctx, *, name: str):
        spielername = name
        channel = ctx.message.channel
        try:
            lol_watcher = LolWatcher(api_key)
            my_region = 'euw1'
            me = lol_watcher.summoner.by_name(my_region, spielername)
            my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
            async with channel.typing():
                if my_ranked_stats:
                    data = my_ranked_stats[0]
                    rang = data["tier"]
                    nummer = data["rank"]
                    punkte = data["leaguePoints"]
                    gewonnen = data["wins"]
                    verloren = data["losses"]
                    neu_in_der_elo = data["freshBlood"]
                    winrate = gewonnen / (gewonnen + verloren) * 100
                    embed = discord.Embed(title=f"Leauge of Legends Ranked Statistiken für {spielername}",
                                          color=ctx.author.color,
                                          timestamp=ctx.message.created_at, )
                    embed.add_field(name="Rang", value=f"{rang} {nummer}", inline=True)
                    embed.add_field(name="Punkte", value=f"{punkte}", inline=True)
                    embed.add_field(name="Neu in der Elo?", value=f"{neu_in_der_elo}", inline=True)
                    embed.add_field(name="Gewonnen:", value=f"{gewonnen}", inline=True)
                    embed.add_field(name="Verloren:", value=f"{verloren}", inline=True)
                    embed.add_field(name="Winrate", value=f"{winrate.__round__()}%", inline=True)
                    embed.set_thumbnail(url="https://antonstech.de/" + str(rang) + ".png")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Spieler nicht gefunden oder nicht eingeranked.")
        except:
            await ctx.send("Spieler nicht gefunden oder nicht eingeranked.")


LeagueofLegendsstats()


def mc():
    base_url = "https://api.mcsrvstat.us/2/"

    @client.group(invoke_without_command=True)
    async def mc(ctx):
        embed = discord.Embed(title="Der Mc Command kann dir viele Nützliche Dinge zum Thema Minecraft anzeigen")
        embed.add_field(name="Funktionen:", value="skin, server, name")
        await ctx.send(embed=embed)

    @mc.command()
    async def server(ctx, *, adresse: str):
        complete_url = base_url + adresse
        response = requests.get(complete_url)
        channel = ctx.message.channel
        x = response.json()
        async with channel.typing():
            status = x["online"]
            embed = discord.Embed(title="Minecraft Server Stats für " + adresse)
            if status is True:
                try:
                    modt = x["motd"]
                    beschreibung = modt["clean"]
                    modtbeschreibung = beschreibung[0]
                    spieler = x["players"]
                    spieleronline = spieler["online"]
                    slots = spieler["max"]
                    embed.add_field(name="Beschreibung", value=f"{modtbeschreibung}")
                    embed.add_field(name="Spieler", value=f"{spieleronline} / {slots}")
                    try:
                        version = x["version"]
                        software = x["software"]
                        embed.add_field(name="Version", value=f"{software} {version}")
                    except:
                        embed.add_field(name="Version", value="Info nicht vorhanden")
                    try:
                        mods = x["mods"]
                        modss = mods["names"]
                        if modss != "":
                            embed.set_author(name="Modlist",
                                             url='https://mcsrvstat.us/server/' + adresse)
                            embed.add_field(name="Modlist", value="Siehe oben links")
                        else:
                            pass
                    except:
                        pass
                    embed.add_field(name="Online?", value="Jap")
                    embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/" + adresse)
                    await ctx.send(embed=embed)
                except:
                    embed.add_field(name="Test", value="Test123")
                    await ctx.send(embed=embed)
            else:
                embed.set_footer(text="Der Server ist derzeit nicht online")
                await ctx.send(embed=embed)

    @mc.command()
    async def skin(ctx, name):
        uuid = "https://api.mojang.com/users/profiles/minecraft/" + name
        response = requests.get(uuid)
        x = response.json()
        playeruuid = x["id"]
        kopf = "https://crafatar.com/avatars/"
        body = "https://crafatar.com/renders/body/"
        embed = discord.Embed(title="Minecraft Skin von " + name)
        embed.set_thumbnail(url=kopf + playeruuid + "?size=50")
        embed.set_image(url=body + playeruuid + "?size=512")
        embed.set_author(name="Skin Download", url="https://minotar.net/download/" + name)
        await ctx.send(embed=embed)

    @mc.command()
    async def name(ctx, name):
        embed = discord.Embed(title="Minecraft Namehistory für " + name)
        try:
            uuid = "https://api.mojang.com/users/profiles/minecraft/" + name
            response = requests.get(uuid)
            x = response.json()
            playeruuid = x["id"]
            namehistory = "https://api.mojang.com/user/profiles/" + playeruuid + "/names"
            response2 = requests.get(namehistory)
            y = response2.json()
            try:
                namen = y[0]["name"]
                embed.add_field(name="Namensänderung:", value=f"**{namen}** --> **{name}**")
            except:
                pass
        except:
            embed.add_field(name="Spieler Nicht gefunden",
                            value="Schau mal nach ob du alles richtig geschrieben hast. Und falls es dann immernoch "
                                  "nicht geht Kontaktier bitte den Entwickler des Bots")
        await ctx.send(embed=embed)


mc()


def corona():
    @client.group(invoke_without_command=True)
    async def corona(ctx):
        url = "https://api.corona-zahlen.org/germany"
        response = requests.get(url)
        x = response.json()
        g_url = "https://api.corona-zahlen.org/vaccinations"
        geimpft = requests.get(g_url)
        y = geimpft.json()
        channel = ctx.message.channel
        async with channel.typing():
            insgesamt = x["cases"]
            todegesamt = x["deaths"]
            inzidenz = x["weekIncidence"]
            data = y["data"]
            jetzgeimpft = data["quote"]
            infor = x["r"]
            rwert = infor["value"]
            gesund = x["recovered"]
            embed = discord.Embed(title="Impfen lassen", url="https://antonstech.de/impfung.html",
                                  color=ctx.author.color)
            await ctx.send(embed=embed)
            embed = discord.Embed(title="Corona Virus Statistiken für Deutschland",
                                  color=ctx.author.color,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name="Fälle insgesammt", value=f"{insgesamt}")
            embed.add_field(name="Tode insgesamt", value=f"{todegesamt}")
            embed.add_field(name="Gesund", value=f"{gesund}")
            embed.add_field(name="Inzidenz", value=f"{inzidenz.__round__()}")
            embed.add_field(name="Geimpft", value=f"{jetzgeimpft.__round__(3) * 100}%")
            embed.add_field(name="R-Wert", value=f"{rwert}")
            embed.set_footer(text="Mit " + prefix + "corona geimpft gibts mehr zur Impfung")
            await ctx.send(embed=embed)
            embed = discord.Embed(title="Aktuelle Corona Map für Deutschland",
                                  color=ctx.author.color,
                                  timestamp=ctx.message.created_at)
            embed.set_image(url="https://api.corona-zahlen.org/map/districts")
            embed.set_footer(text="Mit " + prefix + "corona geimpft gibts mehr zur Impfung")
            await ctx.send(embed=embed)

    @corona.command(invoke_without_command=True)
    async def geimpft(ctx):
        url = "https://api.corona-zahlen.org/vaccinations"
        response = requests.get(url)
        x = response.json()
        channel = ctx.message.channel
        async with channel.typing():
            y = x["data"]
            jetztgeimpft = y["quote"]
            gesamt = y["vaccinated"]
            second = y["secondVaccination"]
            zweite_imfung = second["vaccinated"]
            embed = discord.Embed(title="Impfen lassen", url="https://antonstech.de/impfung.html",
                                  color=ctx.author.color)
            await ctx.send(embed=embed)
            embed = discord.Embed(title="Statistiken zur Impfung in Deutschland",
                                  color=ctx.author.color)
            embed.add_field(name="Prozent der Bevölkerung", value=f"{jetztgeimpft.__round__(3) * 100}%")
            embed.add_field(name="Anzahl der Geimpften", value=f"{gesamt} Personen", inline=False)
            embed.add_field(name="Zweite Impfung haben bereits erhalten", value=f"{zweite_imfung} Personen")
            await ctx.send(embed=embed)


corona()


def osu():
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        osuapi = json_stuff["osuapi"]
        url = "https://osu.ppy.sh/api/get_user?u="

    @client.command()
    async def osu(ctx, name):
        try:
            spielerstats = url + name + "&k=" + osuapi
            response = requests.get(spielerstats)
            x = response.json()
            y = x[0]
            userid = y["user_id"]
            playedgames = y["playcount"]
            level = y["level"]
            levelgerundet = (int(float(level)))
            spielzeit_sekunden = y["total_seconds_played"]
            spielzeit_stunden = int(spielzeit_sekunden) / 3600
            genauigkeit = y["accuracy"]
            genauigkeit_int = (int(float(genauigkeit)))
            globalrank = y["pp_rank"]
            localrank = y["pp_country_rank"]
            land = y["country"]
            embed = discord.Embed(title="Osu Stats für " + name)
            embed.set_thumbnail(url="http://s.ppy.sh/a/" + userid)
            embed.add_field(name="Gespielte Spiele", value=f"{playedgames}")
            embed.add_field(name="Level", value=f"{levelgerundet}")
            embed.add_field(name="Spielzeit", value=f"{(int(float(spielzeit_stunden)))} Stunden")
            embed.add_field(name="Genauigkeit", value=f"{genauigkeit_int.__round__()}%")
            embed.add_field(name="Globaler Rang", value=f"{globalrank}")
            embed.add_field(name="Rang in " + land, value=f"{localrank}")
            await ctx.send(embed=embed)
        except:
            await ctx.send(
                "Irgendetwas ist schief gelaufen; check ob der Name richtig geschrieben ist und falls es dann nicht geht Kontaktiere DCGALAXY#9729")


osu()


def earth2():
    @client.command()
    async def earth2(ctx):
        url = "https://earth2stats.net/api/get_countries/199"
        response = requests.get(url)
        x = response.json()
        land = x["name"]
        wert = x["marketplace_tile_value"]
        verkauft = x["total_sold_tiles"]
        embed = discord.Embed(title="Earth2 Statistiken für " + land, url="https://earth2stats.net/country/" + land)
        embed.set_thumbnail(
            url="https://static-cdn.jtvnw.net/jtv_user_pictures/99783da2-3f60-4aeb-92bd-83e953c03627-profile_image-70x70.png")
        embed.add_field(name="Wert eines Tiles", value=f"{wert}E$")
        embed.add_field(name="Insgesamt verkauft", value=f"{verkauft} Tiles")
        await ctx.send(embed=embed)


earth2()


def anime():
    @client.command()
    async def anime(ctx):
        base_url = "https://trace.moe/api/search?url="
        attachment = ctx.message.attachments[0]
        attachementurl = attachment.url
        url = base_url + attachementurl
        response = requests.post(url)
        x = response.json()
        y = x["docs"][0]
        genauigkeit = y["similarity"]
        hentai = y["is_adult"]
        titel = y["title_english"]
        nativetitel = y["title_native"]
        anilist = y["anilist_id"]
        filename = y["filename"]
        at = y["at"]
        tokenthumb = y["tokenthumb"]
        ### Coming Soon
        filenameencoded = urllib.parse.quote(filename)
        imgrequest = "https://media.trace.moe/image/" + str(anilist) + "/" + filenameencoded + "?t=" + str(
            at) + "&token=" + tokenthumb + "&size=m"
        ###
        if titel != None:
            embed = discord.Embed(title=f"{titel}")
        else:
            embed = discord.Embed(title=f"{nativetitel}")
        anilisturl = "https://anilist.co/anime/" + str(anilist)
        embed.set_author(name="Anilist Link", url=anilisturl)
        embed.add_field(name="Genauigkeit", value=f"{(genauigkeit * 100).__round__()}%")
        if hentai == False:
            embed.add_field(name="Hentai?", value="Nope :(")
        else:
            embed.add_field(name="Hentai?", value="Yess Sir")
        if titel != None:
            embed.add_field(name="Titel in Orginalsprache", value=f"{nativetitel}")
        else:
            pass
        embed.set_image(url=str(imgrequest))
        await ctx.send(embed=embed)


anime()


def ipdata():
    with open('./config.json', 'r') as f:
        json_stuff = json.load(f)
        ipdata = json_stuff["ipdata"]
        url = "https://api.ipdata.co/"

    @client.command()
    async def ip(ctx, ip):
        apiurl = "?api-key=" + ipdata
        resulturl = url + ip + apiurl
        response = requests.get(resulturl)
        x = response.json()
        city = x["city"]
        country = x["country_name"]
        flag = x["flag"]
        y = x["asn"]
        asn = y["name"]
        asntype = y["type"]
        postleitzahl = x["postal"]
        kontinent = x["continent_name"]
        embed = discord.Embed(title="IP Informationen zu " + ip)
        embed.set_thumbnail(url=flag)
        embed.add_field(name="Land", value=f"{country}")
        embed.add_field(name="Stadt", value=f"{city}")
        embed.add_field(name="Kontinent", value=f"{kontinent}")
        if postleitzahl == None:
            pass
        else:
            embed.add_field(name="Postleitzahl", value=f"{postleitzahl}")
        embed.add_field(name="Internetanbieter", value=f"{asn}")
        embed.add_field(name="Anbiter-Type", value=f"{asntype}")
        await ctx.send(embed=embed)


ipdata()


@client.command(invoke_without_command=True)
async def ping(ctx):
    await ctx.send("Der Ping beträgt derzeit " f"{round(client.latency * 1000)}ms")


@client.command(invoke_without_command=True)
async def version(ctx):
    await ctx.send(
        "Der Bot läuft derzeit auf Release " + str(VERSION) + " und geht auch dank discord.py Version {}".format(
            discord.__version__))


@client.command(invite_without_command=True)
async def einladen(ctx):
    embed = discord.Embed()
    embed.set_author(name="Klicke hier zum einladen",
                     url='https://discord.com/api/oauth2/authorize?client_id=744218316167708773&permissions=8&scope=bot')
    await ctx.send(embed=embed)


@client.command(invite_without_command=True)
async def hosten(ctx):
    embed = discord.Embed()
    embed.set_author(name="Klicke hier um ein Tutorial zum Selber hosten zu bekommen",
                     url='https://github.com/antonstech/antonstechbot/wiki/Installation')
    await ctx.send(embed=embed)


@client.command(invite_without_command=True)
async def code(ctx):
    embed = discord.Embed()
    embed.set_author(name="Hier findest du den ganzen Code vom Bot",
                     url='https://github.com/antonstech/antonstechbot')
    await ctx.send(embed=embed)


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


@client.command()
async def nudes(ctx):
    if ctx.channel.is_nsfw():
        embed = discord.Embed(title="Nudes")
        embed.set_image(
            url="https://www.nydailynews.com/resizer/OYta-jTp2D6Xt_Wj_o6zEUqWttE=/415x562/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/7Y53KJVE7FGLZZPD44LTN4QB5I.jpg")
        await ctx.send(embed=embed)
    else:
        await ctx.channel.send("Der Channel ist nicht nsfw")


def hilfe():
    @client.group(invoke_without_command=True)
    async def hilfe(ctx):
        embed = discord.Embed(title="Hilfe",
                              description="Benutze " + prefix + "hilfe (command) für mehr Informationen zu einem Command.",
                              color=ctx.author.color)
        embed.add_field(name="Moderation:", value="clear")
        embed.add_field(name="nützlich:", value="wetter, benutzerinfo , ping, anime", inline=True)
        embed.add_field(name="fun", value="give, corona, earth2", inline=True)
        embed.add_field(name="Game-Stats", value="lol, osu", inline=True)
        embed.add_field(name="Minecraft Zeugs", value="mc", inline=True)
        embed.add_field(name="Infos zum Bot", value="version, einladen, hosten, code", inline=True)
        embed.set_footer(text='Bei sonstigen Fragen einfach DCGALAXY#9729 anschreiben')
        await ctx.send(embed=embed)

    @hilfe.command()
    async def wetter(ctx):
        embed = discord.Embed(title="clear",
                              description="Mit " + prefix + "wetter kannst du dir das Wetter so wie einige Infos dazu anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "wetter (Stadt)")
        embed.add_field(name="Beispiel:", value=prefix + "wetter München")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def clear(ctx):
        embed = discord.Embed(title="wetter",
                              description="Mit " + prefix + "clear kannst du eine beliebige Anzahl an Nachrichten aus einem Channel löschen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "clear (Anzahl)")
        embed.add_field(name="Beispiel:", value=prefix + "clear 15")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def benutzerinfo(ctx):
        embed = discord.Embed(title="benutzerinfo",
                              description="Mit " + prefix + "benutzerinfo kannst du dir einige Infos über einen Nutzer anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "benutzerinfo (Benutzer)")
        embed.add_field(name="Beispiel:", value=prefix + "benutzerinfo DCGALAXY")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def ping(ctx):
        embed = discord.Embed(title="ping",
                              description="Mit " + prefix + "ping kannst du dir die Discord WebSocket protocol latency anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "ping")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def give(ctx):
        embed = discord.Embed(title="ping",
                              description="Mit " + prefix + "give wird eine Minecraft Konsole simuliert",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "give (item) (spieler)")
        embed.add_field(name="Beispiel:", value=prefix + "give diamonds DCGALAXY")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def lol(ctx):
        embed = discord.Embed(title="lol",
                              description="Mit " + prefix + "lol kannst du dir eine League of Legends Stats anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "lol (level/rang) (name)")
        embed.add_field(name="Beispiel:", value=prefix + "lol rang Aftersh0ock")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def mc(ctx):
        embed = discord.Embed(title="mc",
                              description="Mit " + prefix + "mc (command) kannst du dir mehrere Interessante sachen zu Minecraft Anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Mehr Infos gibts es hier:", value=prefix + "mc ")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def osu(ctx):
        embed = discord.Embed(title="osu",
                              description="Mit " + prefix + "osu kannst du dir Osu Stats zu einem Spieler Anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "osu (name)")
        embed.add_field(name="Beispiel:", value=prefix + "osu Aftersh0ock")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def earth2(ctx):
        embed = discord.Embed(title="earth2",
                              description="Mit " + prefix + "earth2 kannst du dir Earth2 Stats zu Deutschland Anzeigen lassen",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=prefix + "earth2")
        await ctx.send(embed=embed)

    @hilfe.command()
    async def anime(ctx):
        embed = discord.Embed(title="anime",
                              description="Sende ein Bild und als Beschreibung " + prefix + "anime und es sagt dir welcher anime es ist",
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value="Bild mit Kommentar" + prefix + "anime")
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
            url="https://static.wikia.nocookie.net/hypixel-skyblock/images/4/4d/Enchanted_Golden_Apple.gif/revision"
                "/latest/smart/width/200/height/200?cb=20200619230630")
        await ctx.send(embed=embed)


give()


use_mysql = False

if os.path.exists("mysql.json"):
        with open('mysql.json', 'r') as f:
            json_stuff = json.load(f)
            host = json_stuff["host"]
            user = json_stuff["user"]
            passwort = json_stuff["passwort"]
            datenbank = json_stuff["datenbank"]
            port = json_stuff["port"]
            tablename = json_stuff["tablename"]
            use_mysql = True



else:
    pass


async def sql_connection_stuff(message):
    if not use_mysql:
        return
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=passwort,
        database=datenbank,
        port=port)
    zeit = datetime.datetime.now()
    zeit_srftime = zeit.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO " + tablename + "(time, content, attachement, membername, memberid, guildid, guildname, channelid,  \
             channelname, id)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    val = [
        (f"{zeit_srftime}", f"{message.content}", f"{message.attachments}", f"{message.author}",
         f"{message.author.id}", f"{message.guild.id}", f"{message.guild}",
         f"{message.channel.id}", f"{message.channel}", f"{message.id}")
    ]
    mycursor = mydb.cursor()
    mycursor.executemany(sql, val)
    mydb.commit()


@client.event
async def on_message(message):
    asyncio.ensure_future(sql_connection_stuff(message))
    await client.process_commands(message)

with open('config.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

client.run(token)

