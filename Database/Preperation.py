import discord
from discord.ext import commands
import sqlite3



def create_cc_database():
    """Create a database of CCs if it doesn't exist already."""
    print("Creating CC database...")
    con = sqlite3.connect("customCommands.db")
    print("Connection has been made")
    cur = con.cursor()
    print("Cursor available")
    q = """CREATE TABLE IF NOT EXISTS CC (
        cc_id INT PRIMARY KEY,
        command TEXT NOT NULL UNIQUE,
        response TEXT NOT NULL
    )
    """
    print("Query initiated")
    cur.execute(q)
    print("Query exectuted")
    con.commit()
    print("Query committed")
    cur.close()
    print("Cursed closed\n Done!")
    con.close()




class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    @commands.has_role("BotDev")
    async def create_database(self, ctx, arg):
        """Create the database and tables"""

        if arg == 'cc':
            await ctx.channel.send("Creating CC Database...")
            create_cc_database()
            await ctx.channel.send("Databases are created!")
        else:
            await ctx.channel.send(f"Database with name {arg} can't be found. Are you sure it's alright?")
        
