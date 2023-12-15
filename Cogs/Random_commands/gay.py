"""Pak iemands user profile picture en transform het in een gay variant!"""

import discord
from discord.ext import commands

class gay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self, ctx, user : discord.Member):
        pass
