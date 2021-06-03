import discord


async def basicerror(ctx):
    embed = discord.Embed(title="Error⚠", colour=discord.Colour.red())
    embed.add_field(name="Something went wrong!", value=f"Please Contact DCGALAXY#9729")
    embed.set_footer(text="Or look for Help on discord.gg/bHQGfxFzhQ  :)")
    await ctx.send(embed=embed)
