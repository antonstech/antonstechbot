import discord
from discord.ext import commands
class Wortfilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(message):
	with open("banned_words.json","r") as f:
		ban =json.load(f)
	banned_words = ban[str(message.guild.id)]
	for word in banned_words:
		if word in message.content.lower():
			print(message.content)
			await message.delete()
	await bot.process_commands(message)
  ''' Optionale Commands'''
@commands.command()
@commands.has_permissions(administrator=True)
async def add_forbidden_word(ctx,*words):
	with open("banned_words.json","r") as f:
		ban =json.load(f)
	banned_words = ban[str(ctx.guild.id)]
	for word in words:
		if word in banned_words:
			await ctx.send(f"**{word}** is already banned from being used")
		else:
			banned_words.append(word)
			ban[str(ctx.guild.id)]= banned_words
			with open("banned_words.json","w") as f:
				json.dump(ban,f)
			await ctx.send(f"Successfully added **{word}** to banned words")
	await ctx.message.delete(delay = 5)

@commands.command()
@commands.has_permissions(administrator=True)
async def remove_forbidden_word(ctx,*words):
	with open("banned_words.json","r") as f:
		ban =json.load(f)
	banned_words = ban[str(ctx.guild.id)]
	for word in words:
		if word  not in banned_words:
			await ctx.send(f"**{word}** is not banned from being used")
		else:
			banned_words.remove(word)
			ban[str(ctx.guild.id)]= banned_words
			with open("banned_words.json","w") as f:
				json.dump(ban,f)
			await ctx.send(f"Successfully remove **{word}** from banned words")
	await ctx.message.delete(delay = 5)

@bot.command()
async def forbidden_words(ctx):
	emb = discord.Embed(title="Forbidden words on this server",description="")
	with open("banned_words.json") as f:
		ban = json.load(f)
	banned_words = ban[str(ctx.guild.id)]
	str1 = '\n'.join(banned_words)
	emb.description= "**"+str1+"**"
	await ctx.send(embed=emb)
  
def setup(bot):
    bot.add_cog(mod(bot))
