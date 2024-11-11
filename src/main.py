import os
import discord 
from discord.ext import commands
import asyncio

# import utils
import levelsys

cogs = [levelsys]


#loads cogs
async def load():
    for i in range(len(cogs)):
        await cogs[i].setup(client)
    print("cogs loaded")

#Get token from .env file
TOKEN = os.getenv("DISCORD_TOKEN")

#Constructor Components
intents = discord.Intents.all()
intents.message_content = True
activity = discord.Game(name="the Guitar")

client = commands.Bot(command_prefix='&', intents=intents, activity=activity, status=discord.Status.online)

@client.command()
async def mention(ctx):
    await ctx.channel.send(f"{ctx.author.mention}")


@client.command()
async def register(ctx):      
    return

@client.event
async def on_ready():
    client.activity
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    await client.process_commands(message)
    
async def main():
    async with client:
        await load()
        await client.start(TOKEN)
        
asyncio.run(main())