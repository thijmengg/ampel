# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands

#Import cogs:
from Cogs.Logic.help import HelpCog
from Cogs.CustomCommands.cc import CustomCommands as CC
from Database.Preperation import Init
from Cogs.Logic.ideas import add_invoice

from get_key import get_key

intents = discord.Intents.all()



# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
client = commands.Bot(command_prefix='.',intents=intents, help_command=None)

announcement = """Mijn lieve vriendjes en vriendinnetjes. Het tijd van de AmpelFamilie bot is dan toch aangebroken!
                    We zijn ONLINE! Vanaf nu 24/7 (eerst een klein proefmaandje) online.
                    Dit betekend dat met .help jullie mij vanaf nu kunnen gebruiken. Hoe gaaf is dat. Een eigen discord bot in deze server DIE WERKT!
                    Op dit moment kan ik nog niet zo veel. Maar dat wil ik gaan uitbreiden. Help je mee? Gebruik .idee om te kijken hoe!"""


# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@client.event
async def on_ready():
	# PRINTS TO THE CONSOLE THAT THE BOT IS ONLINE.

    await client.add_cog(HelpCog(client))
    await client.add_cog(CC(client))
    await client.add_cog(Init(client))
    await client.add_cog(add_invoice(client))
    # embed = discord.Embed(color=discord.Color.gold())
    # embed.add_field(name="SERVER IS ONLINE", value=announcement)
    # await client.get_channel(809840856739479653).send(embed=embed)
    print("Ampel family is ready to serve!")
	


	

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run(get_key())

