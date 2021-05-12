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
                await ctx.send(f"{ctx.message.author.mention} Du hast schon einen Channel!")
            except:
                if channelname is None:
                    channelnamefinal = ctx.message.author.name + "'s Channel"
                else:
                    channelnamefinal = channelname
                if maxusers is None:
                    maxusersfinal = 2
                elif int(maxusers) > 99:
                    await ctx.send(
                        f"{ctx.message.author.mention} es gehen nicht mehr als 99 Member! Member auf 99 gesetzt!")
                    maxusersfinal = 99
                else:
                    maxusersfinal = maxusers
                guild = ctx.guild
                try:
                    with open("temp/categoryname.json", "r") as f:
                        json_stuff = json.load(f)
                        test = json_stuff[str(ctx.guild.id)]
                except:
                    await ctx.send("Der Owner hat noch keine Kategorie für die Privatechannels eingerichtet")
                    await ctx.send(f"Hierzu muss er nur {self.prefix}kategorie ausführen")
                with open("temp/categoryname.json", "r") as f:
                    json_stuff = json.load(f)
                    categoryname = json_stuff[str(ctx.guild.id)]
                category = discord.utils.get(ctx.guild.categories, name=categoryname)
                await guild.create_voice_channel(name=channelnamefinal, user_limit=maxusersfinal, category=category,
                                                    bitrate=self.bitrate)
                channel = discord.utils.get(ctx.guild.channels, name=channelnamefinal)
                channels[str(ctx.message.author.id)] = channel.id
                await channel.set_permissions(ctx.message.author, connect=True, move_members=True, speak=True,
                                                manage_permissions=True, mute_members=True, use_voice_activation=True,
                                                view_channel=True, )
                with open("temp/privatechannel.json", "w") as f:
                    json.dump(channels, f, indent=2)
                await ctx.send(f'Channel "{channelnamefinal}" wurde erfolgreich erstellt!')
                await ctx.send(
                    f"Mit {self.prefix}hinzufügen @User kannst du Leuten Zugriff auf deinen Channel geben")
                await ctx.send(
                    f"Mit {self.prefix}entfernen @User kannst du Leuten Zugriff auf deinen Channel wegnehmen")
                await ctx.send(f"Mit {self.prefix}delchannel kannst du deinen Channel löschen!")
        else:
            await ctx.send("Diese Funktion ist auf diesem Discord nicht aktiviert.")
            await ctx.send(f"Kontaktiere doch {ctx.guild.owner.mention} wenn du es aktiviert haben willst")
            await ctx.send(f" Dieser muss dann {self.prefix}pc machen!")

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
        await ctx.send(f"{channel.name} wurde gelöscht!")

    @commands.command(name="pc")
    async def enable_privatechannels(self, ctx, arg=None):
        if ctx.message.author.id is not ctx.guild.owner.id:
            await ctx.send("Nur der Owner kann diesen Command benutzen!")
        else:
            if arg is None:
                await ctx.send("Du musst eine Option angeben: an/aus")
            elif arg == "an":
                with open("temp/guildlist.json") as thejsonfile:
                    file = json.load(thejsonfile)
                    guild = ctx.author.guild
                    file[str(guild.id)] = True

                with open("temp/guildlist.json", "w") as thejsonfile:
                    json.dump(file, thejsonfile, indent=2)
                await ctx.send("Private Channels sind jetzt aktiviert :)")
            elif arg == "aus":
                with open("temp/guildlist.json") as thejsonfile:
                    file = json.load(thejsonfile)
                    guild = ctx.author.guild
                    file[str(guild.id)] = False

                with open("temp/guildlist.json", "w") as thejsonfile:
                    json.dump(file, thejsonfile, indent=2)
                await ctx.send("Private Channels sind jetzt deaktiviert :(")

    @commands.command(name="kategorie")
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

    @commands.command(name="hinzufügen", aliases=["zugriff", "addchannel"])
    async def add_member(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
        channel_id = json_stuff[str(ctx.message.author.id)]
        channel = self.client.get_channel(channel_id)
        await channel.set_permissions(member, connect=True, speak=True, use_voice_activation=True,
                                      view_channel=True, )
        await ctx.send(f"{member.mention} kann jetzt auf den Channel zugreifen :)")

    @commands.command(name="entfernen", aliases=["deny"])
    async def remove_member(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
        channel_id = json_stuff[str(ctx.message.author.id)]
        channel = self.client.get_channel(channel_id)
        await channel.set_permissions(member, connect=False)
        await ctx.send(f"{member.mention} kann jetzt nicht mehr auf den Channel zugreifen")

    @commands.command(name="removechannel")
    @commands.has_permissions(administrator=True)
    async def remove_channel_admins_only_command(self, ctx, member: discord.Member):
        with open("temp/privatechannel.json", "r") as f:
            json_stuff = json.load(f)
            try:
                channel_id = json_stuff[str(member.id)]
            except KeyError:
                await ctx.send("Dieser Nutzer hat keinen Channel!")
            except:
                await basicerror(ctx)
            try:
                channel = self.client.get_channel(channel_id)
                del json_stuff[str(member.id)]
                with open("temp/privatechannel.json", "w") as f:
                    json.dump(json_stuff, f, indent=2)
                await channel.delete()
                await ctx.send(f'"{channel.name}" von {member.mention} wurde gelöscht!')
            except:
                pass


def setup(client):
    client.add_cog(privatechannel(client))
