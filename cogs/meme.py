from discord.ext import commands
import discord
import requests
from botlibrary import constants
from .errorstuff import basicerror


class Memes(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = constants.reddit_url

    @commands.command(name="meme")
    async def meme(self, ctx):
        try:
            response = requests.get(self.url)
            x = response.json()
            link = x["postLink"]
            reddit = x["subreddit"]
            titel = x["title"]
            img = x["url"]
            acc = x["author"]
            votes = x["ups"]
            embed = discord.Embed(title=f"{titel}")
            embed.set_image(url=img)
            embed.set_footer(text=f"Gepostet von u/{acc} in r/{reddit} mit {votes} Upvotes")
            embed.add_field(name="Link zum Post", value=f"[{link}]({link})")
            await ctx.send(embed=embed)
        except:
            await basicerror(ctx)


def setup(client):
    client.add_cog(Memes(client))
