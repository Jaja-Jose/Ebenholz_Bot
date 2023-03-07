#bot.py

import os
from unicodedata import name
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
import webcrawl


load_dotenv("C:/Users/aguir/Desktop/Program Projects/Jose Aguirre Discord Arknights Bot/bot.env")
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


def finding_name(name_char):
    name_found = webcrawl.find_name(name_char)
    if name_found:
        return True
    else:
        return False


#This function is to format the statistics
def stats_format(name_char):
    op_stats = webcrawl.find_stats(name_char)
    proper_format = f"{name_char} stats at max level (With Trust Bonus)\n\n"
    proper_format += f"HP: {op_stats[1]}\nATTACK: {op_stats[2]}\nDEF: {op_stats[3]}\nRES: {op_stats[4]}"
    return proper_format

#This function is to format the e1art
def e1_format(name_char):
    return webcrawl.find_e1art(name_char)

#This function is to format the e2art
def e2_format(name_char):
    return webcrawl.find_e2art(name_char)


#This function is to give a simple description of the operator
def desc_format(name_char):
    desc_list = webcrawl.find_desc(name_char)
    proper_format = f"{name_char} is a {desc_list[4]} {desc_list[5]} illustrated by {desc_list[3]}.\n"
    proper_format += f"This unit is a {desc_list[0]} star rarity unit"
    proper_format += f" that belongs to the {desc_list[1]} class"
    proper_format += f" within the {desc_list[2]} archetype"
    return proper_format

#This function gives an overview of all previously established functions that describe the operator
def overview_format(name_char):
    overall_format = desc_format(name_char) + "\n\n"
    overall_format += stats_format(name_char) + "\n\n"
    return overall_format



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="Arknights")
async def arknights_info(ctx):


    OG_channel = ctx.channel # This variabe is for the check function
    # INSERT VARIABLE FOR USER CHECK
    OG_user = ctx.author


    failure = "I give up. Leave me alone now"
    introduction = "Which character do you want to know more about?"
    await ctx.send(introduction)

    ark_attr = ["stats", "e1art", "e2art", "describe", "overview"]

    # The following are list variables filled with comments that the bot will randomly select
    # depending on how far you have gone with the bot command
    char_compliments = ["Congrats, this character does exist, what else do you want to know?",
                    "What do you want to know about this character?",
                    "Seriously? This character? Fine, fine. else do you want to know?"]

    char_insults = ["Wrong game. Better luck next time",
                "Do you even play this game? Better luck next time.",
                "What kinda fan are you? No such character exists. Why even bother asking me?"]

    attr_insults = ["No such attribute exists",
                    "Try again, I can't find such an attribute",
                    "I think you might have chosen the wrong game attribute"]


    # This function checks to make sure that the bot responds to the original user in the proper channel
    # that the bot was summoned in
    def check(m):
        # Maybe this might work m.author == OG_user
        return m.channel == OG_channel and m.author == OG_user


    character = await bot.wait_for('message', check = check, timeout = 30)

    
    #Should think about changing this while loop and the next while loop into a separate function
    #chances = guess_again(character.content, ark_chars, char_insults, ctx, check)
    chances = 3
    while finding_name(character) and chances > 1:
        chances -= 1
        await ctx.send(random.choice(char_insults))
        character = await bot.wait_for('message', check = check, timeout = 30)



    if finding_name(character):
        # The bot command ends here if user fails to properly respond 3 times
        await ctx.send(failure)
    else:
        await ctx.send(random.choice(char_compliments))
        await ctx.send("Here are the choices you can choose from:\n")
        await ctx.send(ark_attr)
        attribute = await bot.wait_for('message', check = check, timeout = 30)

        #This is the second while loop that is very similar to the first while loop
        chances = 3
        while attribute.content not in ark_attr and chances > 1:
            chances -=1
            await ctx.send(random.choice(attr_insults)) 
            attribute = await bot.wait_for("message", check = check, timeout = 30)
            

        if attribute.content not in ark_attr:
            # The bot command ends here if user fails to properly respond 3 times
            await ctx.send(failure)
        else:
            # The final answer gets formatted properly and the bot starts webscrapping
            if attribute.content == "stats":
                await ctx.send(stats_format(character.content))
            elif attribute.content == "e1art":
                await ctx.send(e1_format(character.content))
            elif attribute.content == "e2art":
                await ctx.send(e2_format(character.content))
            elif attribute.content == "describe":
                await ctx.send(desc_format(character.content))
            elif attribute.content == "overview":

                op_stats = webcrawl.find_stats(character.content)
                if int(op_stats[0]) < 4:
                    await ctx.send(webcrawl.find_e1art(character.content))
                else:
                    await ctx.send(webcrawl.find_e2art(character.content))
                
                await ctx.send(overview_format(character.content))


bot.run(TOKEN)
