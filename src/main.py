import os
import discord 
from discord.ext import commands
import asyncio

# import utils
import cogs.levelsys as levelsys
import cogs.musicsheetsys as musicsheetsys

cogs = [levelsys, musicsheetsys]


#loads cogs
async def load():
    for i in range(len(cogs)):
        await cogs[i].setup(client)

#Get token from .env file
TOKEN = os.getenv("DISCORD_TOKEN")

#Constructor Components
intents = discord.Intents.all()
intents.message_content = True
activity = discord.Game(name="the Guitar")

client = commands.Bot(command_prefix='&', intents=intents, activity=activity, status=discord.Status.online)

@client.event
async def on_ready():
    client.activity
    
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    await client.process_commands(message)
    
async def main():
    async with client:
        await load()
        await client.start(TOKEN)
        
asyncio.run(main())