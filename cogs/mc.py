from discord.ext import commands
import discord
import requests
import datetime
from botlibrary import constants
from .errorstuff import error


class Mc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://api.mcsrvstat.us/2/"
        self.prefix = constants.bot_prefix

    @commands.command(name="mc")
    async def mc_command(self, ctx, option=None, arg1=None):

        if option is None:
            embed = discord.Embed(title="Der Mc Command kann dir viele Nützliche Dinge zum Thema Minecraft anzeigen")
            embed.add_field(name="Funktionen:", value="skin, server, name, jar")
            await ctx.send(embed=embed)
            return

        if arg1 is None and option != "jar":
            await ctx.send("Fehler: Gebe etwas an wonach du suchst!")

        elif option == "server":
            complete_url = self.base_url + arg1
            response = requests.get(complete_url).json()
            channel = ctx.message.channel
            async with channel.typing():
                status = response["online"]
                embed = discord.Embed(title="Minecraft Server Stats für " + arg1)
                if status is True:
                    try:
                        modt = response["motd"]
                        beschreibung = modt["clean"]
                        modtbeschreibung = beschreibung[0]
                        spieler = response["players"]
                        spieleronline = spieler["online"]
                        slots = spieler["max"]
                        embed.add_field(name="Beschreibung", value=f"{modtbeschreibung}")
                        embed.add_field(name="Spieler", value=f"{spieleronline} / {slots}")
                        try:
                            version = response["version"]
                            software = response["software"]
                            embed.add_field(name="Version", value=f"{software} {version}")
                        except:
                            embed.add_field(name="Version", value="Info nicht vorhanden")
                        try:
                            mods = response["mods"]
                            modss = mods["names"]
                            if modss != "":
                                embed.set_author(name="Modlist",
                                                 url='https://mcsrvstat.us/server/' + arg1)
                                embed.add_field(name="Modlist", value="Siehe oben links")
                            else:
                                pass
                        except:
                            pass
                        embed.add_field(name="Online?", value="Jap")
                        embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/" + arg1)
                        await ctx.send(embed=embed)
                    except:
                        embed.add_field(name="Test", value="Test123")
                        await ctx.send(embed=embed)
                else:
                    embed.set_footer(text="Der Server ist derzeit nicht online")
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
            return

        elif option == "name":
            embed = discord.Embed(title="Minecraft Namehistory für " + arg1)
            try:
                uuid = "https://api.mojang.com/users/profiles/minecraft/" + arg1
                response = requests.get(uuid).json()
                playeruuid = response["id"]
                namehistory = "https://api.mojang.com/user/profiles/" + playeruuid + "/names"
                response2 = requests.get(namehistory).json()
                try:
                    namen = response2[0]["name"]
                    embed.add_field(name="Namensänderung:", value=f"**{namen}** --> **{arg1}**")
                except:
                    pass
            except:
                embed.add_field(name="Spieler Nicht gefunden",
                                value="Schau mal nach ob du alles richtig geschrieben hast. Und falls es dann immernoch "
                                      "nicht geht Kontaktier bitte den Entwickler des Bots")
            await ctx.send(embed=embed)
            return

        elif option == "jar" and arg1 != None:
            base_url = "https://serverjars.com/api/fetchLatest/"
            response = requests.get(base_url + arg1).json()
            if response["status"] == "success":
                x = response["response"]
                version = x["version"]
                filename = x["file"]
                md5sum = x["md5"]
                date = x["built"]
                date_normal = datetime.datetime.fromtimestamp(int(date)).strftime("%d.%m.%Y")
                embed = discord.Embed(title="Informationen zu " + arg1)
                embed.set_author(name="Download der neusten Version von " + arg1, url="https://serverjars.com/api/" + "fetchJar/" + arg1)
                embed.add_field(name="Version", value=version)
                embed.add_field(name="Release", value=date_normal)
                embed.add_field(name="Dateiname", value=filename)
                embed.add_field(name="md5sum", value=md5sum)
                await ctx.send(embed=embed)
            elif response["status"] == "error":
                errorname = response["error"]["title"]
                errorcode = response["error"]["message"]
                embed = discord.Embed(title=f'Fehler "{errorname}" beim Suchen')
                embed.add_field(name="Fehlercode:", value=errorcode)
                await ctx.send(embed=embed)
            else:
                await error(ctx)

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
                    proxies_end = proxies_end.replace(character, "",)
                bedrock = response["response"]["bedrock"]
                bedrock_end = str(bedrock)
                for character in characters_to_remove:
                    bedrock_end = bedrock_end.replace(character, "")
                embed = discord.Embed(title="Liste aller Minecraft Server Jars")
                embed.add_field(name="Plugin", value=normal_end)
                embed.add_field(name="Netzwerk", value=proxies_end)
                embed.add_field(name="Bedrock", value=bedrock_end)
                embed.set_author(name="Mache " + self.prefix + "mc jar (name) um mehr Infos zu einer Jar zu erhalten")
                embed.set_footer(text="Quelle: ServerJars.com", icon_url="https://papermc.io/forums/uploads/default/optimized/2X/9/94d4bbaf78d05116b6bf42c8de86865d6b2cb2cf_2_500x500.png")
                await ctx.send(embed=embed)
            else:
                await error(ctx)

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
