import discord
from discord.ext import commands
from datetime import datetime

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.leveldata = {}
        
    @commands.Cog.listener()
    async def on_ready(self):
        dict = {}
        guild = self.client.get_guild(751394357231222885)
        
        #tally up scores per channel
        for channel in guild.channels:
            messages = [message async for message in channel.history(after=datetime.today().replace(day=1))]
        for x in messages:
            if x.author.id in dict: 
                dict[x.author.id] = dict[x.author.id] + 1
            else:
                dict[x.author.id] = 1

    #listens for each message sent and gives xp
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.leveldata:
            self.leveldata[message.author.id] = self.leveldata[message.author.id] +1
        else:
            self.leveldata[message.author.id] = 1
            
    @commands.command()
    async def rank(self, ctx):
        if ctx.author.id in self.leveldata:
            xp = self.leveldata[ctx.author.id]
            rank = list(self.leveldata).index(ctx.author.id)
            xp *= 5
            lvl = 0
            while True:
                if xp < (50 * ((lvl  ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp / (200 * ((1/2) * (lvl))) * 20))
            
            #Embed
            embed = discord.Embed(title="{}'s level stats".format(ctx.author.name), description='', color = 0x397882)
            embed.add_field(name="Name", value=ctx.author.mention, inline=True) 
            embed.add_field(name="XP", value=f"{xp}/{int(200*(1/2))*lvl}", inline=True)
            embed.add_field(name="Level", value=lvl, inline=True)
            embed.add_field(name="Progress Bar [lvl]", value=boxes*":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("You have no rank")


async def setup(client):
    await client.add_cog(levelsys(client))