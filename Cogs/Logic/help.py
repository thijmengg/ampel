import discord
from discord.ext import commands

help_general_string = """
Commands you can use: \n
.help <command> \t - Om specifieke informatie te krijgen over een command! 
.cc <command_naam> <reactie> \t - Maak een eigen command
.cclist \t - Krijg een complete lijst met alle custom commands en de reacties!
.idee \t - Heb jij een goed idee voor de bot? Of een fout gevonden, volg dan deze link.
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
        else:
            string_embed.add_field(name="Help - Error", value = help_error)
        
        
        await ctx.channel.send(embed = string_embed)
