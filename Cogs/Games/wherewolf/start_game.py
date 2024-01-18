import discord
from discord.ext import commands
import asyncio
import random
from collections import Counter


class start_wherewolf_game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def start_weerwolven(self, ctx):
        """Start a game of werewolf in the dark."""
        MIN_AMOUNT_OF_PLAYERS = 4
        SECONDS = 30
        MAX_PLAYERS = 10
        seconds = SECONDS
        deaths = []
        newembed=discord.Embed(title="Weervolven!", color=discord.Color.yellow())

        newembed.add_field(name="Ben jij klaar voor een spookachtig avontuur?", value="Ik, Ampel Family bot zal jullie onpartijdige wol... leider zijn", inline=False)

        newembed.add_field(name="Doe je mee?", value="Reageer met '✅' om mee te doen!", inline=False)
        
        #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names
        newembed.add_field(name="Tijd om te reageren", value=f"{seconds} seconden!")
        message = await ctx.channel.send(embed=newembed)

        reactions = ["✅", "🐺"]  # Replace with the emojis you want to use
        for reaction in reactions:
            await message.add_reaction(reaction)
        
        def check(reaction, user):
            return str(reaction.emoji) == '✅' and reaction.message.id == message.id and user != self.bot.user

     
        # Wait for reactions from users who reacted with '✅' in the past 90 seconds

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            newembed.set_field_at(2, name="Tijd om te reageren", value=f"{seconds} seconden!")
            await message.edit(embed=newembed)
        


        message = await ctx.channel.fetch_message(message.id)  # Fetch the updated message
        playing_users = []
        for reaction in message.reactions:
            if reaction.emoji == '✅':
                async for user in reaction.users():
                    if user != self.bot.user:
                        playing_users.append(user)

        if len(playing_users) < MIN_AMOUNT_OF_PLAYERS:
            embed = discord.Embed(title="Niet genoeg mensen hebben gereageerd!", description=f"Er moeten binnen {seconds} seconden, minimaal {MIN_AMOUNT_OF_PLAYERS} spelers hebben opgegeven, anders beëindigd het spel!", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return
        
        #Set game variables
        if len(playing_users) <= 4:
            amount_of_wolves = 1
            amount_of_normal_people = len(playing_users) - amount_of_wolves
        elif len(playing_users) <= 8:
            amount_of_wolves = 2
            amount_of_normal_people = len(playing_users) - amount_of_wolves
        elif len(playing_users) <= MAX_PLAYERS:
            amount_of_wolves = 3
            amount_of_normal_people = len(playing_users) - amount_of_wolves
        else:
            embed = discord.Embed(title="Teveel mensen hebben gereageerd!", description=f"Oeps, het lijkt erop dat het spel te populair is geworden. Geen zorgen, je kunt natuurlijk altijd een ronde wachten en zometeen meespelen! Voor nu, is het spel beëindigd. Maximaal aantal spelers is: {MAX_PLAYERS}", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return

        #Update players about the game
        embed = discord.Embed(title="Het spel gaat beginnen", description="Iedereen krijgt een dm toegestuur met zijn/haar rol. De volgende rollen zitten in dit spel.", color=discord.Color.yellow())

        embed.add_field(name="Wolven", value=f"Er is/zijn {amount_of_wolves} wolf/wolven in het spel", inline=False)
        embed.add_field(name="Burgers", value=f"Er zijn {amount_of_normal_people} gewone burgers in het spel", inline=False)
        # embed.add_field(name="Ziener", value="Op dit moment is de ziener nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)
        # embed.add_field(name="Het onschuldige meisje", value="Op dit moment is het onschuldige meisje nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)
        # embed.add_field(name="De jager", value="Op dit moment is de jager nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)
        # embed.add_field(name="Cupido", value="Op dit moment is Cupido nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)
        # embed.add_field(name="De heks", value="Op dit moment is de heks nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)
        # embed.add_field(name="De dief", value="Op dit moment is de dief nog niet beschikbaar, mogelijk wordt deze later toegevoegd", inline=False)

        await ctx.channel.send(embed=embed)
        
        dividing_players = []
        for user_r in playing_users:
            dividing_players.append(user_r)
        player_wolves = []
        player_humans = []

        for i in range(amount_of_wolves):
            choice = random.randint(0, len(dividing_players)-1)
            player_wolves.append(dividing_players[choice])
            dividing_players.pop(choice)
        
        for i in range(amount_of_normal_people):
            choice = random.randint(0, len(dividing_players)-1)
            player_humans.append(dividing_players[choice])
            dividing_players.pop(choice)

        
        embed_human = discord.Embed(color=discord.Color.yellow(), title="Jij bent een burger", description="Jij hebt geen bijzondere gaven. Je enige wapens zijn het vermogen, om het gedrag van andere burgers te analyseren en zodoende weerwolven te identificeren, en de overtuigingskracht, die nodig is om te voorkomen dat een onschuldige burger veroordeeld wordt. ")
        embed_wolf = discord.Embed(color=discord.Color.yellow(), title="Jij bent een wolf!", description="Iedere nacht verslinden zij een burger. Overdag proberen zij hun nachtelijke gedaante te verbergen en zo aan de wraak van de dorpelingen te ontsnappen. Er zijn zaterdagavond waarschijnlijk zo‟n 4 weerwolven in Wakkerdam…")

        for human_user in player_humans:
            await human_user.send(embed=embed_human)
        
        for wolf_user in player_wolves:
            await wolf_user.send(embed=embed_wolf)

        countdown_sec = 15
        countdown_embed = discord.Embed(color=discord.Color.yellow(), title="Ik ga verder over een klein ongeblik, lees nu je rol", description=f"Ik ga verder over: {countdown_sec} seconden")
        message = await ctx.channel.send(embed=countdown_embed)
        while countdown_sec > 0:
            await asyncio.sleep(1)
            countdown_sec -= 1
            countdown_embed = discord.Embed(color=discord.Color.yellow(), title="Ik ga verder over een klein ongeblik, lees nu je rol", description=f"Ik ga verder over: {countdown_sec} seconden")
            await message.edit(embed=countdown_embed)
        
        #Iedereen kent nu zijn/haar rol en het spel kan beginnen!
        #Wat moet er nu nog gebeuren?
        #IMPLEMENTEER VOORBEREIDENDE FASE HIER
        
        #Spelleider roept de dief
        #Spelleider roept cupido
        #Spelleider roept geliefden
            
        #NORMALE FASE
        #De spelleider roept de ziener, niet aanwezig in deze basis versie
        
        #spelleider roept de weerwolven
        while (len(player_wolves) > 0 and len(player_humans) > 2):
        # while (True):
            message = ""
            print(len(playing_users))
            for i in range(len(playing_users)):
                message += f"{i + 1}. {playing_users[i]}\n"
            
            embed = discord.Embed(color=discord.Color.yellow(), title="De weerwolven mogen wakker worden!", description=message)
            embed.add_field(name="Hoe stem je?", value="Door het nummertje in de dm naar deze bot te sturen.", inline=False)
            
            await ctx.channel.send(embed=embed)

            
            #GET VOTE
            # Send a message to the user in DM
            current_votes = []
            for w in player_wolves:
                embed=discord.Embed(color=discord.Color.yellow(), title="Kies alsjeblieft een nummer van de lijst", description="Je hebt in totaal 30 seconden om je stem uit te brengen, andere wolven krijgen te zien wat jij hebt gestemd!")
                for vote in current_votes:
                    embed.add_field(name="Een wolf voor jou heeft gestemd op: ", value=f"{vote} - {playing_users[vote-1].name}", inline=False)
                
                w_message = await w.send(embed=embed)
                w_reactions = ["1️⃣","2️⃣","3️⃣"," 4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟"]  # Replace with the emojis you want to use
                
                for i in range(len(playing_users)):
                    w_reaction = w_reactions[i]
                    await w_message.add_reaction(w_reaction)
            
                def wolf_check(reaction, user):
                    return user == w and str(reaction.emoji) in w_reactions and reaction.message.id == w_message.id

                try:
                    # Wait for a reaction from the command author
                    reaction_of_wolf, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=wolf_check)
                    for r in range(len(w_reactions)):
                        if str(reaction_of_wolf.emoji) == w_reactions[r]:
                            current_votes.append(r+1)
                    
                    vote_embed = discord.Embed(color=discord.Color.green(), title="Je hebt succesvol gestemd!", description=f"Je hebt succesvol op: {str(current_votes[-1])} - {str(playing_users[current_votes[-1]-1].name)} gestemd")
                    await w.send(embed=vote_embed)
                except asyncio.TimeoutError:
                    system_choice = random.randint(0, len(playing_users)-1)
                    embed = discord.Embed(color=discord.Color.red(), title="Je duurde te lang met reageren", description=f"Het systeem heeft voor jou nummer: {str(system_choice+1)} - {str(playing_users[system_choice].name)} gekozen. Let op! Dit kan ook een van je medewolven zijn")
                    current_votes.append(system_choice+1)
                    await w.send(embed=embed)
            
            #All wolves have voted!
            
            # Use Counter to count occurrences
            counter = Counter(current_votes)

            # Find the most common object
            most_common_object = counter.most_common(1)[0][0]
            if(playing_users[most_common_object-1] in player_wolves):
                status = "wolf"
            else:
                status = "burger"
            deaths.append(str(playing_users[most_common_object-1].name))
            embed_voted_out = discord.Embed(color=discord.Color.red(), title="De wolven hebben gegeten!", description=f"Helaas is *{most_common_object} - {str(playing_users[most_common_object-1])}* vermoord! Een klein stilte voor onze: {status}")
            
            if status == 'wolf':
                for i in range(len(player_wolves)):
                    if player_wolves[i] == playing_users[most_common_object-1]:
                        player_wolves.pop(i)
            if status == 'burger':
                for i in range(len(player_humans)):
                    if player_humans[i] == playing_users[most_common_object-1]:
                        player_humans.pop(i)
                

            playing_users.pop(most_common_object-1)
            ctx.channel.send(embed=embed_voted_out)

            #Nu mogen de burgers gaan stemmen om een wolf weg te stemmen
            asyncio.sleep(5)
            

            burgers_embed = discord.Embed(color=discord.Color.blue(), title="Stemmen!", description=f"Alle moffels nog aan toe. Wat is dit nu weer? Onze geliefde {deaths[-1]} is nu gewoon gestorven! Ik moet zeggen ik verdenk zelf: {random.choice(playing_users)} maargoed, ik weet hier ook niet zoveel van af! Tijd om vraak te nemen!")
            message = ""
            for p in range(len(playing_users)):
                message += f"{p+1} - {str(playing_users[p])}\n"
            burgers_embed.add_field("Wie wil jij wegstemmen?", value=message, inline=False)
            msg = await ctx.channel.send(embed=burgers_embed)
            vote_reactions = ["1️⃣","2️⃣","3️⃣"," 4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣", "🔟"]  # Replace with the emojis you want to use
                
            for i in range(len(playing_users)):
                rea = vote_reactions[i]
                await msg.add_reaction(rea)
            
            vote_countdown = 120
            while vote_countdown > 0:
                await asyncio.sleep(1)
                vote_countdown -= 1
                newembed.set_field_at(1, name="Tijd om te reageren", value=f"{vote_countdown} seconden!")
                await message.edit(embed=newembed)
            
            message = await ctx.channel.fetch_message(message.id)  # Fetch the updated message
            voted = []
            for reaction in message.reactions:
                voted.append(len(reaction.users()))
            
            outvoted = voted.index(max(voted))

            if(playing_users[outvoted] not in player_wolves):
                for i in range(len(player_humans)):
                    if player_humans[i] == playing_users[outvoted]:
                        player_humans.pop(i)
                outvoted_embed = discord.Embed(discord.Color.red(), title=f"{str(playing_users[outvoted].name)} was een burger!", description="Stelletje idioten! Dat was een burger! Nu zijn de wolven weer een stap dicterbij de winst!")
            else:
                for i in range(len(player_wolves)):
                    if player_wolves[i] == playing_users[outvoted]:
                        player_wolves.pop(i)
                outvoted_embed = discord.Embed(discord.Color.green(), title=f"{str(playing_users[outvoted].name)} was een wolf!", description=f"Dat is gelukkig één wolf minder! Nog maar {len(player_wolves)} te gaan")
            playing_users.pop(outvoted)
            ctx.channel.send(embed = outvoted_embed)
        
        if(len(player_humans <= 2)):
            win_embed = discord.Embed(discord.Color.red(), title="Wolven hebben gewonnen!", description="De wolven hebben gewonnen")
        else:
            win_embed = discord.Embed(discord.Color.green(), title="Burgers hebben gewonnen!", description="De wolven zijn vermoord!")
        
        ctx.channel.send(embed=win_embed)






