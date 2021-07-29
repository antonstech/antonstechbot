from discord.ext import commands
import discord
import requests
import datetime
from .errorstuff import basicerror
import bot


class Mc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://api.mcsrvstat.us/2/"

    @commands.command(name="mc")
    async def mc_command(self, ctx, option=None, arg1=None):
        prefixes = bot.get_default_prefix(client=self.client, message=ctx.message)


        if option is None:
            embed = discord.Embed(title="The Mc Command can show you useful Thigs about Minecraft")
            embed.add_field(name="Functions:", value="skin, server, name, jar")
            await ctx.send(embed=embed)

        elif arg1 is None and option != "jar":
            await ctx.send("Error, say what you want bro!")

        elif option == "server":
            complete_url = self.base_url + arg1
            response = requests.get(complete_url).json()
            channel = ctx.message.channel
            async with channel.typing():
                status = response["online"]
                embed = discord.Embed(title="Minecraft Server Stats for " + arg1)
                if status is True:
                    modt = response["motd"]
                    beschreibung = modt["clean"]
                    modtbeschreibung = beschreibung[0]
                    spieler = response["players"]
                    spieleronline = spieler["online"]
                    slots = spieler["max"]
                    embed.add_field(name="Description", value=f"{modtbeschreibung}")
                    embed.add_field(name="Players", value=f"{spieleronline} / {slots}")
                    try:
                        version = response["version"]
                        software = response["software"]
                        embed.add_field(name="Version", value=f"{software} {version}")
                    except:
                        pass
                    try:
                        version = response["version"]
                        embed.add_field(name="Version", value=version)
                    except:
                        embed.add_field(name="Version", value="Unknown")
                    try:
                        mods = response["mods"]
                        modss = mods["names"]
                        if modss != "":
                            embed.set_author(name="Modlist",
                                                 url='https://mcsrvstat.us/server/' + arg1)
                            embed.add_field(name="Modlist", value="See link above")
                        else:
                            pass
                    except:
                        pass
                    embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/" + arg1)
                    if response["debug"]["cachetime"] != 0:
                        unix_time = response["debug"]["cachetime"]
                        time = datetime.datetime.fromtimestamp(int(unix_time)).strftime("%H:%M:%S")
                        embed.set_footer(text=f"The Results are from {time}")
                    else:
                        pass
                    if response["players"]["online"] < 10:
                        try:
                            spielernamen = response["players"]["list"]
                            spielernamen = str(spielernamen)
                            characters_to_remove = "'[]"
                            for character in characters_to_remove:
                                spielernamen = spielernamen.replace(character, "")
                            embed.add_field(name="Playernames:", value=spielernamen)
                        except:
                            pass
                    else:
                        pass
                    await ctx.send(embed=embed)
                else:
                    embed.set_footer(text="The Server is not Online")
                    await ctx.send(embed=embed)
            return

        elif option == "skin":
            uuid = "https://api.mojang.com/users/profiles/minecraft/" + arg1
            response = requests.get(uuid)
            x = response.json()
            playeruuid = x["id"]
            kopf = "https://crafatar.com/avatars/"
            body = "https://crafatar.com/renders/body/"
            embed = discord.Embed(title="Minecraft Skin von " + arg1)
            embed.set_thumbnail(url=kopf + playeruuid + "?size=50")
            embed.set_image(url=body + playeruuid + "?size=512")
            embed.set_author(name="Skin Download", url="https://minotar.net/download/" + arg1)
            await ctx.send(embed=embed)

        elif option == "name":
            embed = discord.Embed(title="Namehistory for " + arg1)
            try:
                uuid = "https://api.mojang.com/users/profiles/minecraft/" + arg1
                response = requests.get(uuid).json()
                playeruuid = response["id"]
                namehistory = "https://api.mojang.com/user/profiles/" + playeruuid + "/names"
                response2 = requests.get(namehistory).json()
                try:
                    namen = response2[0]["name"]
                    embed.add_field(name="Namechanges:", value=f"**{namen}** --> **{arg1}**")
                except:
                    pass
            except:
                embed.add_field(name="Player not Found",
                                value="Look if you spelled him right")
            await ctx.send(embed=embed)
            return

        elif option == "jar" and arg1 is not None:
            base_url = "https://serverjars.com/api/fetchLatest/"
            response = requests.get(base_url + arg1).json()
            if response["status"] == "success":
                x = response["response"]
                version = x["version"]
                filename = x["file"]
                md5sum = x["md5"]
                date = x["built"]
                datestr = str(date)
                datewithoutzero = datestr[:-3]
                datefinallytf = float(datewithoutzero)
                date_normal = datetime.datetime.utcfromtimestamp(datefinallytf).strftime("%d.%m.%Y")
                embed = discord.Embed(title="Information about " + arg1)
                embed.set_author(name="Download the Newest Version of " + arg1,
                                 url="https://serverjars.com/api/" + "fetchJar/" + arg1)
                embed.add_field(name="Version", value=version)
                embed.add_field(name="Release", value=date_normal)
                embed.add_field(name="Filename", value=filename)
                embed.add_field(name="md5sum", value=md5sum)
                await ctx.send(embed=embed)
            elif response["status"] == "error":
                errorname = response["error"]["title"]
                errorcode = response["error"]["message"]
                embed = discord.Embed(title=f'Error "{errorname}" while Searching')
                embed.add_field(name="Errorcode:", value=errorcode)
                await ctx.send(embed=embed)
            else:
                await basicerror(ctx)

        elif option == "jar":
            base_url = "https://serverjars.com/api/"
            response = requests.get(base_url + "fetchTypes/").json()
            characters_to_remove = "'[]"
            if response["status"] == "success":
                normal = response["response"]["servers"]
                normal_end = str(normal)
                for character in characters_to_remove:
                    normal_end = normal_end.replace(character, "")
                proxies = response["response"]["proxies"]
                proxies_end = str(proxies)
                for character in characters_to_remove:
                    proxies_end = proxies_end.replace(character, "", )
                bedrock = response["response"]["bedrock"]
                bedrock_end = str(bedrock)
                for character in characters_to_remove:
                    bedrock_end = bedrock_end.replace(character, "")
                embed = discord.Embed(title="List of all Minecraft Jars")
                embed.add_field(name="Plugin", value=normal_end)
                embed.add_field(name="Netzwerk", value=proxies_end)
                embed.add_field(name="Bedrock", value=bedrock_end)
                embed.set_author(name="Do " + prefixes + "mc jar (name) to get more Infos about a specific Jar")
                embed.set_footer(text="Source: ServerJars.com",
                                 icon_url="https://papermc.io/forums/uploads/default/optimized/2X/9/94d4bbaf78d05116b6bf42c8de86865d6b2cb2cf_2_500x500.png")
                await ctx.send(embed=embed)
            else:
                await basicerror(ctx)

        elif option == "uuid":
            uuid = "https://api.mojang.com/users/profiles/minecraft/" + arg1
            response = requests.get(uuid).json()
            playeruuid = response["id"]
            kopf = "https://crafatar.com/avatars/"
            embed = discord.Embed(title="UUID von " + arg1)
            embed.set_footer(text=f"{playeruuid}", icon_url=kopf + playeruuid)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mc(client))
