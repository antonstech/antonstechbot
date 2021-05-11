import discord
from discord.ext import commands
from botlibrary import constants
import requests


class katzen(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_url = constants.cat_api

    @commands.command(name="cat", aliases=["katze", "pussy"])
    async def cat_command(self, ctx):
        response = requests.get(self.api_url).json()
        url = response[0]["url"]
        await ctx.send(url)

def setup(client):
    client.add_cog(katzen(client))
