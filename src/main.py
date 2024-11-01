import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='&', intents=intents)

@client.command()
async def test(ctx, author):
    print(f"passed")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    await client.process_commands(message)
client.run(TOKEN)