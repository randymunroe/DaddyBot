import discord
from discord.ext import commands
import os
import json



class GeneralCog(commands.Cog, name="General Commands"):

    def __init__(self, bot):
        self.bot = bot

    #@commands here
    
    @commands.command(name='google',
                description="Googles whatever you want.",
                brief="Googles things.",
                pass_context=True) #google function
    async def google(self, ctx, *, string:str = 'Nul'):
        if string == 'Nul':
            await ctx.send('Use `!google <search query>`')
            return
        url=string
        url+='\n\nhttp://www.google.com/search?q='
        for s in string:       
            if s==' ':                #when the char is a whitespace, replace with "+" in the resultant output
                url+='+'
                continue
            elif s=='?':                #when the char is a "?", replace with url code in the resultant output
                url+='%3F'
                continue
            else:               
                url+=s
        await ctx.send(url)
        await ctx.message.delete()
      
    @commands.command(name='mock',
                description="Mock all the people",
                brief="iS tHiS sTiLl FuNnY?",
                pass_context=True)
    async def mock(self, ctx,*, string:str = 'Nul'):
        if string == 'Nul':
            await ctx.send('Use `!mock <phrase>`')
            return
        out = ''
        caps = False   #flag to see if upper case 
        for s in string:        #string[::-1] reverses it
            if s == ' ':                #when the char is a whitespace, directly add it to the resultant output
                out += ' '
                continue
            if caps:                 #should be uppercase
                out += s.upper() 
                caps = False 
            else:                    #should be lowercase
                out+=s.lower() 
                caps = True       
        out += ''
        await ctx.send(out)
        await ctx.message.delete()    

def setup(bot):
    bot.add_cog(GeneralCog(bot))