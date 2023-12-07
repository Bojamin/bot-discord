import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os

load_dotenv(".env")
TOKEN = "MTAxOTU5OTE2Nzk2ODAwNjIzNA.GDucKY.Us0h61jZBvNUv23crWDaHsvRz6XcU-kEqE5kkI"

intents=discord.Intents.all()

prefix = './'
bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Bonjour {member.name}, bienvenue sur le serveur de Terre&Humanisme !\nVoici notre e-book : https://formation.terre-humanisme.org/e-book/ \nAinsi que nos différentes ressources https://terre-humanisme.org/ressources/ 🌳 .')

@bot.command(name='contact')
async def msg(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send("https://terre-humanisme.org/contact/")

@bot.command(name='action')
async def msg(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send("https://terre-humanisme.org/agir-avec-nous-pour-lagroecologie/#rejoindre")

@bot.command(name='news')
async def msg(ctx):
    if ctx.author == bot.user:
        return
    else:
        await ctx.send("https://terre-humanisme.org/actualites/")

@bot.event
async def on_message(message):
    if prefix in message.content:
        print("C'est une commande")
        await bot.process_commands(message)
    else:
        with open("words_blacklist.txt") as bf:
            blacklist = [word.strip().lower() for word in bf.readlines()]
        bf.close()

        channel = message.channel
        for word in blacklist:
            if word in message.content:
                bot_message = await channel.send("Votre message contient un mot banni")
                await message.delete()
                await asyncio.sleep(3)
                await bot_message.delete()
                
        await bot.process_commands(message)

#-----------------------------------------Moderation---------------------------------------------------------------#

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Oh non !  Il semblerait qu'il vous manque un argument pour cette commande.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("Oh non ! Il semblerait que vous n'avez pas la permission pour cette commande.")
    if isinstance(error, commands.MissingRole):
        await context.send("Oh non ! Il semblerait que vous n'avez pas la permission pour cette commande.")
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("Oh non ! Il semblerait que je n'ai pas la permission pour cette commande.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("Oh non ! Il semblerait que je n'ai pas la permission pour cette commande.")
    

#|------------------COMMANDS------------------|   
@bot.command()
async def help(message):
    helpC = discord.Embed(title="Bot de Terre et Humanisme \n Guide d'utilisation ", description="Bienvenue sur la fiche d'aide")
    helpC.add_field(name="contact", value="Montre comment contacter l'association.", inline=False)
    helpC.add_field(name="action", value="Montre comment agir avec Terre et Humanisme.", inline=False)
    helpC.add_field(name="news", value="Montre l'actualité de Terre et Humanisme.", inline=False)

    await message.channel.send(embed=helpC)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(context, amount=5):
    await context.channel.purge(limit=amount+1)

@bot.command()
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'Member {member} kicked')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member}  a été banni')

@bot.command()
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await bot.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} a été débanni')
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def softban(context, member : discord.Member, days, reason=None):
    days * 86400 
    await member.ban(reason=reason)
    await context.send(f'{member} a été banni temporairement')
    await asyncio.sleep(days)
    print("Temps pour lever la sanction.")
    await member.unban()
    await context.send(f'{member} La sanction est levée.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def blacklist_add(context, *, word):
    with open("words_blacklist.txt", "a") as f:
        f.write(word+"\n")
    f.close()

    await context.send(f'Le mot "{word}" a été ajouté à la blacklist.')

bot.run(TOKEN)
