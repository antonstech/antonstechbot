from discord.ext import commands
import discord
from botlibrary import constants
import requests
from .errorstuff import basicerror

class Ip(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ipdata = constants.ipdata_token
        self.base_url = constants.ipdata_url

    @commands.command(name="ip")
    async def ip_command(self, ctx, ip):
        try:
            apiurl = "?api-key=" + self.ipdata
            resulturl = self.base_url + ip + apiurl
            response = requests.get(resulturl)
            x = response.json()
            city = x["city"]
            country = x["country_name"]
            flag = x["flag"]
            y = x["asn"]
            asn = y["name"]
            asntype = y["type"]
            postleitzahl = x["postal"]
            kontinent = x["continent_name"]
            embed = discord.Embed(title="IP Informationen zu " + ip)
            embed.set_thumbnail(url=flag)
            embed.add_field(name="Land", value=f"{country}")
            embed.add_field(name="Stadt", value=f"{city}")
            embed.add_field(name="Kontinent", value=f"{kontinent}")
            if postleitzahl is None:
                pass
            else:
                embed.add_field(name="Postleitzahl", value=f"{postleitzahl}")
            embed.add_field(name="Internetanbieter", value=f"{asn}")
            embed.add_field(name="Anbiter-Type", value=f"{asntype}")
            await ctx.send(embed=embed)
            return
        except:
            await basicerror(ctx)



def setup(client):
    client.add_cog(Ip(client))
