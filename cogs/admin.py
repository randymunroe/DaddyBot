import discord
from discord.ext import commands


class AdminCog(commands.Cog, name="Admin Commands"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='screen',
                description="Smashes that 5 key to move the screen up. Requires Admin role.",
                brief="Hit that 5 key.")
    @commands.has_any_role('root','bigham')
    async def screen(self, ctx):
        await ctx.send('5\n5\n5\n5\n5\n5\n5\n5\n5\n5\n5\n5\n5\n5\n5\nGet that shit outta here.')

    @commands.command(name='clear',
                aliases=['purge'],
                description="Purges that wacky shit out of the channel",
                brief="Clear messages out of the channel")
    @commands.has_any_role('root')
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(AdminCog(bot))