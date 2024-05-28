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

    async def on_message(self, message):
        """ When a message is sent """
        if message.author == self.user:
            # Ignore messages from the bot
            return

        # Respond to messages
        # Example: If the message is 'ping', respond with 'pong'
        if message.content == 'ping':
            await message.channel.send('pong')

        # Example: If the message is 'raise-exception', raise an exception
        if message.content == 'raise-exception':
            raise discord.DiscordException

        # Just print the message
        text = f"What's up {message.author.name}? You said: {message.content}"
        await message.channel.send(text)

    async def on_error(self, event, *args, **kwargs):
        """ When an error occurs """
        with open('err.log', 'a', encoding='utf-8') as f:
            if event == 'on_message':
                f.write(f"Unhandled message: {args[0]}\n")
            else:
                raise discord.DiscordException


client = MyBotClient(intents=discord.Intents.all())
client.run(TOKEN)
