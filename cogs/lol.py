from discord.ext import commands
import discord
from botlibrary import constants
import requests
from botlibrary import constants
from riotwatcher import LolWatcher


class Lol(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = constants.lol_token
        self.base_url = constants.lol_url

    @commands.command(name="lol")
    async def lol_command(self, ctx, option=None, username=None):

        if option is None:
            embed = discord.Embed(title="League of Legends Statistiken", color=ctx.author.color)
            embed.add_field(name="Alle Befehle:", value="Mach help lol um dir alle Befehle anzeigen zu lassen",
                            inline=False)
            embed.set_thumbnail(
                url="https://www.riotgames.com/darkroom/original/462106d7bcc8d74a57a49411b70c4a92"
                    ":d4bed097ee383e5afad037edb5e5786e/lol-logo-rendered-hi-res.png")
            embed.set_footer(text='antonstech/antonstechbot ({})'.format(constants.VERSION), icon_url='https://i.imgur.com'
                                                                                            '/gFHBoZA.png')
            await ctx.send(embed=embed)

            return

        if option == "level":
            complete_url = self.base_url + "summoner/v4/summoners/by-name/" + username + "?api_key=" + self.api_key
            response = requests.get(complete_url).json()
            channel = ctx.message.channel
            if 0 < response["summonerLevel"] < 3000:
                async with channel.typing():
                    spielerlevel = response["summonerLevel"]
                    profilbild = response["profileIconId"]
                    embed = discord.Embed(title=f"Leauge of Legends Statistiken für {username}",
                                          color=ctx.author.color,
                                          timestamp=ctx.message.created_at, )
                    embed.add_field(name="Level des Spielers:", value=f"**{spielerlevel}**", inline=False)
                    embed.set_thumbnail(
                        url='http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/' + str(profilbild) + '.png')
                await ctx.send(embed=embed)
            else:
                await ctx.send("Spieler wurde nicht gefunden.")

            return

        if option == "rang":
            channel = ctx.message.channel
            try:
                lol_watcher = LolWatcher(self.api_key)
                my_region = 'euw1'
                me = lol_watcher.summoner.by_name(my_region, username)
                my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
                async with channel.typing():
                    if my_ranked_stats:
                        data = my_ranked_stats[0]
                        rang = data["tier"]
                        nummer = data["rank"]
                        punkte = data["leaguePoints"]
                        gewonnen = data["wins"]
                        verloren = data["losses"]
                        neu_in_der_elo = data["freshBlood"]
                        winrate = gewonnen / (gewonnen + verloren) * 100
                        embed = discord.Embed(title=f"Leauge of Legends Ranked Statistiken für {username}",
                                              color=ctx.author.color,
                                              timestamp=ctx.message.created_at, )
                        embed.add_field(name="Rang", value=f"{rang} {nummer}", inline=True)
                        embed.add_field(name="Punkte", value=f"{punkte}", inline=True)
                        embed.add_field(name="Neu in der Elo?", value=f"{neu_in_der_elo}", inline=True)
                        embed.add_field(name="Gewonnen:", value=f"{gewonnen}", inline=True)
                        embed.add_field(name="Verloren:", value=f"{verloren}", inline=True)
                        embed.add_field(name="Winrate", value=f"{round(winrate, 2)}%", inline=True)
                        embed.set_thumbnail(url="https://antonstech.de/" + str(rang) + ".png")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Spieler nicht gefunden oder nicht eingeranked.")
            except:
                await ctx.send("Spieler nicht gefunden oder nicht eingeranked.")


def setup(client):
    client.add_cog(Lol(client))
