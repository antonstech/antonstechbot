from discord.ext import commands
import discord
import requests


class Mc(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://api.mcsrvstat.us/2/"

    @commands.command(name="mc")
    async def mc_command(self, ctx, option=None, arg1=None):

        if option is None:
            embed = discord.Embed(title="Der Mc Command kann dir viele Nützliche Dinge zum Thema Minecraft anzeigen")
            embed.add_field(name="Funktionen:", value="skin, server, name")
            await ctx.send(embed=embed)
            return

        if arg1 is None:
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


def setup(client):
    client.add_cog(Mc(client))
