import os
import discord
from dotenv import load_dotenv

TOKEN = ''
GUILD = ''
load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)

