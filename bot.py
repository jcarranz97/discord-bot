#!/usr/bin/env python3
""" Example bot.py """
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the .env file

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    """ When the bot is ready """
    print(f'{client.user} has connected to Discord!')
    connected_guilds = len(client.guilds)
    print(f"{client.user} is connected to {connected_guilds} guilds.")
    for guild in client.guilds:
        print(f"  - {guild.name} (ID: {guild.id})")
        for member in guild.members:
            print(f"    - {member.name} (ID: {member.id})")

client.run(TOKEN)
