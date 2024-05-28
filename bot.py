#!/usr/bin/env python3
""" Example bot.py """
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the .env file


class MyBotClient(commands.Bot):
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

    async def on_error(self, event, *args, **kwargs):
        """ When an error occurs """
        with open('err.log', 'a', encoding='utf-8') as f:
            if event == 'on_message':
                f.write(f"Unhandled message: {args[0]}\n")
            else:
                raise discord.DiscordException


class MyCog(commands.Cog):
    """ Custom cog """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test_command(self, ctx):
        """ Test command """
        await ctx.send('Test command executed!')


async def main():
    """ Main function """
    async with MyBotClient(
        intents=discord.Intents.all(),
        command_prefix="!"
    ) as bot:
        await bot.add_cog(MyCog(bot))
        await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
