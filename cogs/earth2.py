from discord.ext import commands
import discord
import requests
from botlibrary import constants


class Earth2(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = constants.earth2
        self.imgurl = constants.earth2landicon

    @commands.command(name="earth2")
    async def earth2_command(self, ctx):
        response = requests.get(self.url).json()
        land = response["name"]
        wert = response["marketplace_tile_value"]
        verkauft = response["total_sold_tiles"]
        embed = discord.Embed(title="Earth2 Statistiken für " + land, url=self.imgurl + land)
        embed.set_thumbnail(
            url="https://static-cdn.jtvnw.net/jtv_user_pictures/99783da2-3f60-4aeb-92bd-83e953c03627-profile_image-70x70.png")
        embed.add_field(name="Wert eines Tiles", value=f"{wert}E$")
        embed.add_field(name="Insgesamt verkauft", value=f"{verkauft} Tiles")
        await ctx.send(embed=embed)
        return


def setup(client):
    client.add_cog(Earth2(client))
