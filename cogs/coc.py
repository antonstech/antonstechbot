import urllib.parse
import discord
import requests
from discord.ext import commands
from botlibrary import constants
from .errorstuff import basicerror



class CoC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = constants.coc_url
        self.prefix = constants.bot_prefix
        self.token = constants.coc_token

    @commands.command(name="coc")
    async def coc_command(self, ctx, option=None, arg1=None):

        if option is None:
            embed = discord.Embed(title="The CoC Command can show you some stats about the Game COC")
            embed.add_field(name="Funktionen:", value="clan, player")
            await ctx.send(embed=embed)

        if arg1 is None and option is not None:
            await ctx.send("Error: say what you want bro!")

        elif option == "clan":
            clantag = urllib.parse.quote(arg1)
            complete_url = self.base_url + "clans/" + clantag
            headers = {"Authorization": "Bearer " + self.token}
            response = requests.get(complete_url, headers=headers).json()
            try:
                try:
                    if response["reason"] == "notFound":
                        await ctx.send("Clan not Found, you have to take the tag for Example: #CG82U2QG")
                    else:
                        pass
                except:
                    badge = response["badgeUrls"]["medium"]
                    pokale = response["clanPoints"]
                    try:
                        Standort = response["location"]["name"]
                    except:
                        Standort = "Unknown"
                    name = response["name"]
                    mitglieder = response["members"]
                    warwins = response["warWins"]
                    embed = discord.Embed(title="Clan Stats for " + name)
                    embed.set_thumbnail(url=badge)
                    embed.add_field(name="Trophies", value=f"{pokale} :trophy:")
                    embed.add_field(name="Members", value=f"{mitglieder} / 50")
                    embed.add_field(name="Location", value=Standort)
                    embed.add_field(name="won Clanwars", value=warwins)
                    await ctx.send(embed=embed)
            except:
                await basicerror(ctx)

        elif option == "player":
            playertag = urllib.parse.quote(arg1)
            playertagwithouthashtag = str(arg1).replace("#", "")
            complete_url = self.base_url + "players/" + playertag
            headers = {"Authorization": "Bearer " + self.token}
            response = requests.get(complete_url, headers=headers).json()
            try:
                try:
                    if response["reason"] == "notFound":
                        await ctx.send("Player not Found, you have to use the Tag for Example: #CG82U2QG")
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
                    embed = discord.Embed(title="Stats for " + name)
                    embed.set_author(name="More Information", url="https://www.coc-stats.net/de/player/" + playertagwithouthashtag + "/")
                    embed.set_thumbnail(url=clanzeichen)
                    embed.add_field(name="Townhall", value=f"Level {townhall}")
                    embed.add_field(name="Playerlevel", value=playerlvl)
                    embed.add_field(name="Trophies", value=pokale)
                    embed.add_field(name="Trophies-Records", value=maxpokale)
                    embed.add_field(name="Warstars", value=sterne)
                    embed.add_field(name="Builderbase", value=f"Level {nachtdorf}")
                    embed.add_field(name="Clan-Name", value=clanname)
                    await ctx.send(embed=embed)
            except:
                await basicerror(ctx)

def setup(client):
    client.add_cog(CoC(client))
