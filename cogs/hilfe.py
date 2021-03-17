from discord.ext import commands
import discord
from lib import constants
import json


class Hilfe(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def send(self, ctx, command_name, description, usage, example):
        embed = discord.Embed(title=command_name,
                              description=description.format(constants.bot_prefix),
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=usage.format(constants.bot_prefix))
        embed.add_field(name="Beispiel:", value=example.format(constants.bot_prefix))
        await ctx.channel.send(embed=embed)

    @commands.command(name="hilfe")
    async def hilfe_command(self, ctx, command_name=None):

        if command_name is None:
            embed = discord.Embed(title="Hilfe",
                                  description="Benutze " + constants.bot_prefix + "hilfe (command) für mehr Informationen zu einem Command.",
                                  color=ctx.author.color)
            embed.add_field(name="Moderation:", value="clear")
            embed.add_field(name="nützlich:", value="wetter, benutzerinfo , ping, anime", inline=True)
            embed.add_field(name="fun", value="give, corona, earth2", inline=True)
            embed.add_field(name="Game-Stats", value="lol, osu", inline=True)
            embed.add_field(name="Minecraft Zeugs", value="mc", inline=True)
            embed.add_field(name="Infos zum Bot", value="version, einladen, hosten, code", inline=True)
            embed.set_footer(text='Bei sonstigen Fragen einfach DCGALAXY#9729 anschreiben')
            await ctx.send(embed=embed)
            return

        with open("lib/help.json") as f:
            json_stuff = json.load(f)

        try:
            base = json_stuff[command_name]
            description = base["description"]
            usage = base["usage"]
            example = base["example"]
            await self.send(ctx, command_name, description, usage, example)

        except KeyError:
            pass


def setup(client):
    client.add_cog(Hilfe(client))
