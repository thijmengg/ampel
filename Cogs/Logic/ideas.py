import discord
from discord.ext import commands

class add_invoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def idee(self, ctx):
        embed = discord.Embed(color=discord.Color.green())
        message2 = discord.Embed(title="Klik hier om een issue te maken", url="https://github.com/thijmengg/ampel/issues", color=discord.Color.green())

        roleid = 1184892185544503306
        botdevrole = f"<@&{roleid}>"
        fout_melding=f"""
        OH OH! Je hebt een fout in mij gevonden? Of heb jij nu een spectaculair idee voor de volgende update?
        Maak dan nu een issues aan via de link!
        Mijn maker (vader Thijmen) zal dan kijken naar jou idee of fout en kijken of hij het al kan oplossen.
        Natuurlijk kunnen we niks beloven. Maar zouden jullie ideeën en feedback erg op prijs stellen.
        
        P.S. Kun je nu echt niet via github een issue aanmaken?? Dat is erg vervelend, maar geen probleem. Stuur dan een berichtje naar iemand met de role {botdevrole}
        """
        embed.add_field(name="Issues", value=fout_melding)
        await ctx.channel.send(embed=message2)
        await ctx.channel.send(embed=embed)
