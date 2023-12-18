import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import sqlite3
import random 

conn = sqlite3.connect("Ampel.db")
cur = conn.cursor()

def has_eco_account(id):
    q = f"SELECT COUNT(*) FROM economic WHERE user_id = '{id}'"
    c = cur.execute(q)
    r = c.fetchall()
    if r[0][0] == 0:
        return False
    return True

class money_transfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    
    @cooldown(1, 600, BucketType.user)
    @commands.command()
    async def steel(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            embed = discord.Embed(title="Jij boefje", description="Je mag niet van jezelf stelen", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            if (has_eco_account(ctx.author.id)):
                if(has_eco_account(user.id)):
                    cur = conn.cursor()
                    q = f"""SELECT bal FROM economic WHERE user_id = '{user.id}'"""
                    result = cur.execute(q)
                    victim_amounts = result.fetchall()
                    victim_amount = victim_amounts[0][0]
                    u = f"""SELECT bal FROM economic WHERE user_id = '{ctx.author.id}'"""
                    result2 = cur.execute(u)
                    own_amounts = result2.fetchall()
                    own_amount = own_amounts[0][0]
                    embed = discord.Embed(title="Roof", color=discord.Color.purple())
                    
                    if(random.randint(1,100) >= 45):
                        amount = random.randint(0,int(victim_amount/5))
                        embed.add_field(name="Status", value=f"Een prachtige roof met een buit van €{amount}. {user.mention} zal vast niet blij zijn!", inline=False)
                        new_victim_amount = victim_amount - amount
                        new_own_amount = own_amount + amount
                        q2 = f"""UPDATE economic SET bal = {new_victim_amount} WHERE user_id = '{user.id}'"""
                        u2 = f"""UPDATE economic SET bal = {new_own_amount} WHERE user_id = '{new_own_amount}'"""
                        cur.execute(q2)
                        cur.execute(u2)
                        embed.add_field(name=f"Nieuw totaal van {ctx.author.name}", value=f"€{new_own_amount}", inline=False)
                        embed.add_field(name=f"Nieuw totaal van {user.name}", value=f"€{new_victim_amount}", inline=False)
                    else:
                        amount = random.randint(0,int(own_amount/10))
                        embed.add_field(name="Status", value=f"Je bent gepakt, je betaald €{amount} aan {user.mention} als schadevergoeding")
                        new_victim_amount = victim_amount + amount
                        new_own_amount = own_amount - amount
                        q2 = f"""UPDATE economic SET bal = {new_victim_amount} WHERE user_id = '{user.id}'"""
                        u2 = f"""UPDATE economic SET bal = {new_own_amount} WHERE user_id = '{new_own_amount}'"""
                        cur.execute(q2)
                        cur.execute(u2)
                        embed.add_field(name=f"Nieuw totaal van {ctx.author.name}", value=f"€{new_own_amount}", inline=False)
                        embed.add_field(name=f"Nieuw totaal van {user.name}", value=f"€{new_victim_amount}", inline=False)
                    conn.commit()
                    await ctx.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="Status error", description=f"{user.mention} heeft nog geen account in de economie.", color=discord.Color.red())
                    await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Status error", description=f"{user.mention} heeft nog geen account in de economie.", color=discord.Color.red())
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def geef(self, ctx, user: discord.Member, amount: int):
        if user.id == ctx.author.id:
            embed = discord.Embed(title="Jij boefje", description="Je mag niet van jezelf stelen", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            if (has_eco_account(ctx.author.id)):
                if(has_eco_account(user.id)):
                    cur = conn.cursor()
                    q = f"""SELECT bal FROM economic WHERE user_id = '{user.id}'"""
                    result = cur.execute(q)
                    receivers_amounts = result.fetchall()
                    receivers_amount = receivers_amounts[0][0]
                    u = f"""SELECT bal FROM economic WHERE user_id = '{ctx.author.id}'"""
                    result2 = cur.execute(u)
                    own_amounts = result2.fetchall()
                    own_amount = own_amounts[0][0]
                    embed = discord.Embed(title="Gegund", color=discord.Color.purple(), description=f"Je hebt {user.mention} €{amount} gegeven!")
                    if amount > own_amount:
                        error_embed = discord.Embed(title="Dat kan niet", description="Je kunt niet meer geven dan je hebt!", color=discord.Color.red())
                        ctx.channel.send(embed=error_embed)
                        
                    elif amount < 1:
                        error_embed = discord.Embed(title="Dat kan niet", description="Je kunt niet minder dan 1 euro geven", color=discord.Color.red())
                        ctx.channel.send(embed=error_embed)
                    else:
                        cur.execute(f"UPDATE economic SET bal = {own_amount - amount} WHERE user_id = '{ctx.author.id}'")
                        cur.execute(f"UPDATE economic SET bal = {receivers_amount + amount} WHERE user_id = '{ctx.author.id}'")
                        conn.commit()
                        await ctx.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="Status error", description=f"{user.mention} heeft nog geen account in de economie.", color=discord.Color.red())
                    await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Status error", description=f"{user.mention} heeft nog geen account in de economie.", color=discord.Color.red())
                await ctx.channel.send(embed=embed)



