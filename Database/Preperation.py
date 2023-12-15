import discord
from discord.ext import commands
import sqlite3



def create_cc_database():
    """Create a database of CCs if it doesn't exist already."""
    print("Creating CC database...")
    con = sqlite3.connect("Ampel.db")
    print("Connection has been made")
    cur = con.cursor()
    print("Cursor available")
    q = """CREATE TABLE IF NOT EXISTS CC (
        cc_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def create_user_database():
    # Create the eco table in the economy database
    db = sqlite3.connect('Ampel.db')
    cursor = db.cursor()
    q = """CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        discord_id INT
    )
    """
    cursor.execute(q)
    db.commit()
    cursor.close()

def create_eco_database():
    db = sqlite3.connect('Ampel.db')
    cursor = db.cursor()
    q = """CREATE TABLE IF NOT EXISTS economic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bal INT DEFAULT 0,
        job TEXT,
        car TEXT,
        house TEXT,
        phone TEXT,
        education TEXT,
        pc TEXT,
        FOREIGN KEY (user_id) REFERENCES users(discord_id) ON UPDATE CASCADE ON DELETE CASCADE ON INSERT CASCADE
    )
    """
    cursor.execute(q)
    db.commit()
    cursor.close()


def insert_user(id, name):
    conn = sqlite3.connect("Ampel.db")
    cur = conn.cursor()
    query = f"SELECT COUNT(*) FROM users WHERE discord_id={id}"
    count = cur.execute(query).fetchall()[0][0]
    
    if count != 0:
        return False
    query = f"INSERT INTO users (name, discord_id) VALUES ('{name}', '{id}')"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return True

def create_economics(id):
    conn = sqlite3.connect("Ampel.db")
    cur = conn.cursor()
    query = f"SELECT COUNT(*) FROM economic WHERE user_id={id}"
    count = cur.execute(query).fetchall()[0][0]
    if count != 0:
        return False
    query = f"INSERT INTO economic (user_id, bal, job, car, house, phone, education, pc) VALUES ({id}, 0, 'werkloos','geen','geen','geen','geen', 'geen')"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return True




def member_is_registered(id):
    conn = sqlite3.connect("Ampel.db")
    cur = conn.cursor()
    query = f"SELECT COUNT(*) FROM users WHERE discord_id='{id}'"
    return_value = cur.execute(query).fetchall()[0][0] != 0
    cur.close()
    conn.close()
    return return_value

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def create_databases(self, ctx, arg='all'):
        """Create the database and tables"""

        if arg == 'cc':
            await ctx.channel.send("Creating CC Database...")
            create_cc_database()
            await ctx.channel.send("Database is created!")
        elif arg == 'all':
            await ctx.channel.send("Creating CC Database...")
            create_cc_database()
            await ctx.channel.send("Creating User Database...")
            create_user_database()
            await ctx.channel.send("Creating Eco Database...")
            create_eco_database()
            await ctx.channel.send("Databases are created!")
        elif arg == 'users':
            await ctx.channel.send("Creating User Database...")
            create_user_database()
            await ctx.channel.send("Database is created!")
        elif arg == 'eco':
            await ctx.channel.send("Creating Eco Database...")
            create_eco_database()
            await ctx.channel.send("Database is created!")
        else:
            await ctx.channel.send(f"Database with name {arg} can't be found. Are you sure it's alright?")
    
    @commands.command(pass_context=True)
    @commands.has_role("Admin")
    async def start(self, ctx, arg='all'):
        """Register user to all databases"""
        # Checking if user already registered in DB
        embed = discord.Embed(color=discord.Color.blue())
        if arg == 'all':
            if(insert_user(ctx.message.author.id, ctx.message.author.name)):
                embed.add_field(name="User - Success", value="user account aangemaakt.")
            else:
                embed.add_field(name="User - Foutje!", value="Helaas is je user account nog niet aangemaakt. Mogelijk heb je er al één!")
            if(create_economics(ctx.author.id)):
                embed.add_field(name="Eco - Success", value="Economie account aangemaakt.")
            else:
                embed.add_field(name="Eco - Foutje!", value="Oeps, er is iets fout gegaan. Mogelijk ben je al geregistreerd bij de economie database!")
        elif arg =='eco':
            if(create_economics(ctx.author.id)):
                embed.add_field(name="Eco -Success", value="Economie account aangemaakt.")
            else:
                embed.add_field(name="Eco - Foutje!", value="Oeps, er is iets fout gegaan. Mogelijk ben je al geregistreerd bji de economie database!\nControleer ook of je al een user account hebt. Om overal voor te registeren gebruik: '.start' ")
        elif arg == 'user':
            if(insert_user(ctx.message.author.id, ctx.message.author.name)):
                embed.add_field(name="User - Success", value="user account aangemaakt.")
            else:
                embed.add_field(name="User - Foutje!", value="Helaas is je user account nog niet aangemaakt. Mogelijk heb je er al één!")
        else:
            embed.add_field(name="ONGELDIGE INPUT", value="Oeps, je hebt een ongeldige input. Probeer deze command nog eens!")

        await ctx.channel.send(embed=embed)            

        
