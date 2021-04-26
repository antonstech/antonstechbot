import requests
import discord
from discord.ext import commands
from botlibrary import constants
from .errorstuff import error


class ShortUrl(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = constants.bot_prefix

    @commands.command(name="short")
    async def short_command(self, ctx, link2short=None, customlink=None):

        if link2short is None:
            embed = discord.Embed(title="Mit der Short Funktion kannst du Links verkürzen")
            embed.add_field(name="Benutzung:", value=f"{self.prefix}short (link) (kürzel)")
            embed.set_author(name="Du musst das https:// mit angeben!")
            embed.add_field(name="Beispiel:",
                            value=f"{self.prefix}short https://www.amazon.de/abc cooles Produkt")
            embed.set_footer(
                text="Wichtig: Das Kürzel ist NICHT notwendig, wenn keins angeben wird wird 1 Zufälliges erzeugt")
            await ctx.send(embed=embed)

        elif link2short is not None and customlink is not None:
            response = requests.post(f"https://api.pyshort.de?points_to={link2short}&short={customlink}").json()
            await ctx.send(response)

        elif link2short is not None:
            response = requests.post(f"https://api.pyshort.de?points_to={link2short}").json()
            await ctx.send(response)

        else:
            await error(ctx)


def setup(client):
    client.add_cog(ShortUrl(client))
