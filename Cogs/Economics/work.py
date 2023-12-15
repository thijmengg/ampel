import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import sqlite3
import random

status_rejected = "Helaas, je hebt het niet gehaald!"
status_accepted = "Je hebt het gehaald, je bent nu een "

job_responses_prostitue_reject = ["Je bent zelfs te lelijk voor de straat!"]
job_responses_prostitue_accept = ["Het is in ieder geval snel geld toch?"]
job_responses_accountant_reject = ["Ach joh, wie wilt er nu ook accountant worden?"]
job_responses_accountant_accept = ["MONEY MONEY MONEY, MUST BE FUNNY, IN A RICH MANS WORLD!"]
job_responses_zanger_accept = ["Hij gaat het toch nooit maker... toch?"]

possible_jobs = """
prostituee \t| Verdien tot wel 50 euro \t| Kans om aangenomen te worden = 1/2
accountant \t| Verdien tot wel 150 euro \t| Kans om aangenomen te worden = 1/10
zanger \t | Verdien tot wel 1000 euro per gig | Kans om aangenomen te worden = 100%
"""

def has_eco_account(ctx):
    conn = sqlite3.connect("Ampel.db")
    cur = conn.cursor()
    q = f"SELECT COUNT(*) FROM economic WHERE user_id = {ctx.author.id}"
    if cur.execute(q).fetchall()[0][0] == 0:
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()
    return True

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(1, 300, BucketType.user)
    @commands.command()
    async def werk(self, ctx):
        if(has_eco_account(ctx)):
            embed = discord.Embed(title="Je hebt gewerkt!", color=discord.Color.dark_blue())
            # Connect to database and get user data
            conn = sqlite3.connect("Ampel.db")
            cur = conn.cursor()
            q = f"SELECT job, bal FROM economic WHERE user_id = '{ctx.author.id}'"
            print(ctx.author.id)
            result = cur.execute(q)
            fetched = result.fetchall()
            job = str(fetched[0][0])

            current_amount = fetched[0][1]
            print(current_amount)
            
            if job == 'werkloos':
                earning = random.randint(1,5)
                answers = [f"Je hebt {earning} verdiend!", f"Allememaggies, je hebt gewoon {earning} bij elkaar gebedeld.", f"Je hebt {earning} verdiend. Das toch wel 1 soep!"]
            elif job == 'prostituee':
                earning = random.randint(35, 70)
                answers = [f"Je hebt de laatste stoeptegel nog gekust. En daarmee €{earning} verdiend.", f"Wat zou moffel zeggen als hij ziet dat je met dit werk {earning} verdiend?"]
            elif job == 'accountant':
                earning = random.randint(0,150)
                answers = [f"Die nummertjes verschuiven heeft wel gewerkt ik heb {earning} verdiend!", f"Alle moffels nog aan toe, met dit geld kan ik piertje laten omleggen. Ik heb {earning} verdiend!"]
            elif job =='zanger':
                if (random.randint(1,100) > 95):
                    earning = random.randint(800,1000)
                    answers = [f"<@&{ctx.author.id}> verdiende {earning} met zijn optreden in Las Vegas, wat een moffelaar"]
                elif (random.randint(1,50) > 48):
                    earning = random.randint(400, 500)
                    answers = [f"<@&{ctx.author.id}> verdiende {earning} met zijn optreden in Los Vogos"]

                else:
                    earning = random.randint(10, 100)
                    answers = [f"Wie gooit er bier? Toch €{earning} verdiend voor 5 minuten optreden."]
            new_amount = current_amount + earning
            # Update the users balance
            u = f"UPDATE economic SET bal = {new_amount} WHERE user_id = '{ctx.author.id}'"
            cur.execute(u)
            conn.commit()
            cur.close()
            conn.close()

            #Inform the user about their earnings
            embed.add_field(name="Verdiend", value=random.choice(answers), inline=False)
            embed.add_field(name="Nieuw totaal", value=f"Je hebt nu €{new_amount}!", inline=False)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Nog geen account", description="Je moet eerst een account maken bij economics. Gebruik `.help start` om te kijken hoe.", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
    
    

    @cooldown(1, 900, BucketType.user)
    @commands.command()
    async def zoek_werk(self, ctx, *, job='list'):
        if(has_eco_account(ctx)):
            conn = sqlite3.connect("Ampel.db")
            cur = conn.cursor()
            job = job.lower()
            q = f"""UPDATE economic SET job = '{job}' WHERE user_id = {ctx.author.id}"""
            embed = discord.Embed(title="Je hebt werk gezocht!",color=discord.Color.blue())
            if job == "prostituee":
                chance = random.randint(1,2)
                if chance==1:
                    embed.add_field(name="Prositutie", value=random.choice(job_responses_prostitue_accept), inline=False)
                    embed.add_field(name="Status", value=status_accepted, inline=False)
                    cur.execute(q)
                else:
                    embed.add_field(name="Prositutie", value=random.choice(job_responses_prostitue_reject), inline=False)
                    embed.add_field(name="Status", value=status_rejected, inline=False)                
            elif job == 'accountant':
                chance = random.randint(1,10)
                if chance == 10:
                    embed.add_field(name="Accountant",value=random.choice(job_responses_accountant_accept), inline=False)
                    embed.add_field(name="Status", value=status_accepted, inline=False)
                    cur.execute(q)
                else:
                    embed.add_field(name="Accountant",value=random.choice(job_responses_accountant_reject), inline=False)
                    embed.add_field(name="Status", value=status_rejected, inline=False)
            elif job == 'zanger':
                cur.execute(q)
                embed.add_field(name="Zanger", value=random.choice(job_responses_zanger_accept), inline=False)
                embed.add_field(name="Status", value=status_accepted, inline=False)


            else:
                embed.add_field(name="Niks gevonden", value="Je hebt gezocht maar niks gevonden. Controleer de volgende keer goed de spelling van de banen. Nu maar wachten! 'Het leven is hard, maar weetje wat harder is?'")

            conn.commit()
            cur.close()
            conn.close()
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Nog geen account", description="Je moet eerst een account maken bij economics. Gebruik `.help start` om te kijken hoe.", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        @commands.command()
        async def zoekwerklist(self, ctx):
            embed = discord.Embed(title="Lijst met werk",color=discord.Color.blue())
            embed.add_field(name="Beschikbare banen", value=possible_jobs)
            await ctx.channel.send(embed=embed)
            
    
            


        