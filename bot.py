import asyncio
import discord
import discord.ext
from discord.ext import commands
import json

# Wichs Codierung
# ä=Ã¼
# ö=Ã¶

bottoken = {"token": input("Dein Bot Token: ")}
with open("config.json", "w") as f:
 json.dump(bottoken, f)
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Du bist eingeloggt als {0.user}".format(client))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(".help für Hilfe"), status=discord.Status.online)
        await asyncio.sleep(360)
        await client.change_presence(activity=discord.Game(".Joint Varo xD"), status=discord.Status.online)
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
    embed.add_field(name='Höchste Rolle', value=member.top_role.mention, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Benutzerinfo')
    await ctx.send(embed=embed)


with open('./config.json', 'r') as f:
    json_stuff = json.load(f)
    token = json_stuff["token"]

client.run(token)
