from discord.ext import commands
from botlibrary.utils import get_variable


def owner_only(func):
    async def wrapper(self, message, *args, **kwargs):
        ctx = get_variable('ctx')
        info = await self.client.application_info()
        if ctx.author.id == info.owner.id:
            return await func(self, message, *args, **kwargs)
        await ctx.channel.send("You can't do that Bro you know that very well!")
        print(f"{message.author} tried to shutdown the bot!")

    return wrapper


class shutdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="shutdown", aliases=["off", "stop", "HAAALTSTOP", "ALARM!"])
    @owner_only
    async def shutdown_command(self, ctx):
        await ctx.send("Bot is shutting off... ")
        await self.client.close()


def setup(client):
    client.add_cog(shutdown(client))
