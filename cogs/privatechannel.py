import configparser
import datetime
import discord
import psycopg2
from psycopg2 import errors
from discord.ext import commands
from discord.ext.commands import MemberConverter
from botlibrary import constants
from discord.ext.commands.errors import *


class privatechannel(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = constants.bot_prefix
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        database_config = config["Database"]
        if database_config["channel-enable"] == "true":
            self.use_database = True
            self.database_connection = psycopg2.connect(
                host=constants.host,
                user=constants.user,
                password=constants.password,
                database=constants.database,
                port=constants.port)

    @commands.command(name="privatechannel", aliases=["channel", "privatchannel", "privatkanal", "kanal"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def privatechannel(self, ctx, arg1=None, arg2=None, arg3=None):
        if constants.channel_enable == "false":
            await ctx.send(f"{ctx.author.mention} this Function is not enabled by the bot hoster")
            return
        mycursor = self.database_connection.cursor()
        if arg1 is None:
            embed = discord.Embed(title="Create custom Channels")
            embed.add_field(name="Functions for everyone:", value="create, add, delete")
            embed.add_field(name="Admin Only: ", value="on, off, category, remove")
            await ctx.send(embed=embed)

        elif arg1 == "delete":
            code2execute = "SELECT channelid FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{ctx.message.author.id}'"
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            self.database_connection.commit()
            channelid = result[0]
            channel = self.client.get_channel(channelid)
            await channel.delete()
            code2execute = "DELETE FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{ctx.message.author.id}'"
            mycursor.execute(code2execute)
            self.database_connection.commit()
            await ctx.send(f'"{channel.name}" was deleted!')

        elif arg1 == "add":
            code2execute = "SELECT channelid FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{ctx.message.author.id}'"
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            self.database_connection.commit()
            channelid = result[0]
            channel = self.client.get_channel(channelid)
            converter = MemberConverter()
            member = await converter.convert(ctx, arg2)
            await channel.set_permissions(member, connect=True, speak=True, use_voice_activation=True,
                                          view_channel=True, stream=True)
            await ctx.send(f"{member.mention} can now access the Channel :)")

        elif arg1 == "deny":
            code2execute = "SELECT channelid FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{ctx.message.author.id}'"
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            channelid = result[0]
            channel = self.client.get_channel(channelid)
            converter = MemberConverter()
            member = await converter.convert(ctx, arg2)
            await channel.set_permissions(member, connect=False)
            await ctx.send(f"{member.mention} can't access The Channel anymore")

        elif arg1 == "on":
            if ctx.message.author.guild_permissions.administrator:
                code2execute = f"UPDATE servers SET state = true WHERE id = {ctx.guild.id}"
                self.database_connection.commit()
                mycursor.execute(code2execute)
                self.database_connection.commit()
                try:
                    code2execute = f'create table "{ctx.guild.id}"(memberid bigint not null constraint "{ctx.guild.id}_pkey" primary key,channelid bigint not null, creation_time timestamp not null)'
                    mycursor.execute(code2execute)
                    self.database_connection.commit()
                except errors.lookup("42P07"):
                    pass
                await ctx.send("Custom User Channels are now **activated**")
            else:
                await ctx.send(f"{ctx.author.mention} You are not an Administrator!")

        elif arg1 == "off":
            if ctx.message.author.guild_permissions.administrator:
                code2execute = f"UPDATE servers SET state = false WHERE id = {ctx.guild.id}"
                self.database_connection.commit()
                mycursor.execute(code2execute)
                self.database_connection.commit()
                await ctx.send("Custom User Channels are now **disabled**")
            else:
                await ctx.send(f"{ctx.author.mention} You are not an Administrator!")

        elif arg1 == "create":
            code2execute = f"SELECT state FROM servers where id = {ctx.guild.id}"
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            self.database_connection.commit()
            if result[0] is True:
                code2execute = f"SELECT * FROM " + f'"{ctx.guild.id}"' + " WHERE memberid = " + f"'{ctx.message.author.id}'"
                mycursor.execute(code2execute)
                result = mycursor.fetchone()
                if result is not None:
                    await ctx.send(f"{ctx.author.mention} you already have a Channel!")
                else:
                    code2execute = "SELECT name FROM " + "categorynames" + " WHERE serverid = " + f"'{ctx.message.guild.id}'"
                    try:
                        mycursor.execute(code2execute)
                        result = mycursor.fetchone()
                        justatestifitbreaks = result[0]
                    except:
                        await ctx.send("The category where the Channels should be created is not set")
                    categoryname = result[0]
                    await ctx.send("Channel is being created (This might take some time)", delete_after=5)
                    if arg2 is None:
                        channelnamefinal = ctx.message.author.name + "'s Channel"
                    else:
                        channelnamefinal = arg2
                    if arg3 is None:
                        maxusersfinal = 5
                    elif int(arg3) > 99:
                        await ctx.send(
                            f"{ctx.message.author.mention} you cant do more than 99 Members!", delete_after=15)
                        maxusersfinal = 99
                    else:
                        maxusersfinal = arg3
                    if arg2 is None and arg3 is None:
                        await ctx.send(
                            f"{ctx.message.author.mention} btw you can use ur own Channel Name and Member Limit\n"
                            f"Example: {self.prefix}channel create nice 69")
                    guild = ctx.guild
                    category = discord.utils.get(ctx.guild.categories, name=categoryname)
                    created_channel = await guild.create_voice_channel(name=channelnamefinal, user_limit=maxusersfinal,
                                                                       category=category,
                                                                       bitrate=guild.bitrate_limit)
                    channel = discord.utils.get(ctx.guild.channels, id=created_channel.id)
                    await channel.set_permissions(ctx.message.author, connect=True, move_members=True, speak=True,
                                                  mute_members=True, use_voice_activation=True,
                                                  view_channel=True, stream=True)
                    zeit = datetime.datetime.now()
                    zeit_srftime = zeit.strftime("%Y-%m-%d %H:%M:%S")
                    sql = "INSERT INTO " + f'"{ctx.guild.id}"' + " (memberid, channelid, creation_time)  VALUES (%s, %s, %s) "
                    val = [
                        (f"{ctx.message.author.id}", f"{created_channel.id}", f"{zeit_srftime}")
                    ]
                    mycursor.executemany(sql, val)
                    self.database_connection.commit()
                    await ctx.send(f'Channel "{channelnamefinal}" was successfully created!\n'
                                   f"With {self.prefix}channel add @User you can give people access to your channel\n"
                                   f"With {self.prefix}channel deny @User you can take away people access to your channel\n"
                                   f"With {self.prefix}channel delete you can delete your channel!")
            else:
                await ctx.send(f"This function is not enabled on this Discord.\n"
                               f"Please contact {ctx.guild.owner.mention} if you want to have it activated")
        elif arg1 == "category":
            try:
                code2execute = f"UPDATE categorynames SET name = '{arg2}' WHERE serverid = {ctx.guild.id}"
                mycursor.execute(code2execute)
                self.database_connection.commit()
            except:
                code2execute = f"INSERT INTO categorynames (serverid, name) VALUES {ctx.guild.id} {arg2}"
                mycursor.execute(code2execute)
                self.database_connection.commit()
            await ctx.send(f'The Category where custom user Channels will now be created will be "{arg2}"')

        elif arg1 == "remove":
            converter = MemberConverter()
            member = await converter.convert(ctx, arg2)
            code2execute = "SELECT channelid FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{member.id}'"
            mycursor.execute(code2execute)
            result = mycursor.fetchone()
            self.database_connection.commit()
            channelid = result[0]
            channel = self.client.get_channel(channelid)
            await channel.delete()
            code2execute = "DELETE FROM " + f'"{ctx.message.guild.id}"' + " WHERE memberid = " + f"'{member.id}'"
            mycursor.execute(code2execute)
            self.database_connection.commit()
            await ctx.send(f'"{channel.name}" from {member.mention} was removed!')

        else:
            raise CommandNotFound
        self.database_connection.commit()


def setup(client):
    client.add_cog(privatechannel(client))
