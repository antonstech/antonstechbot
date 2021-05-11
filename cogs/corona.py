from discord.ext import commands
import discord
import requests
from botlibrary import constants


class Corona(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="corona", aliases=["covid"])
    async def corona_command(self, ctx, option=None):

        if option is None:
            url = "https://api.corona-zahlen.org/germany"
            response = requests.get(url).json()
            g_url = "https://api.corona-zahlen.org/vaccinations"
            geimpft = requests.get(g_url)
            data = geimpft.json()
            channel = ctx.message.channel
            async with channel.typing():
                insgesamt = response["cases"]
                todegesamt = response["deaths"]
                inzidenz = response["weekIncidence"]
                data = data["data"]
                jetzgeimpft = data["quote"]
                infor = response["r"]
                rwert = infor["value"]
                gesund = response["recovered"]
                embed = discord.Embed(title="Impfen lassen", url="https://antonstech.de/impfung.html",
                                      color=ctx.author.color)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Corona Virus Statistiken für Deutschland",
                                      color=ctx.author.color,
                                      timestamp=ctx.message.created_at)
                embed.add_field(name="Fälle insgesamt", value=f"{insgesamt}")
                embed.add_field(name="Tode insgesamt", value=f"{todegesamt}")
                embed.add_field(name="Gesund", value=f"{gesund}")
                embed.add_field(name="Inzidenz", value=f"{round(inzidenz, 2)}")
                embed.add_field(name="Geimpft", value=f"{round(jetzgeimpft, 2) * 100}%")
                embed.add_field(name="R-Wert", value=f"{rwert}")
                embed.set_footer(text="Mit " + constants.bot_prefix + "corona geimpft gibts mehr zur Impfung")
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Aktuelle Corona Map für Deutschland",
                                      color=ctx.author.color,
                                      timestamp=ctx.message.created_at)
                embed.set_image(url="https://api.corona-zahlen.org/map/districts")
                embed.set_footer(text="Mit " + constants.bot_prefix + "corona geimpft gibts mehr zur Impfung")
                await ctx.send(embed=embed)

        elif option == "geimpft":
            url = "https://api.corona-zahlen.org/vaccinations"
            response = requests.get(url).json()
            channel = ctx.message.channel
            async with channel.typing():
                data = response["data"]
                jetztgeimpft = data["quote"]
                gesamt = data["vaccinated"]
                second = data["secondVaccination"]
                zweite_imfung = second["vaccinated"]
                embed = discord.Embed(title="Impfen lassen", url="https://antonstech.de/impfung.html",
                                      color=ctx.author.color)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Statistiken zur Impfung in Deutschland",
                                      color=ctx.author.color)
                embed.add_field(name="Prozent der Bevölkerung", value=f"{round(jetztgeimpft, 2) * 100}%")
                embed.add_field(name="Anzahl der Geimpften", value=f"{gesamt} Personen", inline=False)
                embed.add_field(name="Zweite Impfung haben bereits erhalten", value=f"{zweite_imfung} Personen")
                await ctx.send(embed=embed)

            return


def setup(client):
    client.add_cog(Corona(client))
