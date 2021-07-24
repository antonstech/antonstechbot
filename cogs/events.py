from discord.ext import commands
import os
import json
import mysql.connector
import datetime
import asyncio
from botlibrary import constants
import logging

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.use_mysql = False
        self.default_prefix = constants.bot_prefix
        if os.path.exists("config/mysql.json"):
            with open('config/mysql.json', 'r') as f:
                json_stuff = json.load(f)
                self.host = json_stuff["host"]
                self.user = json_stuff["user"]
                self.passwort = json_stuff["passwort"]
                self.datenbank = json_stuff["datenbank"]
                self.port = json_stuff["port"]
                self.tablename = json_stuff["tablename"]
                self.use_mysql = True

    async def sql_connection_stuff(self, message):
        if not self.use_mysql:
            return
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.passwort,
            database=self.datenbank,
            port=self.port)
        zeit = datetime.datetime.now()
        zeit_srftime = zeit.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO " + self.tablename + "(time, content, attachment, membername, memberid, guildid, guildname, channelid,  \
                 channelname, id)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        val = [
            (f"{zeit_srftime}", f"{message.content}", f"{message.attachments}", f"{message.author}",
             f"{message.author.id}", f"{message.guild.id}", f"{message.guild}",
             f"{message.channel.id}", f"{message.channel}", f"{message.id}")
        ]
        mycursor = mydb.cursor()
        mycursor.executemany(sql, val)
        mydb.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            pass
        else:
            asyncio.ensure_future(self.sql_connection_stuff(message))

        try:
            if message.mentions[0] == self.client.user:
                with open("config/prefixes.json", "r") as f:
                    prefixes = json.load(f)

                prefix = prefixes[str(message.guild.id)]
                await message.channel.send(f"Hey {message.author.mention} :)")
                await message.channel.send(f'My Prefix (on this Server) is "{prefix}"')

        except IndexError:
            pass



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("config/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = self.default_prefix.rel

        with open("config/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=2)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        time = datetime.datetime.now().strftime("%d.%m.%Y")
        logging.basicConfig(filename=f"temp/logfile-{time}.log", level=logging.INFO)
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        logging.info(f'{ctx.message.author} used "{ctx.message.content}" at {time} on {ctx.guild.name}({ctx.guild.id})')


def setup(client):
    client.add_cog(Events(client))
