from discord.ext import commands
import discord
import requests
from .errorstuff import basicerror


class Wetter(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = "7d518678abe248fc7de360ba82f9375b"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    @commands.command(name="wetter")
    async def wetter_command(self, ctx, city):
        try:
            complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city + "&lang=de"
            response = requests.get(complete_url).json()
            channel = ctx.message.channel
            if response["cod"] != "404":
                async with channel.typing():
                    y = response["main"]
                    derzeitige_temperatur = y["temp"]
                    derzeitige_temperatur_celsius = str(round(derzeitige_temperatur - 273.15))
                    druck = y["pressure"]
                    luftfeuchtigkeit = y["humidity"]
                    fuehlt_sich_an_wie = y["feels_like"]
                    fuehlt_sich_an_wie_celsius = str(round(fuehlt_sich_an_wie - 273.15))
                    z = response["weather"]
                    symbol = z[0]["icon"]
                    wetter_beschreibung = z[0]["description"]
                    embed = discord.Embed(title=f"Wetter in {city}",
                                          color=ctx.guild.me.top_role.color,
                                          timestamp=ctx.message.created_at, )
                    embed.add_field(name="Beschreibung", value=f"**{wetter_beschreibung}**", inline=False)
                    embed.add_field(name="Temperatur(C)", value=f"**{derzeitige_temperatur_celsius}°C**", inline=False)
                    embed.add_field(name="Fühlt sich an wie(C)", value=f"**{fuehlt_sich_an_wie_celsius}°C**",
                                    inline=False)
                    embed.add_field(name="Luftfeuchtigkeit(%)", value=f"**{luftfeuchtigkeit}%**", inline=False)
                    embed.add_field(name="Luftdruck(hPa)", value=f"**{druck}hPa**", inline=False)
                    embed.set_thumbnail(url="http://openweathermap.org/img/wn/" + symbol + ".png")
                    embed.set_footer(text=f"Angefragt von {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Stadt wurde nicht gefunden.")
        except:
            await basicerror(ctx)


def setup(client):
    client.add_cog(Wetter(client))
