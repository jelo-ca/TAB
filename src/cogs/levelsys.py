import discord
from discord.ext import commands
import json
from datetime import date, timedelta

json_file = './data/user.json'

def saveData(self):
    with open(json_file, "w") as outfile:
        json.dump(self.leveldata, outfile, indent=4)

def isValid(submission):
    valid_files = [".mp3", ".wax",".m4a",".flac",".mp4",".mkv",".avi",".mov"]
    file = submission.filename.lower()
    
    return any(file.endswith(extension) for extension in valid_files)

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.leveldata = {}
        
        #Parses JSON file for user level data
        with open(json_file) as user_data:
            self.leveldata = json.load(user_data)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Level System Cog loaded")
                
        guild = self.client.get_guild(751394357231222885)

    #listens for each message sent and gives xp
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments and isValid(message.attachments[0]):
            #check if attachment is a valid audio or video file
            
            
            self.leveldata[str(message.author.id)]["xp"] += 10
            saveData(self)
    
    #adds appropriate points when someone reacts to a submission
    @commands.Cog.listener()        
    async def on_reaction_add(self, reaction, user):
        #prevents self voting
        if (int(user.id) == int(reaction.message.author.id)):
            return
        
        #checks if reacted message is a file
        #uses len() because .attachment returns a list
        if len(reaction.message.attachments) and isValid(reaction.message.attachments[0]):
            self.leveldata[str(reaction.message.author.id)]["xp"] += 2
            self.leveldata[str(user.id)]["xp"] += 1
            saveData(self)
        
        
            
    @commands.command()
    async def register(self, ctx):
        if str(ctx.author.id) in self.leveldata:
            await ctx.channel.send("You already have an account!")
        else:
            self.leveldata[str(ctx.author.id)] = {
                "lvl": 0,
                "xp":0,
                "instruments":[],
                "favorites": {},
                "approval": False,
                "cooldown": str(date.today() - timedelta(days=1)),
                "hasPracticed": False,
                "streak":0,
                }; 
            
            print(self.leveldata)
            
            saveData(self)
                
        await ctx.channel.send("Registered Successfully!")
        
    @commands.command()
    async def stats(self, ctx):
        userID = str(ctx.author.id)
        if userID in self.leveldata:
            xp = self.leveldata[userID]["xp"]
            xp *= 5
            lvl = 0
            streak = self.leveldata[userID]["streak"]
            practice = "✅" if self.leveldata[userID]["hasPracticed"] else "❌"
            
            #Multiplies xp 
            while True:
                if xp < (50 * ((lvl  ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp / (200 * ((1/2) * (lvl))) * 20))
            
            #Embed layout 
            embed = discord.Embed(title="{}'s level stats".format(ctx.author.global_name), description='', color = 0x397882)
            embed.add_field(name="Name", value=ctx.author.mention, inline=True) 
            embed.add_field(name="XP", value=f"{xp}/{int(200*(1/2))*lvl}", inline=True)
            embed.add_field(name="Streak", value=f"{streak}  {practice}", inline=True)
            embed.add_field(name=f"Level {lvl}", value=boxes*":notes:" + (20-boxes) * ":heavy_minus_sign:", inline=False)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("You have no rank")

    @commands.command()
    async def practice(self, ctx):
        userID = str(ctx.author.id)
        user_cooldown = self.leveldata[userID]["cooldown"]
        cooldown = str(date.today())
        
        #24 hour cooldown
        if user_cooldown == cooldown:
            await ctx.channel.send("You can only send a practice request once a day")
            return
        
        #break daily streak
        if ((date.today() - date.fromisoformat(user_cooldown)).days > 1):
            self.leveldata[userID]["streak"] = 0
            pass
        
        #resets practice cooldown
        self.leveldata[userID]["cooldown"] = cooldown
        self.leveldata[userID]["approval"] = True
        self.leveldata[userID]["hasPracticed"] = False
        
        saveData(self)
        
        #sends a request for approval as proof of musician's practice
        embed = discord.Embed(title=f"{ctx.author.global_name} is continuing their habit")
        embed.add_field(name="", value="Peer approval needed", inline=True)
        await ctx.channel.send(embed=embed)
            
    @commands.command()
    async def notice(self, ctx, mention: discord.Member = None):
        if mention is None:
            await ctx.channel.send("Please mention a user")
            return
        
        userID = str(ctx.author.id)
        target_ID = str(mention.id)
      
        if(userID == target_ID):
            await ctx.channel.send("Please mention a valid user other than yourself")
            return
        elif(self.leveldata[target_ID]["approval"] == False):
            await ctx.channel.send("User has not sent a request")
            return
        
        #approves user if user has approval request
        self.leveldata[target_ID]["approval"] = False
        self.leveldata[target_ID]["hasPracticed"] = True
        self.leveldata[target_ID]["streak"] += 1
        
        self.leveldata[userID]["xp"] += 2
        self.leveldata[target_ID]["xp"] += 5 + self.leveldata[userID]["streak"]
        
        saveData(self)
        await ctx.channel.send(f":musical_note: {ctx.author.global_name} has noticed {mention.global_name} improvement :clap: :party_popper:")
    
async def setup(client):
    await client.add_cog(levelsys(client))