import discord
from discord.ext import commands
import sqlite3



class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cc (self, ctx, command_name, *,output='\0'):
        """Add or response to a custom command"""
        admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
        conn = sqlite3.connect("customCommands.db")
        cur = conn.cursor()
        command_name = command_name.lower()
        if command_name == 'delete':
            if (admin_role in ctx.author.roles):
                c = f"SELECT COUNT(*) FROM CC WHERE command= '{output}'"
                count = cur.execute(c).fetchall()[0][0]
                if count != 0:
                    q = f"DELETE FROM CC WHERE command = '{output}'"
                    cur.execute(q)
                    conn.commit()
                    cur.close()
                    await ctx.channel.send(f"De command '{output}' is verwijderd!")
                else:
                    await ctx.channel.send("Sorry, deze command bestaat niet, probeer het alsjeblieft opnieuw!")
        elif (cur.execute(f"SELECT COUNT(*) FROM CC WHERE command='{command_name}'").fetchall()[0][0] != 0):
            await ctx.channel.send(cur.execute(f"SELECT response FROM CC WHERE command='{command_name}'").fetchall()[0][0])
        else:
            if (output == '\0'):
                embed = discord.Embed(color=discord.Color.green())
                message = """
                Voer alsjeblieft een geldige invoer in voor de deze command. 
                Probeer je geen command te maken? Controleer dan of de command die je probeert uit te voeren bestaat met: '.cclist' 
                """
                embed.add_field(name="CC - Foutieve command", value=message)
                await ctx.channel.send(embed=embed)
            q = f"INSERT INTO CC (command, response) VALUES ('{command_name}','{output}')"
            cur.execute(q)
            conn.commit()
            cur.close()
            await ctx.channel.send(f"Succefully created the command '.cc {command_name}'")
        conn.close()

    @commands.command()
    async def cclist(self, ctx):
        """Lists all custom commands made"""
        embed = discord.Embed(color=discord.Color.green())
        conn = sqlite3.connect('customCommands.db')
        cur = conn.cursor()
        cmds = cur.execute("SELECT command, response FROM CC").fetchall()
        count = 1
        for command in cmds:
            embed.add_field(name=f"{count}. "+str(command[0]),value=command[1],inline=True)
            count += 1
        await ctx.channel.send(embed=embed)

    

        
