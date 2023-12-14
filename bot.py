# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands

#Import cogs:
from Cogs.Logic.help import HelpCog
from Cogs.CustomCommands.cc import CustomCommands as CC
from Database.Preperation import Init

intents = discord.Intents.all()



# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
client = commands.Bot(command_prefix='.',intents=intents, help_command=None)




# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@client.event
async def on_ready():
	# PRINTS TO THE CONSOLE THAT THE BOT IS ONLINE.
    await client.add_cog(HelpCog(client))
    await client.add_cog(CC(client))
    await client.add_cog(Init(client))
    print("Ampel family is ready to serve!")
	


	

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run("ODI1MTA2NjY1MTQ5MDM4NjMy.G4SiGr.0yG7FdfGRmnGGh1ypOV33UIL5zSOiHqbUWWxmA")

