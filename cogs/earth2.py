from discord.ext import commands
import discord
import requests


class Earth2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="earth2")
    async def earth2_command(self, ctx):
        url = "https://earth2stats.net/api/get_countries/199"
        response = requests.get(url).json()
        land = response["name"]
        wert = response["marketplace_tile_value"]
        verkauft = response["total_sold_tiles"]
        embed = discord.Embed(title="Earth2 Statistiken für " + land, url="https://earth2stats.net/country/" + land)
        embed.set_thumbnail(
            url="https://static-cdn.jtvnw.net/jtv_user_pictures/99783da2-3f60-4aeb-92bd-83e953c03627-profile_image-70x70.png")
        embed.add_field(name="Wert eines Tiles", value=f"{wert}E$")
        embed.add_field(name="Insgesamt verkauft", value=f"{verkauft} Tiles")
        await ctx.send(embed=embed)
        return


def setup(client):
    client.add_cog(Earth2(client))
