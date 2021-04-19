from discord.ext import commands
from botlibrary.utils import get_variable


def owner_only(func):
    async def wrapper(self, message, *args, **kwargs):
        ctx = get_variable('ctx')
        info = await self.client.application_info()
        if ctx.author.id == info.owner.id:
            return await func(self, message, *args, **kwargs)
        else:
            await ctx.channel.send("Das darfst du nicht Bro das weißt du ganz genau!")
            print(f"{message.author} hat probiert den Bot herunterzufahren!")

    return wrapper


class shutdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="shutdown")
    @owner_only
    async def shutdown_command(self, ctx):
        await ctx.send("Bot wird heruntergefahren... ")
        await self.client.close()


def setup(client):
    client.add_cog(shutdown(client))
