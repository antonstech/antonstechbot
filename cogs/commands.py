﻿from discord.ext import commands
import discord
from botlibrary import constants
import psycopg2

database_connection = psycopg2.connect(
    host=constants.host,
    user=constants.user,
    password=constants.password,
    database=constants.database,
    port=constants.port)

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    def ist_gepinnt(self, message):
        return not message.pinned

    @commands.command(name="ping", aliases=["latency"])
    async def ping_command(self, ctx):
        await ctx.channel.send(f"The Ping is {round(self.client.latency * 1000)}ms")

    @commands.command(name="version")
    async def version(self, ctx):
        await ctx.channel.send(
            "The Bot is running on Release " + str(
                constants.VERSION) + " and is working because of discord.py Version {}".format(
                discord.__version__))

    @commands.command(name="einladen", aliases=["invite", "ialsowantthatcoolbot"])
    async def einladen(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Press the Link to invite the bot",
                         url=discord.utils.oauth_url(self.client.user.id, permissions=discord.Permissions(8),
                                                     guild=ctx.guild))
        await ctx.channel.send(embed=embed)

    @commands.command(name="hosten", aliases=["host"])
    async def hosten_command(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Press here for a Tutorial to selfhost the bot",
                         url='https://github.com/antonstech/antonstechbot/wiki/Setup')
        await ctx.channel.send(embed=embed)

    @commands.command(name="code")
    async def code_command(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Here you can find the whole Code of the Bot",
                         url='https://github.com/antonstech/antonstechbot')
        await ctx.channel.send(embed=embed)

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx, amount=7):
        await ctx.channel.purge(limit=amount + 1, check=self.ist_gepinnt)
        await ctx.send(f"{amount} Messages were deleted by {ctx.author} :)", delete_after=7)

    @commands.command(name="list")
    async def list_command(self, ctx):
        if str(len(self.client.guilds)) == 1:
            await ctx.send("The Bot is on the following Server:")
        else:
            await ctx.send("The Bot is on the following " + str(len(self.client.guilds)) + " Servers:")
        for guild in self.client.guilds:
            await ctx.send("- " + str(guild.name))
        await ctx.send(
            f"On these {str(len(self.client.guilds))} Servers there are {len(set(self.client.get_all_members()))} Members")

    @commands.command(name="changeprefix", aliases=["prefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix):
        if prefix == "" or '':
            await ctx.send("Your Prefix cant be nothing Bro")
        else:
            code2execute = f"UPDATE prefixes SET prefix = '{prefix}' WHERE id = {ctx.guild.id}"
            mycursor = database_connection.cursor()
            mycursor.execute(code2execute)
            database_connection.commit()
            await ctx.send(f'The Prefix is now "{prefix}"')

    @commands.command(name="maxmembers")
    async def max_member_command(self, ctx):
        await ctx.send(f"The maximum Amount of Members on this Server is {ctx.guild.max_members}")


def setup(client):
    client.add_cog(Commands(client))
