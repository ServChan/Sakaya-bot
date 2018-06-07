import discord, config, os, asyncio, time
from discord.ext import commands
from trash import *

bot = commands.Bot(command_prefix='//', description='your description')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)

@bot.event
async def on_message_delete(message):
    m = str(message.content)
    n = str(message.author)
    mes = "```"+n+" удалил сообщение \""+m+"\"```"
    await bot.send_message(message.channel, mes)
    logging("Deleted", mes)

@bot.event
async def on_message_edit(before, after):
    m = str(before.content)
    n = str(before.author)
    ma = str(after.content)
    mes = "```" + n + " изменил сообщение.\nРанее - "+m+"\nТеперь - "+ma+"```"
    await bot.send_message(before.channel, mes)
    logging("Edit", mes)

@bot.command()
async def hello():
    await bot.say('Hello!')
    logging('Command', 'hello')

@bot.command()
async def calc(a:int, oper:str, b:int):
    if oper == "+":
        c = a+b
    elif oper == "*":
        c = a*b
    elif oper == "-":
        c = a-b
    elif oper == "/":
        c = a/b
    else:
        c = 'nothing. Wrong command.'
    await bot.say('Res ' + str(c))
    logging('Command', 'calc, result - ' + str(c))

bot.run(os.getenv(config.bottoken))
