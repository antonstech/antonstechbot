from discord.ext import commands
import discord
import requests
from .errorstuff import basicerror
from botlibrary import constants

class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.anime_url = constants.anime

    @commands.command(name="anime")
    async def anime_command(self, ctx):
        channel = ctx.message.channel
        async with channel.typing():
            try:
                attachment = ctx.message.attachments[0]
                attachementurl = attachment.url
                url = self.anime_url + attachementurl
                abfrage = requests.post(url)
                response = abfrage.json()["result"][0]
                anilist = response["anilist"]
                if "Database is overloaded" in abfrage.text:
                    ctx.send("The database is too busy, try again in a moment!")
                else:
                    genauigkeit = response["similarity"]
                    hentai = anilist["isAdult"]
                    titel = anilist["title"]["english"]
                    nativetitel = anilist["title"]["native"]
                    anilist = anilist["id"]
                    imgurl = response["image"]
                    if titel is not None:
                        embed = discord.Embed(title=f"{titel}")
                    else:
                        embed = discord.Embed(title=f"{nativetitel}")
                    anilisturl = "https://anilist.co/anime/" + str(anilist)
                    embed.set_author(name="Anilist Link", url=anilisturl)
                    embed.add_field(name="Accuracy", value=f"{round(genauigkeit * 100, 2)}%")
                    if hentai is False:
                        embed.add_field(name="Hentai?", value="Nope :(")
                    else:
                        embed.add_field(name="Hentai?", value="Yess Sir")
                    if titel is not None:
                        embed.add_field(name="Title in original language", value=f"{nativetitel}")
                    else:
                        pass
                    embed.set_image(url=str(imgurl))
                    await ctx.send(embed=embed)
            except:
                await basicerror(ctx)


def setup(client):
    client.add_cog(Anime(client))
