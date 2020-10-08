import discord
from discord.ext import commands
import os
import json


class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=False)
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cname = "cogs."+cog
        try:
            self.bot.load_extension(cname)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=False)
    @commands.is_owner()
    async def unload_unload(self, ctx, *, cog: str):
        """Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cname = "cogs."+cog
        if cname == "cogs.owner":
            await ctx.send("Don't unload the owner cog dummy!")
            return
        try:
            self.bot.unload_extension(cname)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=False)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        cname = "cogs."+cog
        if cname == "cogs.owner":
            await ctx.send("Don't unload the owner cog dummy!")
            return
        try:
            self.bot.unload_extension(cname)
            self.bot.load_extension(cname)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')
        
    @commands.command(name='filteradd',
                aliases=["fadd"],
                description='Adds word to the filter',
                brief='Add bad words to the filter',
                pass_context=True)
    @commands.is_owner()
    async def fadd(self, ctx, *, word: str):
        if os.path.isfile("filter.json"):
            with open("filter.json", "r") as fr:
                dickfilter = json.load(fr)
        if word not in dickfilter:
            dickfilter.append(word)
            with open('filter.json', 'w') as fr:
                print('Word added to filter')
                json.dump(dickfilter, fr, indent=2)
            await ctx.send(f'"{word}" added to filter.')
        else:
            await ctx.send(f'"{word}"" already in filter!')
        await ctx.message.delete()

    @commands.command(name='filterremove',
                aliases=["frem"],
                description='Removes words from the filter',
                brief='Remove bad words from the filter',
                pass_context=True)
    @commands.is_owner()
    async def frem(self, ctx, *, word: str):
        if os.path.isfile("filter.json"):
            with open("filter.json", "r") as fr:
                dickfilter = json.load(fr)
        if word in dickfilter:
            with open('filter.json', 'w') as fr:
                dickfilter.remove(word)
                json.dump(dickfilter, fr, indent=2)
            await ctx.send(f'"{word}" removed from filter!')
        else:
            await ctx.send(f'"{word}" not found in filter!')
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(OwnerCog(bot))