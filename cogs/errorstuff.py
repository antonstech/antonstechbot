import discord


async def basicerror(ctx):
    embed = discord.Embed(title="Fehler⚠", colour=discord.Colour.red())
    embed.add_field(name="Irgendetwas ist schief gelaufen!", value="Kontaktiere bitte DCGALAXY#9729")
    embed.set_footer(text="oder schau auf discord.gg/bHQGfxFzhQ vorbei :)")
    await ctx.send(embed=embed)
