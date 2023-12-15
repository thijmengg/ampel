import discord
from discord.ext import commands
import sqlite3

class user_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def bal(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(color=discord.Color.green())
        conn = sqlite3.connect("Ampel.db")
        cur = conn.cursor()
        q = f"""
        SELECT bal, job, car, house, phone, education, pc FROM economic WHERE user_id = '{user.id}'
        """
        embed.add_field(name="Gebruiker", value=f"{user.mention}", inline=False)
        try:
            results = cur.execute(q)
            result = results.fetchall()[0]
            print(result)
            embed.add_field(name="Huidig vermogen", value='€'+str(result[0]), inline=False)
            embed.add_field(name="Huidige baan", value=result[1], inline=False)
            embed.add_field(name="Huidige auto", value=result[2], inline=False)
            embed.add_field(name="Huidig huis", value=result[3], inline=False)
            embed.add_field(name="Huidige telefoon", value=result[4], inline=False)
            embed.add_field(name="Hoogst afgeronde opleiding", value=result[5], inline=False)
            embed.add_field(name="Huidige pc", value=result[6], inline=False)
        except Exception:
            embed.add_field(name="Error", value="Deze gebruiker is nog niet gerigistreerd bij onze economie.")
        await ctx.channel.send(embed=embed)

        