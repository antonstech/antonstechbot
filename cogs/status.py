import time
from discord.ext import commands
import os
import psutil
import platform

uname = platform.uname()


class Status(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="status", aliases=["stats", "dash", "dashboard", "übersicht", "performance", "stat"])
    async def mc_command(self, ctx):
        pid = os.getpid()
        process = psutil.Process(pid)
        process.create_time()
        memoryuse = process.memory_full_info()
        await ctx.send(f"```prolog\n"
                       f"Discord Stuff:\n"
                       f"Servers: {len(self.client.guilds)}\n"
                       f"Users: {len(set(self.client.get_all_members()))}\n"
                       "-------\n"
                       f"Bot Performance:\n"
                       f"RAM-Usage: {memoryuse.rss / 1024000} MB \n"
                       f'Running Since: {time.strftime("%d.%m.%Y %H:%M", time.localtime(process.create_time()))}\n'
                       f"Websocket Latency: {round(self.client.latency * 1000)}ms\n"
                       "-------\n"
                       f"System:\n"
                       f"CPU-Usage: {psutil.cpu_percent()}%\n"
                       f"RAM-Usage : {psutil.virtual_memory()[2]}%\n"
                       f"OS: {uname.system} {uname.version}\n"
                       f"Systemarchitecture: {uname.machine}\n"
                       f"```")


def setup(client):
    client.add_cog(Status(client))
