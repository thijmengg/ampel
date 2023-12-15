import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown


class cooldown_listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            error_embed = discord.Embed(title="Cooldown active", color=discord.Color.red())
            cd = error.retry_after
            minutes = cd//60
            seconds = cd%60
            error_embed.add_field(name="Wachttijd", value=f"Je kunt dit over {minutes:.0f} minuten en {seconds:.0f} seconden doen")
            await ctx.channel.send(embed=error_embed)
