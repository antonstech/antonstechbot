from discord.ext import commands
import discord
import json


class Hilfe(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def send(self, ctx, command_name, description, usage, example):
        prefixes = self.client.get_default_prefix(client=self.client, message=ctx.message)
        prefix = prefixes[str(ctx.message.guild.id)]
        embed = discord.Embed(title=command_name,
                              description=description.format(prefix),
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=usage.format(prefix))
        embed.add_field(name="Beispiel:", value=example.format(prefix))
        await ctx.channel.send(embed=embed)

    @commands.command(name="hilfe", aliases=["help", "welp"])
    async def hilfe_command(self, ctx, command_name=None):
        prefix = self.client.get_default_prefix(client=self.client, message=ctx.message)
        if command_name is None:
            embed = discord.Embed(title="Help",
                                  description="Use " + prefix + "help (command) for more Information about a Command.",
                                  color=ctx.author.color)
            embed.add_field(name="Admin Only:", value="clear, prefix")
            embed.add_field(name="Privatechannel", value="privatechannel, add, remove, pc, category")
            embed.add_field(name="usefull:", value="weather, userinfo ,anime, corona, reddit", inline=True)
            embed.add_field(name="Nerd-Stuff", value="ip, short")
            embed.add_field(name="fun", value="cat, earth2, meme", inline=True)
            embed.add_field(name="Game-Stats", value="lol, osu, mc, coc", inline=True)
            embed.add_field(name="Infos zum Bot", value="version, invite, host, code, ping, list", inline=True)
            embed.set_footer(text='For other questions just write DCGALAXY#9729')
            await ctx.send(embed=embed)
            return

        with open("botlibrary/help.json") as f:
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
