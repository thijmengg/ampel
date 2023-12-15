import discord
from discord.ext import commands

help_general_string = """
Commands you can use: \n
.help <command> \t - Om specifieke informatie te krijgen over een command! 
.cc <command_naam> <reactie> \t - Maak een eigen command
.cclist \t - Krijg een complete lijst met alle custom commands en de reacties!
.idee \t - Heb jij een goed idee voor de bot? Of een fout gevonden, volg dan deze link.
.start <index> \t - Registreer je in de Ampel Familie database en start met het spelen van alle spellen.
"""

help_help_string = """
.help <command> \t - Om specifieke informatie te krijgen over een command! Bijvoorbeeld: .help help
"""

help_cc_string = """
.cc <command_naam> <reactie> \t - Maak een eigen command!
Altijd al gedroomd van een eigen command maken, of een bot iets laten zeggen wat hij nu niet doet?. Gebruik dan de .cc command.
.cclist
Show ALL custom made commands!
Voorbeelden:
.cc hallo "Hallo, ik ben AmpelBot!"
.cc Thiago "Wat is hij toch ook zo'n schatje he?"
\n
Beperkingen:
- Op dit moment kan er nog maar één .cc command worden gemaakt met een specieke naam. Dus <command_naam> mag/kan niet twee keer bestaan
- Hij voert geen server acties uit. Dus alleen reacties geven met je eigen input
- Alleen een @admin kan op dit moment jou custom command eruit halen. Let dus goed op wat je doet. Misbruik kan leiden tot een warning en/of een ban.
"""

help_error = """
Oepsiepoepsie het lijkt erop dat er iets fout is gegaan! Controleer de spelling eventjes. En anders raadpleeg een botdeveloper eventjes.
"""
help_start = """
.start \t | Om jezelf aan te melden voor alle databases van Ampel familie. Je hoeft verder niks te doen, alleen .start
.start user \t | Om jezelf handmatig te registreren voor de gebruikers database van de Ampel familie
.start eco \t | Om jezelf handmatig te regisreren voor de economie database, dan kun je ook starten met het spelen van alle economie spellen
"""
help_eco = """
.zoekwerklist \t| Krijg een compleet overzicht met alle mogelijke banen
.zoek_werk <baan> \t| Soliciteer bij een baan, foute spelling = geen baan
.werk \t| Ga werken bij je baan, heb je nog geen baan zoek er dan eerst één, anders wordt het bedelen.
.bal \t| Zie jou balans
.bal <user> \t| Zie de balans van iemand anders
"""

help_casino = """
Alle casino games zijn:
.bj <inleg> \t| Speel blackjack tegen de computer!
"""

help_bj = """
Regels van blackjack (deze versie!):
- De A is 11 punten waard en is niet in te splitsen in een 1 en 11.
- 21 voor jou? Goedzo, je krijgt nu 2x inleg als winst terug.

- Gokverslaafd? Klinkt niet als mijn probleem! (Zolang je het maar bij mij houdt is alles goed <3)
"""
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def help(self, ctx, args='\0'):
        string_embed = discord.Embed(color=discord.Color.green())
        if args=='\0':
            string_embed.add_field(name="Algemeen", value=help_general_string)
        elif args == 'help':
            string_embed.add_field(name="Help - help", value=help_help_string)
        elif args == 'cc':
            string_embed.add_field(name= "Help - Custom Commands", value = help_cc_string)
        elif args == 'start':
            string_embed.add_field(name="Help - start", value=help_start)
        elif args == 'eco':
            string_embed.add_field(name="Help - economie", value=help_eco)
        elif args == 'casino':
            string_embed.add_field(name="Help - Casino", value=help_casino)
        elif args == 'bj':
            string_embed.add_field(name="Help - Blackjack", value=help_bj)
        else:
            string_embed.add_field(name="Help - Error", value = help_error)
        
        
        await ctx.channel.send(embed = string_embed)
