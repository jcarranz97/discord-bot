#!/usr/bin/env python3
""" Example bot.py """
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the .env file


class MyBotClient(discord.Client):
    """ Custom bot client """
    async def on_ready(self):
        """ When the bot is ready """
        print(f'{self.user} has connected to Discord!')
        connected_guilds = len(self.guilds)
        print(f"{self.user} is connected to {connected_guilds} guilds.")
        for guild in self.guilds:
            print(f"  - {guild.name} (ID: {guild.id})")
            for member in guild.members:
                print(f"    - {member.name} (ID: {member.id})")

    async def on_member_join(self, member):
        """ When a member joins the guild """
        print(f"{member.name} joined the guild.")
        await member.create_dm()
        await member.dm_channel.send(
            f"Hi {member.name}, welcome to the this server!"
        )


client = MyBotClient(intents=discord.Intents.all())
client.run(TOKEN)
