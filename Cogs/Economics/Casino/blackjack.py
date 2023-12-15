import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import sqlite3
import random
import asyncio


conn = sqlite3.connect("Ampel.db")
cur = conn.cursor()

suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

# Create a list of playing cards in the format "rank of suit"
playing_cards_file_names = [f"{rank}_of_{suit}.png" for suit in suits for rank in ranks]

rank_points = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}

playing_cards = [(f"{rank}_of_{suit}.png", rank_points[rank]) for suit in suits for rank in ranks]


def has_eco_account(id):
    q = f"SELECT COUNT(*) FROM economic WHERE user_id = '{id}'"
    c = cur.execute(q)
    r = c.fetchall()
    if r[0][0] == 0:
        return False
    return True

def points_of_hand(hand):
    total = 0
    for card in hand:
        total+= card[1]
    return total


class blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.max_concurrency(number=1, per=BucketType.user, wait=False)
    @commands.command()
    async def bj(self, ctx, bet: int):

        if(has_eco_account(ctx.author.id)):
            if (bet > 0):
                player_points = 0
                dealers_points =0

                dealers_hand = [random.choice(playing_cards)] # playing_cards = [(card_name, value)]
                players_hand = [random.choice(playing_cards), random.choice(playing_cards)]

                current_player_amount = cur.execute(f"SELECT bal FROM economic WHERE user_id='{ctx.author.id}'").fetchall()[0][0]

                if current_player_amount < bet:
                    embed = discord.Embed(title="Onvoldoende saldo", color=discord.Color.red(), description="Sorry, je bent broke! Je hebt niet genoeg geld. Verlaag je inleg of ga werken ofz 🙄")
                    await ctx.channel.send(embed=embed)
                else:
                
                    player_points = points_of_hand(players_hand)
                    dealers_points = points_of_hand(dealers_hand)
                    """
                    Blackjack rules:
                        1. dealer 1 card and player 2
                        2. Player chooses hit or stay
                        3. If player hits they get another card
                        4. If player stays they win if their hand is higher than the dealer's
                        5. Dealers do a soft 17
                        6. If player wins, their bet gets dubbled. Else they lose their bet
                    """
                    embed=discord.Embed(title="BlackJack!", color=discord.Color.yellow())

                    embed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                    embed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                    embed.add_field(name="Inleg", value=f"Je inleg is €{bet}", inline=False)

                    embed.add_field(name="Hit or stay?", value="✅ is hit, ❌ is stay")

                    #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names

                    message = await ctx.channel.send(embed=embed)

                    reactions = ["✅", "❌"]  # Replace with the emojis you want to use
                    for reaction in reactions:
                        await message.add_reaction(reaction)
                    
                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == message.id

                    try:
                        # Wait for a reaction from the command author
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        reaction = None
                        embed = discord.Embed(title="Niet op tijd!", description="Je moet binnen 60 seconden een reactie geven.", color=discord.Color.red())
                        await ctx.channel.send(embed=embed)
                        return
                    
                    
                    while reaction.emoji == "✅" and points_of_hand(players_hand) < 21:
                        players_hand.append(random.choice(playing_cards))
                        player_points = points_of_hand(players_hand)
                        if player_points < 21:
                            newembed=discord.Embed(title="BlackJack!", color=discord.Color.yellow())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Inleg", value=f"Je inleg is €{bet}", inline=False)

                            newembed.add_field(name="Hit or stay?", value="✅ is hit, ❌ is stay")

                            #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names

                            message = await ctx.channel.send(embed=newembed)

                            reactions = ["✅", "❌"]  # Replace with the emojis you want to use
                            for reaction in reactions:
                                await message.add_reaction(reaction)
                            
                            def check(reaction, user):
                                return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == message.id

                            try:
                                # Wait for a reaction from the command author
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                reaction = None
                                embed = discord.Embed(title="Niet op tijd!", description="Je moet binnen 60 seconden een reactie geven.", color=discord.Color.red())
                                await ctx.channel.send(embed=embed)
                                return
                        elif player_points >21:
                            newembed=discord.Embed(title="Verloren :(", color=discord.Color.red())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Inleg", value=f"Je inleg is €{bet}", inline=False)

                            newembed.add_field(name="Verloren", value="Helaas heb je verloren! Je bent de inleg kwijt!")

                            #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names
                            cur.execute(f"UPDATE economic SET bal = {current_player_amount - bet} WHERE user_id = '{ctx.author.id}'")
                            conn.commit()
                            await ctx.channel.send(embed=newembed) 
                            return 
                        else:
                            newembed=discord.Embed(title="Gewonnen🥳", color=discord.Color.green())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Winst", value=f"Je hebt €{bet * 2} gewonnen!", inline=False)

                            newembed.add_field(name="Gewonnen", value="Gefeliciteerd, je hebt 21! Dit betekend dat je 2x je inleg krijgt!")
                            cur.execute(f"UPDATE economic SET bal = {current_player_amount + bet * 2} WHERE user_id = {ctx.author.id}")
                            conn.commit()
                            await ctx.channel.send(embed=embed)

                            return

                    #Here you are <= 21 and dealer = 1 card
                    if points_of_hand(players_hand) == 21:
                        newembed=discord.Embed(title="Gewonnen🥳", color=discord.Color.green())

                        newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                        newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                        newembed.add_field(name="Winst", value=f"Je hebt €{bet * 2} gewonnen!", inline=False)

                        newembed.add_field(name="Gewonnen", value="Gefeliciteerd, je hebt 21! Dit betekend dat je 2x je inleg krijgt!")
                        cur.execute(f"UPDATE economic SET bal = {current_player_amount + bet * 2} WHERE user_id = {ctx.author.id}")
                        conn.commit()
                        await ctx.channel.send(embed=embed)
                    else:
                        while points_of_hand(dealers_hand) < 17:
                            dealers_hand.append(random.choice(playing_cards))
                        dealers_points = points_of_hand(dealers_hand)
                        
                        if points_of_hand(dealers_hand) == points_of_hand(players_hand):
                            newembed=discord.Embed(title="Gelijkspel", color=discord.Color.yellow())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Winst", value="Je hebt €0 gewonnen!", inline=False)

                            newembed.add_field(name="Gelijkspel", value="Het is gelijkspel, je wint niks. Maar verliest ook niks", inline=False)
                        elif points_of_hand(dealers_hand) > points_of_hand(players_hand) and points_of_hand(dealers_hand) <= 21:
                            newembed=discord.Embed(title="Verloren :(", color=discord.Color.red())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Inleg", value=f"Je inleg is €{bet}", inline=False)

                            newembed.add_field(name="Verloren", value="Helaas heb je verloren! Je bent de inleg kwijt!")

                            #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names
                            cur.execute(f"UPDATE economic SET bal = {current_player_amount - bet} WHERE user_id = '{ctx.author.id}'")
                            conn.commit()
                        else:
                            newembed=discord.Embed(title="Gewonnen🥳", color=discord.Color.green())

                            newembed.add_field(name="Dealers hand!", value=f"Dealer heeft: {dealers_points} punten", inline=False) 
                            newembed.add_field(name="Jou hand!", value=f"Je hebt: {player_points} punten", inline=False)            

                            newembed.add_field(name="Inleg", value=f"Je inleg is €{bet}", inline=False)

                            newembed.add_field(name="Gewonnen", value="Gefeliciteerd, je hebt van de dealer gewonnen. Je hebt nu je inleg verdubbeld.")

                            #reactions = ['Cogs/Economics/Casino/cardspng/king_of_diamonds2.png', 'Cogs/Economics/Casino/cardspng/9_of_spades.png']  # Replace with the actual file names
                            cur.execute(f"UPDATE economic SET bal = {current_player_amount + bet} WHERE user_id = '{ctx.author.id}'")
                            conn.commit()
                        
                        
                        await ctx.channel.send(embed=newembed)
            else:
                embed=discord.Embed(title="Foutieve inleg", description="Je moet minimaal 1 euro inleggen!", color=discord.Color.red())
                await ctx.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Je moet eerst registreren!", description="Je moet eerst registerenen doormiddel van `.start` om gebruit te kunnen maken van het casino", color=discord.Color.red())
            await ctx.channel.send(embed=embed)