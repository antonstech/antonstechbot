from discord.ext import commands
import os
import json
import mysql.connector
import datetime
import asyncio


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.use_mysql = False
        if os.path.exists("config/mysql.json"):
            with open('mysql.json', 'r') as f:
                json_stuff = json.load(f)
                self.host = json_stuff["host"]
                self. user = json_stuff["user"]
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
        sql = "INSERT INTO " + self.tablename + "(time, content, attachement, membername, memberid, guildid, guildname, channelid,  \
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
        asyncio.ensure_future(self.sql_connection_stuff(message))
        

def setup(client):
    client.add_cog(Events(client))
