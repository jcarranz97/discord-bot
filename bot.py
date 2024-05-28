#!/usr/bin/env python3
""" Example bot.py """
import os
import asyncio
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from strenum import StrEnum

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the .env file


class Channels(StrEnum):
    """ Enum for channels """
    FORTNITE = "fortnite"


class MyBotClient(commands.Bot):
    """ Custom bot client """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__playing_fornite = []

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

    async def on_voice_state_update(self, member, before, after):
        """ When a member joins or leaves a voice channel """
        # Reference:
        #  - https://discordpy.readthedocs.io/en/stable/api.html#voice
        #  - https://discordpy.readthedocs.io/en/stable/api.html#discord.VoiceState  # noqa
        if before.channel is None:
            print(f"{member.name} joined {after.channel.name}.")
            if after.channel.name == Channels.FORTNITE:
                self.__playing_fornite.append(member)
                print(f"{member.name} is playing Fortnite.")
        elif after.channel is None:
            print(f"{member.name} left {before.channel.name}.")
            if before.channel.name == Channels.FORTNITE.value:
                self.__playing_fornite.remove(member)
                print(f"{member.name} stopped playing Fortnite.")
        else:
            print(f"{member.name} moved from {before.channel.name} to {after.channel.name}.")  # noqa
            if before.channel == Channels.FORTNITE.value:
                self.__playing_fornite.remove(member)
                print(f"{member.name} stopped playing Fortnite.")
            if after.channel == Channels.FORTNITE.value:
                self.__playing_fornite.append(member)
                print(f"{member.name} is playing Fortnite.")

    @property
    async def playing_fortnite(self):
        """ Get the members playing Fortnite """
        return self.__playing_fornite



class LearningCog(commands.Cog):
    """ Custom cog """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test_command(self, ctx):
        """Run the test command

        This command is used to test the bot.
        """
        await ctx.send('Test command executed!')

    @commands.command(name='ping')
    async def ping_command(self, ctx):
        """Run the ping command

        This command is used to test the latency of the bot.
        """
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(name='echo')
    async def echo_command(self, ctx, *, message):
        """Run the echo command

        This command is used to echo a message.
        """
        await ctx.send(message)

    @commands.command(name='choice')
    async def choice_command(self, ctx, *choices):
        """Run the choice command

        This command is used to choose a random choice.
        """
        choice = random.choice(choices)
        await ctx.send(f'I choose: {choice}')

    @commands.command(name='whois')
    async def whois_command(self, ctx, member: discord.Member):
        """Run the whois command

        This command is used to get information about a member.
        """
        await ctx.send(f'The user name is: {member.name}')
        await ctx.send(f'The user ID is: {member.id}')
        await ctx.send(f'The user status is: {member.status}')
        await ctx.send(f'The user joined at: {member.joined_at}')

    @commands.command(name='guess')
    async def guess_command(self, ctx):
        """Run the guess command

        This command is used to guess a number.
        """
        number = random.randint(1, 10)
        await ctx.send('Guess a number between 1 and 10.')

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit()

        guess = await self.bot.wait_for('message', check=check)
        guess = int(guess.content)

        if guess == number:
            await ctx.send('You guessed it right!')
        else:
            await ctx.send(f'You guessed it wrong. It was {number}.')

    @commands.command(name='fortnite')
    async def fortnite_command(self, ctx):
        """Run the Fortnite command

        This command is used to get the members playing Fortnite.
        """
        playing_fortnite = await self.bot.playing_fortnite
        if playing_fortnite:
            await ctx.send('The members playing Fortnite are:')
            for member in playing_fortnite:
                await ctx.send(f' - {member.name}')
        else:
            await ctx.send('No members are playing Fortnite.')


async def main():
    """ Main function """
    async with MyBotClient(
        intents=discord.Intents.all(),
        command_prefix=commands.when_mentioned_or("b!"),
    ) as bot:
        await bot.add_cog(LearningCog(bot))
        await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
