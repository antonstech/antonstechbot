from discord.ext import commands
import discord


class Benutzerinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="benutzerinfo", aliases=["userinfo", "info", "user"])
    async def benutzerinfo_command(self, ctx, member: discord.Member):
        embed = discord.Embed(title='Userinfo for {}'.format(member.name),
                              description='Userinfo for {}'.format(
                                  member.mention),
                              color=0x69E82C)
        embed.add_field(name='Joined Server',
                        value=member.joined_at.strftime('%d/%m/%Y'),
                        inline=True)
        embed.add_field(name='Joined Discord',
                        value=member.created_at.strftime('%d/%m/%Y'),
                        inline=True)
        embed.add_field(name=f"Roles ({len(member.roles)})",
                        value=" ".join([role.mention for role in member.roles]))

        rollen = ''
        for role in member.roles:
            if not role.is_default():
                rollen += '{} \r\n'.format(role.mention)
        embed.add_field(name='Highest Role', value=member.top_role.mention, inline=True),
        embed.add_field(name="User-ID", value=member.id, inline=True),
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text='Userinfo')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Benutzerinfo(client))
