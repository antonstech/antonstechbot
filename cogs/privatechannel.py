import json
import discord
from discord.ext import commands
from botlibrary import constants
import os
from .errorstuff import basicerror


class privatechannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bitrate = constants.bitrate
        self.prefix = constants.bot_prefix

    @commands.command(name="privatechannel")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def create_voice_channel(self, ctx, channelname=None, maxusers=None):
        if os.path.exists("temp/privatechannel.json"):
            pass
        else:
            with open("temp/privatechannel.json", "w") as f:
                f.write("{}")
        with open("temp/guildlist.json", "r") as f:
            json_stuff = json.load(f)
        if json_stuff[str(ctx.guild.id)] is True:
            with open("temp/privatechannel.json", "r") as f:
                channels = json.load(f)
            try:
                channels[str(ctx.message.author.id)]
                await ctx.send(f"{ctx.message.author.mention} You already have a Channel!")
            except:
                if channelname is None:
                    channelnamefinal = ctx.message.author.name + "'s Channel"
                else:
                    channelnamefinal = channelname
                if maxusers is None:
                    maxusersfinal = 2
                elif int(maxusers) > 99:
                    await ctx.send(
                        f"{ctx.message.author.mention} you cant do more than 99 Members!")
                    maxusersfinal = 99
                else:
                    maxusersfinal = maxusers
                guild = ctx.guild
                try:
                    with open("temp/categoryname.json", "r") as f:
                        json_stuff = json.load(f)
                        test = json_stuff[str(ctx.guild.id)]
                except:
                    await ctx.send("The owner has not yet created a category for the private channels")
                    await ctx.send(f"For this he only has to execute {self.prefix}category")
                with open("temp/categoryname.json", "r") as f:
                    json_stuff = json.load(f)
                    categoryname = json_stuff[str(ctx.guild.id)]
                category = discord.utils.get(ctx.guild.categories, name=categoryname)
                await guild.create_voice_channel(name=channelnamefinal, user_limit=maxusersfinal, category=category,
                                                 bitrate=self.bitrate)
                channel = discord.utils.get(ctx.guild.channels, name=channelnamefinal)
                channels[str(ctx.message.author.id)] = channel.id
                with open("temp/privatechannel.json", "w") as f:
                    json.dump(channels, f, indent=2)
                await channel.set_permissions(ctx.message.author, connect=True, move_members=True, speak=True,
                                              manage_permissions=True, mute_members=True, use_voice_activation=True,
                                              view_channel=True, )
                await ctx.send(f'Channel "{channelnamefinal}" was successfully created!')
                await ctx.send(
                    f"With {self.prefix}add @User you can give people access to your channel")
                await ctx.send(
                    f"With {self.prefix}remove @User you can take away people access to your channel")
                await ctx.send(f"With {self.prefix}delchannel you can delete your channel!")
        else:
            await ctx.send("This function is not enabled on this Discord.")
            await ctx.send(f"Contact {ctx.guild.owner.mention} if you want to have it activated")
            await ctx.send(f"This must then make {self.prefix}pc!")

    @commands.command(name="delchannel")
    async def delete_voice_channel(self, ctx):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
        channel_id = json_stuff[str(ctx.message.author.id)]
        channel = self.client.get_channel(channel_id)
        del json_stuff[str(ctx.message.author.id)]

        with open("temp/privatechannel.json", "w") as f:
            json.dump(json_stuff, f, indent=2)
        await channel.delete()
        await ctx.send(f"{channel.name} was deleted!")

    @commands.command(name="pc")
    async def enable_privatechannels(self, ctx, arg=None):
        if ctx.message.author.id is not ctx.guild.owner.id:
            await ctx.send("Only the Owner can use this command!")
        else:
            if arg is None:
                await ctx.send("You have to take an Option: on/off")
            elif arg == "on":
                with open("temp/guildlist.json") as thejsonfile:
                    file = json.load(thejsonfile)
                    guild = ctx.author.guild
                    file[str(guild.id)] = True

                with open("temp/guildlist.json", "w") as thejsonfile:
                    json.dump(file, thejsonfile, indent=2)
                await ctx.send("Privatechannels are now activated :)")
            elif arg == "off":
                with open("temp/guildlist.json") as thejsonfile:
                    file = json.load(thejsonfile)
                    guild = ctx.author.guild
                    file[str(guild.id)] = False

                with open("temp/guildlist.json", "w") as thejsonfile:
                    json.dump(file, thejsonfile, indent=2)
                await ctx.send("Privatechannels are now deactivated :(")

    @commands.command(name="kategorie", aliases=["category"])
    async def kategorie_command(self, ctx, kategorie=None):
        if os.path.exists("temp/categoryname.json"):
            pass
        else:
            with open("temp/categoryname.json", "w") as f:
                f.write("{}")
        if ctx.message.author.id is not ctx.guild.owner.id:
            await ctx.send("Nur der Owner kann diesen Command benutzen!")
        else:
            if kategorie is None:
                await ctx.send("Hier musst du eine Kategorie auswählen in welcher die Privatechannels erstellt werden")
                await ctx.send(
                    'Du musst es so einstellten, das der "Standard-Nutzer" diese zwar sehen kann aber nicht darauf zugreifen kann')
            else:
                channels = {f"{str(ctx.guild.id)}": kategorie}
                with open("temp/categoryname.json", "w") as f:
                    json.dump(channels, f, indent=2)

    @commands.command(name="hinzufügen", aliases=["zugriff", "addchannel", "add"])
    async def add_member(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
        channel_id = json_stuff[str(ctx.message.author.id)]
        channel = self.client.get_channel(channel_id)
        await channel.set_permissions(member, connect=True, speak=True, use_voice_activation=True,
                                      view_channel=True, )
        await ctx.send(f"{member.mention} can now access the Channel :)")

    @commands.command(name="entfernen", aliases=["deny", "remove"])
    async def remove_member(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
        channel_id = json_stuff[str(ctx.message.author.id)]
        channel = self.client.get_channel(channel_id)
        await channel.set_permissions(member, connect=False)
        await ctx.send(f"{member.mention} can't access The Channel anymore")

    @commands.command(name="removechannel")
    @commands.has_permissions(administrator=True)
    async def remove_channel_admins_only_command(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
            try:
                channel_id = json_stuff[str(member.id)]
            except KeyError:
                await ctx.send("This User does not have a Channel!")
            except:
                await basicerror(ctx)
            try:
                channel = self.client.get_channel(channel_id)
                del json_stuff[str(member.id)]
                with open("temp/privatechannel.json", "w") as f:
                    json.dump(json_stuff, f, indent=2)
                await channel.delete()
                await ctx.send(f'"{channel.name}" from {member.mention} was deleted!')
            except:
                pass


def setup(client):
    client.add_cog(privatechannel(client))
