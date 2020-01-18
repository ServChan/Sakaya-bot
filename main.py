import discord, os, asyncio, time
from discord.ext import commands
from trash import *

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)

@bot.event
async def on_message_delete(message):
    if message.author.bot == False:
        m = str(message.content)
        n = str(message.author.name)
        mes = n + " удалил сообщение ```" + m + "```"
        await message.channel.send(mes)
        logging("Deleted", mes)
    else:
        pass

@bot.event
async def on_message_edit(before, after):
    if (after.author.bot == False) and not (before == after):
        m = str(before.content)
        n = str(before.author.name)
        ma = str(after.content)
        mes = n + " изменил сообщение. ```Ранее - " + m + "\nТеперь - " + ma + "```"
        await before.channel.send(mes)
        logging("Edit", mes)
    else:
        pass

@bot.event
async def on_channel_create(chann):
    name = chann.name
    await chann.channel.send("Что это тут у нас? Новый канал?")
    logging("NEW", "Channel created - " + name)

@bot.event
async def on_channel_update(before, after):
    istherebe = 0
    channafter = before.name
    topicafter = before.topic
    channnow = after.name
    topicnow = after.topic
    if channafter != channnow:
        m = "А у нас тут ремонт! ```[НАЗВАНИЕ]\n    Ранее - " + channafter + "\n    Теперь - " + channnow + "```"
        await after.channel.send(m)
        istherebe = 1
    if topicafter != topicnow:
        if istherebe == 0:
            m = "А у нас тут ремонт! ```[ОПИСАНИЕ]\n    Ранее - " + topicafter + "\n    Теперь - " + topicnow + "```"
        elif istherebe == 1:
            m = "```[ОПИСАНИЕ]\n    Ранее - " + topicafter + "\n    Теперь - " + topicnow + "```"
        await after.channel.send(m)
    logging("EDIT", "Channel edited - " + channnow)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    logging('Command', '>hello')

bot.run(os.getenv("TOKEN"))