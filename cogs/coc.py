import urllib.parse
import discord
import requests
from discord.ext import commands
from botlibrary import constants
from .errorstuff import error



class CoC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = constants.coc_url
        self.prefix = constants.bot_prefix
        self.token = constants.coc_token

    @commands.command(name="coc")
    async def coc_command(self, ctx, option=None, arg1=None):

        if option is None:
            embed = discord.Embed(title="Der CoC Command kann dir viele Nützliche Dinge zum Thema Minecraft anzeigen")
            embed.add_field(name="Funktionen:", value="clan, spieler")
            await ctx.send(embed=embed)

        if arg1 is None and option is not None:
            await ctx.send("Fehler: Gebe etwas an wonach du suchst!")

        elif option == "clan":
            clantag = urllib.parse.quote(arg1)
            complete_url = self.base_url + "clans/" + clantag
            headers = {"Authorization": "Bearer " + self.token}
            response = requests.get(complete_url, headers=headers).json()
            try:
                try:
                    if response["reason"] == "notFound":
                        await ctx.send("Clan nicht gefunden; du musst den Tag angeben also z.B #CG82U2QG")
                    else:
                        pass
                except:
                    badge = response["badgeUrls"]["medium"]
                    pokale = response["clanPoints"]
                    try:
                        Standort = response["location"]["name"]
                    except:
                        Standort = "Unbekannt"
                    name = response["name"]
                    mitglieder = response["members"]
                    warwins = response["warWins"]
                    embed = discord.Embed(title="Clan Statistiken für " + name)
                    embed.set_thumbnail(url=badge)
                    embed.add_field(name="Pokale", value=f"{pokale} :trophy:")
                    embed.add_field(name="Mitglieder", value=f"{mitglieder} / 50")
                    embed.add_field(name="Standort", value=Standort)
                    embed.add_field(name="gewonnene Clankriege", value=warwins)
                    await ctx.send(embed=embed)
            except:
                await error(ctx)

        elif option == "spieler":
            playertag = urllib.parse.quote(arg1)
            playertagwithouthashtag = str(arg1).replace("#", "")
            complete_url = self.base_url + "players/" + playertag
            headers = {"Authorization": "Bearer " + self.token}
            response = requests.get(complete_url, headers=headers).json()
            try:
                try:
                    if response["reason"] == "notFound":
                        await ctx.send("Spieler nicht gefunden; du musst den Tag angeben also z.B #CG82U2QG")
                    else:
                        pass
                except:
                    name = response["name"]
                    townhall = response["townHallLevel"]
                    playerlvl = response["expLevel"]
                    pokale = response["trophies"]
                    maxpokale = response["bestTrophies"]
                    sterne = response["warStars"]
                    nachtdorf = response["builderHallLevel"]
                    clanzeichen = response["clan"]["badgeUrls"]["small"]
                    clanname = response["clan"]["name"]
                    embed = discord.Embed(title="Statistiken für " + name)
                    embed.set_author(name="Mehr Infos", url="https://www.coc-stats.net/de/player/" + playertagwithouthashtag + "/")
                    embed.set_thumbnail(url=clanzeichen)
                    embed.add_field(name="Rathaus", value=f"Level {townhall}")
                    embed.add_field(name="Spielerlevel", value=playerlvl)
                    embed.add_field(name="Pokale", value=pokale)
                    embed.add_field(name="Pokal-Rekord", value=maxpokale)
                    embed.add_field(name="Kriegssterne", value=sterne)
                    embed.add_field(name="Nachtdorf", value=f"Level {nachtdorf}")
                    embed.add_field(name="Clan-Name", value=clanname)
                    await ctx.send(embed=embed)
            except:
                await error(ctx)

def setup(client):
    client.add_cog(CoC(client))
