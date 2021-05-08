from discord.ext import commands
import discord
from botlibrary import constants


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    def ist_gepinnt(self, message):
        return not message.pinned

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.channel.send("Der Ping beträgt derzeit " f"{round(self.client.latency * 1000)}ms")

    @commands.command(name="version")
    async def version(self, ctx):
        await ctx.channel.send(
            "Der Bot läuft derzeit auf Release " + str(
                constants.VERSION) + " und geht auch dank discord.py Version {}".format(
                discord.__version__))

    @commands.command(name="einladen")
    async def einladen(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Klicke hier zum einladen",
                         url=discord.utils.oauth_url(self.client.user.id, permissions=discord.Permissions(8),
                                                     guild=ctx.guild))
        await ctx.channel.send(embed=embed)

    @commands.command(name="hosten")
    async def hosten_command(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Klicke hier um ein Tutorial zum Selber hosten zu bekommen",
                         url='https://github.com/antonstech/antonstechbot/wiki/Installation')
        await ctx.channel.send(embed=embed)

    @commands.command(name="code")
    async def code_command(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="Hier findest du den ganzen Code vom Bot",
                         url='https://github.com/antonstech/antonstechbot')
        await ctx.channel.send(embed=embed)

    @commands.command(name="nudes")
    async def nudes_command(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(title="Nudes")
            embed.set_image(
                url="https://www.nydailynews.com/resizer/OYta-jTp2D6Xt_Wj_o6zEUqWttE=/415x562/top/arc-anglerfish-arc2-prod-tronc.s3.amazonaws.com/public/7Y53KJVE7FGLZZPD44LTN4QB5I.jpg")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Der Channel ist nicht nsfw")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx, amount=7):
        await ctx.channel.purge(limit=amount + 1, check=self.ist_gepinnt)

    @commands.command(name="list")
    async def list_command(self, ctx):
        if str(len(self.client.guilds)) == 1:
            await ctx.send("Der Bot ist zurzeit auf folgendem Server:")
        else:
            await ctx.send("Der Bot ist zurzeit auf folgenden " + str(len(self.client.guilds)) + " Servern:")
        for guild in self.client.guilds:
            await ctx.send("- " + str(guild.name))
            await ctx.send(f"Auf diesen {str(len(self.client.guilds))} Servern sind insgesamt {len(set(self.client.get_all_members()))} Mitglieder")

def setup(client):
    client.add_cog(Commands(client))
