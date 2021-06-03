from discord.ext import commands
import discord
from botlibrary import constants
import requests
from .errorstuff import basicerror


class Osu(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.osuapi = constants.osu_token
        self.url = constants.osu_url

    @commands.command(name="osu")
    async def osu_command(self, ctx, name):
        try:
            spielerstats = self.url + name + "&k=" + self.osuapi
            response = requests.get(spielerstats).json()[0]
            userid = response["user_id"]
            playedgames = response["playcount"]
            level = response["level"]
            levelgerundet = (int(float(level)))
            spielzeit_sekunden = response["total_seconds_played"]
            spielzeit_stunden = int(spielzeit_sekunden) / 3600
            genauigkeit = response["accuracy"]
            genauigkeit_int = (int(float(genauigkeit)))
            globalrank = response["pp_rank"]
            localrank = response["pp_country_rank"]
            land = response["country"]
            embed = discord.Embed(title="Osu Stats for " + name)
            embed.set_thumbnail(url="http://s.ppy.sh/a/" + userid)
            embed.add_field(name="Played Games", value=f"{playedgames}")
            embed.add_field(name="Level", value=f"{levelgerundet}")
            embed.add_field(name="Playtime", value=f"{(int(float(spielzeit_stunden)))} Stunden")
            embed.add_field(name="Accuracy", value=f"{round(genauigkeit_int, 2)}%")
            embed.add_field(name="Global Rank", value=f"{globalrank}")
            embed.add_field(name="Rank in " + land, value=f"{localrank}")
            await ctx.send(embed=embed)
        except:
            await basicerror(ctx)


def setup(client):
    client.add_cog(Osu(client))
