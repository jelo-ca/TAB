import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import json

#API Access
import requests

#I used songsterr due to my guitar playing background but soon realized that other musicsheet websites
#such as musescore would've been better in terms of including other instruments
#Songsterr also does not have an official API so beautifulSoup was used to traverse the HTML
#that the url returned
URL = 'https://www.songsterr.com/'

json_file = './data/user.json'

def getData(url, query=None):   
    if query:
        url += f'?pattern={query}'
    response = requests.get(url)        
    #Uses BeautifulSoup to parse as API returns in HTML format
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

class musicsheetsys(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Sheet Cog loaded")
        
    @commands.command()
    async def search(self,ctx, *args):
        embed=discord.Embed(title="Music Sheet Results")
        
        if not args:
            await ctx.channel.send("Search command must have a query")
            return
            
        #%20 is used by the api as spaces in a query search
        query = '%20'.join(args)
            
        soup = getData(URL, query)
        songs = soup.find_all("a", class_="B0cew") #B0cew is the class used within the webpage
        
        # Limits search results to top 5 since too much overloads the embed and may surpass discord text limit
        for i, song in enumerate(songs):
            if i == 5:
                break
            
            title = song.find("div", attrs={"data-field":"name"})
            artist = song.find("div", attrs={"data-field":"artist"})
            link = song['href']
               
            embed.add_field(name=f"{title.text.strip()}", value=f"by {artist.text.strip()} [:musical_score:](https://www.songsterr.com{link})", inline=False)
        
        await ctx.channel.send(embed=embed)
        
    @commands.command()
    async def favorite(self, ctx, args=None):
        if args is None:
            await ctx.channel.send("Please input the songgster link you want to favorite")
        
        if  len(args) > 24 and (args[:25] == "https://www.songsterr.com"):
            
            soup = getData(args)
            title = soup.find("h1", class_="C612su").find("span", attrs={"aria-label":"title"}).text.strip() #B0cew is the class used within the webpage
            
            embed = discord.Embed(title=f"{title}", description="Is this the song you want to favorite?")
            
            view = discord.ui.View()
            
            confirm = discord.ui.Button(label="Confirm", style=discord.ButtonStyle.success)
            async def confirm_callback(interaction: discord.Interaction):
                with open(json_file) as user_data:
                    data = json.load(user_data)
                
                if (title in data[str(ctx.author.id)]["favorites"]):
                    await interaction.response.send_message("Song already in your favorites")
                    return
                
                data[str(ctx.author.id)]["favorites"][f"{title}"]= args
            
                with open(json_file, "w") as outfile:
                    json.dump(data, outfile, indent=4)
                    
                await interaction.response.send_message("Successfully favorited")
            
            confirm.callback = confirm_callback
            view.add_item(confirm)
            
            decline = discord.ui.Button(label="Decline", style=discord.ButtonStyle.danger)
            async def decline_callback(interaction: discord.Interaction):
                await interaction.response.send_message("Oh, ok :(")
                
            
            decline.callback = decline_callback
            view.add_item(decline)
            
            await ctx.channel.send(embed=embed, view=view)
        else:
            await ctx.channel.send("Please input the songgster link you want to favorite")

    @commands.command()
    async def favorites(self, ctx):
        embed=discord.Embed(title="Your Favorites")
        
        with open(json_file, "r") as user_data:
            data = json.load(user_data)
        
        
        if len(data[str(ctx.author.id)]["favorites"]):
            for i, song in enumerate(data[str(ctx.author.id)]["favorites"]):
                if i == 5:
                    break
                
                title = song
                link = data[str(ctx.author.id)]["favorites"][song]
                
                embed.add_field(name=f"{title}", value=f"link: [:musical_note:]({link})", inline=False)   
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("You dont have any favorites")
        
    # @commands.command()
    # async def daily(self, ctx):
    #     embed= discord.Embed(title="Daily Challenge")
    #     embed.add_field(name="Music Sheet", value="https://www.songsterr.com/a/wsa/metallica-master-of-puppets-tab-s455118", inline=True)
    #     await ctx.channel.send(embed=embed)
    
async def setup(client):
    await client.add_cog(musicsheetsys(client))