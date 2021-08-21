from discord.ext import commands
import discord
import requests
from botlibrary import constants
from .errorstuff import basicerror

# Rewrite that shit

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
            embed = discord.Embed(url=link, title=titel)
            embed.set_image(url=img)
            embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
            await ctx.send(embed=embed)
        except:
            await basicerror(ctx)


def setup(client):
    client.add_cog(Memes(client))
