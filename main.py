import discord, os, asyncio, time
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
    n = str(message.author.name)
    mes = n+" удалил сообщение```"+m+"```"
    await bot.send_message(message.channel, mes)
    logging("Deleted", mes)

@bot.event
async def on_message_edit(before, after):
    m = str(before.content)
    n = str(before.author.name)
    ma = str(after.content)
    mes = n + " изменил сообщение.```Ранее - "+m+"\nТеперь - "+ma+"```"
    await bot.send_message(before.channel, mes)
    logging("Edit", mes)

@bot.event
async def on_channel_create(chann):
    name = chann.name
    await bot.send_message(chann, "Что это тут у нас? Новый канал?")

@bot.event
async def on_channel_update(before, after):
    istherebe = 0
    channafter = before.name
    topicafter = before.topic
    channnow = after.name
    topicnow = after.topic
    if channafter != channnow:
        m = "А у нас тут ремонт!```[НАЗВАНИЕ]\n    Ранее - " + channafter + "\n    Теперь - " + channnow + "```"
        await bot.send_message(after, m)
        istherebe = 1
    if topicafter != topicnow:
        if istherebe == 0:
            m = "А у нас тут ремонт!```[ОПИСАНИЕ]\n    Ранее - " + topicafter + "\n    Теперь - " + topicnow + "```"
        elif istherebe == 1:
            m = "```[ОПИСАНИЕ]\n    Ранее - " + topicafter + "\n    Теперь - " + topicnow + "```"
        await bot.send_message(after, m)

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

bot.run(os.getenv("TOKEN"))
