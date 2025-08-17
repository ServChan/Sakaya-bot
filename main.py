import os
import discord
import aiofiles
from discord.ext import commands
from trash import logging as ext_logging

intents=discord.Intents.default()
intents.guilds=True
intents.messages=True
intents.message_content=True

bot=commands.Bot(command_prefix='>',intents=intents,help_command=None)

def safe_log(*a,**k):
    try: ext_logging(*a,**k)
    except Exception as e: print(f'Логирование упало: {e}')

class ChannelCache:
    def __init__(self):
        self.cache={}
    def load_cache(self,guilds):
        self.cache={ch.id:ch.name for g in guilds for ch in g.channels}
        print('Кэш каналов загружен')
    def set(self,channel_id,name):
        self.cache[channel_id]=name
    def remove(self,channel_id):
        self.cache.pop(channel_id,None)
    def get(self,channel_id):
        return self.cache.get(channel_id,'Канал не найден')

channel_cache=ChannelCache()

async def log_to_file(filename,message):
    try:
        async with aiofiles.open(filename,'a',encoding='utf-8') as f:
            await f.write(message+'\n')
    except Exception as e:
        print(f'Ошибка записи в {filename}: {e}')

@bot.event
async def on_ready():
    try:
        channel_cache.load_cache(bot.guilds)
        print(f'Logged in as {bot.user.name}')
    except Exception as e:
        print(f'on_ready ошибка: {e}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    try:
        await bot.process_commands(message)
    except Exception as e:
        print(f'Ошибка обработки команды: {e}')

@bot.event
async def on_message_delete(message):
    try:
        if message.author.bot:
            return
        content=message.content or 'Пустое сообщение'
        mes=f"{message.author.name} удалил сообщение: ```{content}```"
        await message.channel.send(mes)
        safe_log('Deleted',mes)
        await log_to_file('deleted_messages.log',mes)
    except Exception as e:
        print(f'on_message_delete ошибка: {e}')

@bot.event
async def on_message_edit(before,after):
    try:
        if after.author.bot or (before.content==after.content):
            return
        bc=before.content or 'Пусто'
        ac=after.content or 'Пусто'
        mes=f"{before.author.name} изменил сообщение.\n```Ранее - {bc}\nТеперь - {ac}```"
        await before.channel.send(mes)
        safe_log('Edit',mes)
        await log_to_file('edited_messages.log',mes)
    except Exception as e:
        print(f'on_message_edit ошибка: {e}')

@bot.event
async def on_guild_channel_create(channel):
    try:
        channel_cache.set(channel.id,channel.name)
        if isinstance(channel,discord.TextChannel):
            mes='Что это тут у нас? Новый канал?'
            await channel.send(mes)
        safe_log('NEW',f'Channel created - {channel.name}')
    except Exception as e:
        print(f'on_guild_channel_create ошибка: {e}')

@bot.event
async def on_guild_channel_update(before,after):
    try:
        changes=[]
        if before.name!=after.name:
            changes.append(f"[НАЗВАНИЕ]\n    Ранее - {before.name}\n    Теперь - {after.name}")
            channel_cache.set(after.id,after.name)
        if isinstance(before,discord.TextChannel) and isinstance(after,discord.TextChannel):
            if before.topic!=after.topic:
                bt=before.topic or 'Нет описания'
                at=after.topic or 'Нет описания'
                changes.append(f"[ОПИСАНИЕ]\n    Ранее - {bt}\n    Теперь - {at}")
        if changes and isinstance(after,discord.TextChannel):
            mes="А у нас тут ремонт!\n```"+"\n".join(changes)+"```"
            await after.send(mes)
        if changes:
            safe_log('EDIT',f'Channel edited - {after.name}')
    except Exception as e:
        print(f'on_guild_channel_update ошибка: {e}')

@bot.event
async def on_guild_channel_delete(channel):
    try:
        channel_cache.remove(channel.id)
        safe_log('DEL',f'Channel deleted - {getattr(channel,"name","unknown")}')
    except Exception as e:
        print(f'on_guild_channel_delete ошибка: {e}')

@bot.event
async def on_command_error(ctx,error):
    try:
        msg='Ошибка: '+str(error)
        await ctx.send(msg)
        safe_log('CommandError',msg)
    except Exception as e:
        print(f'on_command_error ошибка: {e}')

@bot.command(name='help')
async def _help(ctx):
    try:
        help_message="Доступные команды:\n>hello - Поприветствовать бота.\n>help - Показать это сообщение помощи.\n>get_channel_name <id> - Получить название канала по ID."
        await ctx.send(f"```{help_message}```")
        safe_log('Command','>help')
    except Exception as e:
        print(f'help ошибка: {e}')

@bot.command()
async def get_channel_name(ctx,channel_id:int):
    try:
        name=channel_cache.get(channel_id)
        await ctx.send(f"Название канала: {name}")
        safe_log('Command',f'>get_channel_name {channel_id}')
    except Exception as e:
        print(f'get_channel_name ошибка: {e}')

@bot.command()
async def hello(ctx):
    try:
        await ctx.send('Hello!')
        safe_log('Command','>hello')
    except Exception as e:
        print(f'hello ошибка: {e}')

def _token():
    t=os.getenv('TOKEN')
    if not t: raise RuntimeError('Не задан TOKEN в переменных окружения')
    return t

if __name__=='__main__':
    bot.run(_token())
