from discord.ext import commands
from discord.ext.commands.errors import *
import discord
from botlibrary import constants


class NotFound(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = constants.bot_prefix

        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, CommandNotFound):
                embed = discord.Embed(title="Command not Found!", colour=discord.Colour.red())
                embed.set_footer(text="With " + self.prefix + "help you can see which Commands the Bot has")
                await ctx.send(embed=embed)
            elif isinstance(error, MissingPermissions):
                await ctx.send("You dont have Permissions for that! ")
            elif isinstance(error, MissingRequiredArgument):
                await ctx.send("Something is missing :wink:")
            elif isinstance(error, MemberNotFound):
                await ctx.send("This User doesn't exist!")
            elif isinstance(error, CommandOnCooldown):
                await ctx.send("**This Command has a Cooldown!**, please try again in {:.2f} Seconds".format(error.retry_after))
            else:
                raise error


def setup(client):
    client.add_cog(NotFound(client))
