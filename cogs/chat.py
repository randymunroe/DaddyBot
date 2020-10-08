import discord
from discord.ext import commands
import os
import json
import random
    


class ChatCog(commands.Cog, name="Chat Commands"):

    def __init__(self, bot):
        self.bot = bot
    
    #@commands here
    @commands.command(name='level',
                aliases=['lvl'],
                description='Reports your level.',
                brief='Reports your potty words usage level',
                pass_context=True)
    async def level(self, ctx):
        if os.path.isfile('users.json'):
            with open('users.json', 'r') as fp:
                users = json.load(fp)
                user_id=(ctx.message.author.id)
                exp= users[str(user_id)]['xp']
                lvl= users[str(user_id)]['level']
                lvlexp= (lvl * 5) + 5
            await ctx.send(ctx.message.author.mention + " \nLevel: " + str(lvl) + " \n" + "Experience to next level: " + str((lvlexp-exp)))
            return 
        else:
            print('JSON File Error.')
            return 0
    
    @commands.command(name='leaders',        
                description='Report the level of all users.',
                brief='Get level of all users',
                pass_context=True)
    async def leaders(self, ctx):
        if os.path.isfile('users.json'):
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            high_score_list = sorted(users, key=lambda x : users[x].get('level', 0), reverse=True)
            message = '```'
            for number, user in enumerate(high_score_list):
                name = discord.Guild.get_member(ctx.message.guild, int(user))
                if name is not None:
                    nick = name.nick
                else:
                    continue
                if nick == None:
                    nick = name
                if nick is not None:
                    message += '{0}. {1} ({2} : Level {3})\n'.format(number + 1, nick, name, users[user].get('level', 0))
                else:
                    print('unable to parse, idiot')
            message += '```'
            await ctx.send(message)
            return 
        else:
            print('unable to parse.')
            return

    async def user_add_xp(self, user_id: str, xp: int, channel, author):
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id]['xp'] += xp
                lvl= users[user_id]['level']
                exp= users[user_id]['xp']
                lvlexp= (lvl * 5) + 5
                if exp >= lvlexp:
                    lvl += 1
                    exp -= lvlexp
                    users[user_id]['level'] = lvl
                    users[user_id]['xp'] = exp
                    await channel.send('\N{PILE OF POO}  Level up! ' + author.mention + ' is now level ' + str(lvl) + '! \N{PILE OF POO}') #
                with open('users.json', 'w') as fp:
                    print('Add XP Success')
                    json.dump(users, fp, indent=4)
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id] = {}
                users[user_id]['xp'] = xp
                users[user_id]['level'] = 1
                with open('users.json', 'w') as fp:
                    print('Key Error: User and XP Add Success')
                    json.dump(users, fp, indent=4)
        else:
            users = {user_id: {}}
            users[user_id]['xp'] = xp
            users[user_id]['level'] = 1
            with open('users.json', 'w') as fp:
                print('Misc Error: User added at level 1')
                json.dump(users, fp, indent=4)

#----------------------------------------Listener-----------------------------------------------#
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            print('Ignoring bot message')
            return
        
        if message.content.startswith('>') or message.content.startswith('!') or message.content.startswith('?'):
            return
        
        if os.path.isfile("filter.json"):
            count=0
            with open("filter.json", "r") as fd:
                poopfilter = json.load(fd)
                for word in poopfilter:
                    if word in message.content.lower():
                        print('Keyword found in message :', word, message.author)
                        count+=1
                if count > 0:
                    xp = count * random.randint(2,4)
                    await message.add_reaction('\N{PILE OF POO}')
                    await self.user_add_xp(str(message.author.id), xp, message.channel, message.author)
        
#-----------------------------------------Random Interactions-----------------------------------#  

        if "jammed" in message.content.lower():
            chatroll = random.randint(1,100)
            if chatroll > 90:
                await message.channel.send("https://media2.giphy.com/media/4PvP4zij51Lyw/giphy.gif")   
            return   
      


def setup(bot):
    bot.add_cog(ChatCog(bot))