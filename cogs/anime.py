from discord.ext import commands
import discord
import requests
import urllib.parse


class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="anime")
    async def anime_command(self, ctx):
        base_url = "https://trace.moe/api/search?url="
        attachment = ctx.message.attachments[0]
        attachementurl = attachment.url
        url = base_url + attachementurl
        response = requests.post(url).json()["docs"][0]
        genauigkeit = response["similarity"]
        hentai = response["is_adult"]
        titel = response["title_english"]
        nativetitel = response["title_native"]
        anilist = response["anilist_id"]
        filename = response["filename"]
        at = response["at"]
        tokenthumb = response["tokenthumb"]
        # Coming Soon
        filenameencoded = urllib.parse.quote(filename)
        imgrequest = "https://media.trace.moe/image/" + str(anilist) + "/" + filenameencoded + "?t=" + str(
            at) + "&token=" + tokenthumb + "&size=m"
        ###
        if titel is not None:
            embed = discord.Embed(title=f"{titel}")
        else:
            embed = discord.Embed(title=f"{nativetitel}")
        anilisturl = "https://anilist.co/anime/" + str(anilist)
        embed.set_author(name="Anilist Link", url=anilisturl)
        embed.add_field(name="Genauigkeit", value=f"{round(genauigkeit * 100, 2)}%")
        if hentai is False:
            embed.add_field(name="Hentai?", value="Nope :(")
        else:
            embed.add_field(name="Hentai?", value="Yess Sir")
        if titel is not None:
            embed.add_field(name="Titel in Orginalsprache", value=f"{nativetitel}")
        else:
            pass
        embed.set_image(url=str(imgrequest))
        await ctx.send(embed=embed)
        return


def setup(client):
    client.add_cog(Anime(client))
