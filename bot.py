import asyncio
import discord
import discord.ext
from discord.ext import commands
import json


# Wichs Codierung
# ä=Ã¼
# ö=Ã¶

def start():
    tokengesetzt = input("Ist dein Token gesetzt? (j/n) ")
    if tokengesetzt == "j":
        pass
    else:
        bottoken = {"token": input("Dein Bot Token: ")}
        with open("token.json", "w") as f:
            json.dump(bottoken, f)

    prefixgesetzt = input("Ist dein Bot Prefix gesetzt? (j/n) ")
    if prefixgesetzt == "j":
        pass
    else:
        botprefix = {"prefix": input("Dein Bot Prefix: ")}
        with open("prefix.json", "w") as f:
            json.dump(botprefix, f)


with open('./prefix.json', 'r') as f:
    json_stuff = json.load(f)
    prefix = json_stuff["prefix"]

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

start()


@client.event
async def on_ready():
    print("Yess der bot läuft :)".format(client))
    print("Du bist eingeloggt als {0.user} auf discord.py Version {1}".format(client, discord.__version__))
    print("Der Bot ist zurzeit auf folgenden Server:")
    for guild in client.guilds:
        print("-" + guild.name)
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("SimpleBot by antonstech"), status=discord.Status.online)
        await asyncio.sleep(360)
        await client.change_presence(activity=discord.Game("Moin Meister"), status=discord.Status.online)
        await asyncio.sleep(360)


@client.command()
async def benutzerinfo(ctx, member: discord.Member):
    embed = discord.Embed(title='Benutzerinfo für {}'.format(member.name),
                          description='Benutzerinfo für {}'.format(
                              member.mention),
                          color=0x69E82C)
    embed.add_field(name='Server beigetreten',
                    value=member.joined_at.strftime('%d/%m/%Y'),
                    inline=True)
    embed.add_field(name='Discord beigetreten',
                    value=member.created_at.strftime('%d/%m/%Y'),
                    inline=True)
    embed.add_field(name=f"Rollen ({len(member.roles)})", value=" ".join([role.mention for role in member.roles]))

    rollen = ''
    for role in member.roles:
        if not role.is_default():
            rollen += '{} \r\n'.format(role.mention)
    embed.add_field(name='Höchste Rolle', value=member.top_role.mention, inline=True),
    embed.add_field(name="Benutzer ID", value=member.id, inline=True),
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Benutzerinfo')
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send("Der Ping beträgt derzeit " f"{round(client.latency * 1000)}ms")


def ist_gepinnt(mess):
    return not mess.pinned


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1, check=ist_gepinnt)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send("Du hast keine Berechtigung dazu!")


# Clear Funktion Hinzufügen

with open('token.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

client.run(token)
