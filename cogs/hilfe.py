import json
from discord.ext import commands
import discord
from botlibrary import constants
import psycopg2

default_prefix = constants.bot_prefix
database_connection = psycopg2.connect(
    host=constants.host,
    user=constants.user,
    password=constants.password,
    database=constants.database,
    port=constants.port)

class Hilfe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="hilfe", aliases=["help", "welp"])
    async def hilfe_command(self, ctx, command_name=None):
        try:
            code2execute = f"SELECT prefix FROM prefixes WHERE id = {ctx.message.guild.id}"
            mycursor = database_connection.cursor()
            database_connection.commit()
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            prefix = result[0]
        except:
            prefix = default_prefix

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

    async def send(self, ctx, command_name, description, usage, example):
        try:
            code2execute = f"SELECT prefix FROM prefixes WHERE id = {ctx.message.guild.id}"
            mycursor = database_connection.cursor()
            database_connection.commit()
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            prefix = result[0]
        except:
            prefix = default_prefix
        embed = discord.Embed(title=command_name,
                              description=description.format(prefix),
                              color=ctx.author.color)
        embed.add_field(name="Benutzung:", value=usage.format(prefix))
        embed.add_field(name="Beispiel:", value=example.format(prefix))
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Hilfe(client))
