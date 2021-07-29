import asyncio
import configparser
import datetime
import logging

import psycopg2
from discord.ext import commands

from botlibrary import constants


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.use_database = False
        self.default_prefix = constants.bot_prefix
        config = configparser.ConfigParser()
        config.read("config/config.ini")
        database_config = config["Database"]
        if database_config["logging-enable"] == "true":
            self.tablename = database_config["logging-tablename"]
            self.use_database = True
            self.database_connection = psycopg2.connect(
                host=constants.host,
                user=constants.user,
                password=constants.password,
                database=constants.database,
                port=constants.port)

    async def sql_connection_stuff(self, message):
        zeit = datetime.datetime.now()
        zeit_srftime = zeit.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO " + self.tablename + "(time, content, attachment, membername, memberid, guildid, guildname, channelid,  \
                 channelname, id)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        val = [
            (f"{zeit_srftime}", f"{message.content}", f"{message.attachments}", f"{message.author}",
             f"{message.author.id}", f"{message.guild.id}", f"{message.guild}",
             f"{message.channel.id}", f"{message.channel}", f"{message.id}")
        ]
        mycursor = self.database_connection.cursor()
        mycursor.executemany(sql, val)
        self.database_connection.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.use_database:
            return
        if not message.guild:
            return
        else:
            asyncio.ensure_future(self.sql_connection_stuff(message))

        try:
            if message.mentions[0] == self.client.user:
                database_connection = psycopg2.connect(
                    host=constants.host,
                    user=constants.user,
                    password=constants.password,
                    database=constants.database,
                    port=constants.port)
                code2execute = "SELECT prefix FROM prefixes " + f"WHERE id = {message.guild.id}"
                mycursor = database_connection.cursor()
                mycursor.execute(code2execute)
                result = mycursor.fetchone()
                prefix = result[0]
                await message.channel.send(f"Hey {message.author.mention} :)")
                await message.channel.send(f'My Prefix (on this Server) is "{prefix}"')

        except IndexError:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        mycursor = self.database_connection.cursor()
        sql = "INSERT INTO servers (id, state)  VALUES (%s, %s)"
        val = [
            (f"{int(guild.id)}", False)
        ]
        mycursor.executemany(sql, val)
        sql = "INSERT INTO prefixes (id, prefix)  VALUES (%s, %s)"
        val = [
            (f"{int(guild.id)}", constants.bot_prefix)
        ]
        mycursor.executemany(sql, val)
        self.database_connection.commit()


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        mycursor = self.database_connection.cursor()
        code2execute = f"DELETE FROM servers WHERE id = {guild.id}"
        mycursor.execute(code2execute)
        self.database_connection.commit()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        time = datetime.datetime.now().strftime("%d.%m.%Y")
        logging.basicConfig(filename=f"temp/logfile-{time}.log", level=logging.INFO)
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logging.info(f'{ctx.message.author} used "{ctx.message.content}" at {time} on {ctx.guild.name}({ctx.guild.id})')


def setup(client):
    client.add_cog(Events(client))
