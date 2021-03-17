from discord.ext import commands
import discord
import random


class Give(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="give")
    async def give_command(self, ctx, item=None, member: discord.Member=None):
        randomnum = random.randint(0, 64)
        if item is None:
            embed = discord.Embed(title="Minecraft Konsole",
                                 description="gieb das Item und dann den Discord Namen ein".format(),
                                 colour=ctx.author.color)
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/top-crop/width/300/height/300?cb=20190903234415")
            await ctx.channel.send(embed=embed)

        if member is None:
            await ctx.channel.send("Du musst einen discord nutzer angeben!")

        elif item == "diamonds":
            embed = discord.Embed(title="Minecraft Konsole",
                                  description="`/give {0} minecraft:diamonds {1}`".format(member.name, randomnum),
                                  colour=ctx.author.color)
            embed.set_thumbnail(url="https://freepngimg.com/thumb/minecraft/11-2-minecraft-diamond-png.png")
            await ctx.channel.send(embed=embed)

        elif item == "schwert":
            embed = discord.Embed(title="Minecraft Konsole",
                                  description="`/give {0} minecraft:diamond_sword {1}`".format(member.name, randomnum),
                                  colour=ctx.author.color)
            embed.set_thumbnail(url="https://assets.stickpng.com/images/580b57fcd9996e24bc43c301.png")
            await ctx.send(embed=embed)

        elif item == "opgoldapfel":
            embed = discord.Embed(title="Minecraft Konsole",
                                  description="`/give {0} enchanted_golden_apple {1}`".format(member.name, randomnum),
                                  colour=ctx.author.color)
            embed.set_thumbnail(
                url="https://static.wikia.nocookie.net/hypixel-skyblock/images/4/4d/Enchanted_Golden_Apple.gif/revision"
                    "/latest/smart/width/200/height/200?cb=20200619230630")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Give(client))
