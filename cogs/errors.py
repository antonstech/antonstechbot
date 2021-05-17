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
                embed = discord.Embed(title="Befehl nicht gefunden!", colour=discord.Colour.red())
                embed.set_footer(text="Mit " + self.prefix + "hilfe bekommst du eine übersicht aller Befehle")
                await ctx.send(embed=embed)
            elif isinstance(error, MissingPermissions):
                await ctx.send("Dazu hast du keine Berechtigungen! ")
            elif isinstance(error, MissingRequiredArgument):
                await ctx.send("Da fehlt noch etwas :wink:")
            elif isinstance(error, MemberNotFound):
                await ctx.send("Dieser Nutzer existiert nicht!")
            elif isinstance(error, CommandOnCooldown):
                await ctx.send("**Dieser Befehl hat einen Cooldown!**, bitte versuche es erneut in {:.2f} Sekunden".format(error.retry_after))
            else:
                raise error


def setup(client):
    client.add_cog(NotFound(client))
