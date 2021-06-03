from discord.ext import commands
import discord
import requests
from botlibrary import constants


# Anton Rewrite that shit

class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = constants.reddit_url

    @commands.command(name="reddit")
    async def reddit_command(self, ctx, subreddit):
        response = requests.get(self.url + "/" + subreddit)
        x = response.json()
        try:
            print(x)
            try:
                link = x["postLink"]
            except:
                pass
            reddit = x["subreddit"]
            titel = x["title"]
            img = x["url"]
            acc = x["author"]
            votes = x["ups"]
            nsfw = x["nsfw"]
            if not nsfw:
                try:
                    embed = discord.Embed(title=f"{titel}")
                    embed.set_image(url=img)
                    embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
                    embed.add_field(name="Link to Post", value=f"[{link}]({link})")
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title=f"{titel}")
                    embed.set_image(url=img)
                    embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
                    await ctx.send(embed=embed)
            else:
                if ctx.channel.is_nsfw():
                    try:
                        embed = discord.Embed(title=f"{titel}")
                        embed.set_image(url=img)
                        embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
                        embed.add_field(name="Link to Post", value=f"[{link}]({link})")
                    except:
                        embed = discord.Embed(title=f"{titel}")
                        embed.set_image(url=img)
                        embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
                        embed.add_field(name="Link to Post", value=f"[{link}]({link})")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("This Channel is not nsfw!")
        except:
            errorcode = x["message"]
            embed = discord.Embed(title="Error!")
            embed.add_field(name="Errorcode:", value=f"`{errorcode}`")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(reddit(client))
