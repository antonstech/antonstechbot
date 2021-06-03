import requests
import discord
from discord.ext import commands
from botlibrary import constants
from .errorstuff import basicerror


class ShortUrl(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = constants.bot_prefix

    @commands.command(name="short")
    async def short_command(self, ctx, link2short=None, customlink=None):

        if link2short is None:
            embed = discord.Embed(title="With the short function you can shorten links")
            embed.add_field(name="Usage:", value=f"{self.prefix}short (link) (abbreviation)")
            embed.set_author(name="You must include the https://!")
            embed.add_field(name="Example:",
                            value=f"{self.prefix}short https://www.amazon.de/abc productabc")
            embed.set_footer(
                text="Important: The abbreviation is NOT necessary, if none is specified 1 random will be generated")
            await ctx.send(embed=embed)

        elif link2short is not None and customlink is not None:
            response = requests.post(f"https://api.pyshort.de?points_to={link2short}&short={customlink}").json()
            await ctx.send(response)

        elif link2short is not None:
            response = requests.post(f"https://api.pyshort.de?points_to={link2short}").json()
            await ctx.send(response)

        else:
            await basicerror(ctx)


def setup(client):
    client.add_cog(ShortUrl(client))
