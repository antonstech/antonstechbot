from discord.ext import commands
from discord.ext.commands import CommandNotFound
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
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send("Dazu hast du keine Berechtigungen! ")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("Da fehlt noch etwas :wink:")
            else:
                raise error


def setup(client):
    client.add_cog(NotFound(client))
