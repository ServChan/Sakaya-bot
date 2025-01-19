import discord
import os
from discord.ext import commands
from trash import logging

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='>', intents=intents)

class ChannelCache:
    """Класс для управления кэшем каналов."""
    def __init__(self):
        self.cache = {}

    def load_cache(self, guilds):
        self.cache = {
            channel.id: channel.name
            for guild in guilds
            for channel in guild.channels
        }
        print("Кэш каналов загружен")

    def get_channel_name(self, channel_id):
        return self.cache.get(channel_id, "Канал не найден")

channel_cache = ChannelCache()

@bot.event
async def on_ready():
    channel_cache.load_cache(bot.guilds)
    print(f'Logged in as {bot.user.name}')

async def log_to_file(filename, message):
    """Асинхронное логирование в файл."""
    async with aiofiles.open(filename, mode='a', encoding='utf-8') as file:
        await file.write(message + '\n')

@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        mes = f"{message.author.name} удалил сообщение: ```{message.content}```"
        await message.channel.send(mes)
        logging("Deleted", mes)
        await log_to_file("deleted_messages.log", mes)

@bot.event
async def on_message_edit(before, after):
    if not after.author.bot and before.content != after.content:
        mes = (
            f"{before.author.name} изменил сообщение.\n"
            f"```Ранее - {before.content}\nТеперь - {after.content}```"
        )
        await before.channel.send(mes)
        logging("Edit", mes)
        await log_to_file("edited_messages.log", mes)

@bot.event
async def on_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        mes = "Что это тут у нас? Новый канал?"
        await channel.send(mes)
        logging("NEW", f"Channel created - {channel.name}")

@bot.event
async def on_channel_update(before, after):
    changes = []

    if before.name != after.name:
        changes.append(f"[НАЗВАНИЕ]\n    Ранее - {before.name}\n    Теперь - {after.name}")

    if before.topic != after.topic:
        changes.append(f"[ОПИСАНИЕ]\n    Ранее - {before.topic or 'Нет описания'}\n    Теперь - {after.topic or 'Нет описания'}")

    if changes:
        mes = "А у нас тут ремонт!\n```" + "\n".join(changes) + "```"
        if isinstance(after, discord.TextChannel):
            await after.send(mes)
        logging("EDIT", f"Channel edited - {after.name}")

@bot.command()
async def help(ctx):
    help_message = (
        "Доступные команды:\n"
        ">hello - Поприветствовать бота.\n"
        ">help - Показать это сообщение помощи.\n"
        ">get_channel_name <id> - Получить название канала по его ID."
    )
    await ctx.send(f"```{help_message}```")
    logging('Command', '>help')

@bot.command()
async def get_channel_name(ctx, channel_id: int):
    channel_name = channel_cache.get_channel_name(channel_id)
    await ctx.send(f"Название канала: {channel_name}")
    logging('Command', f'>get_channel_name {channel_id}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')
    logging('Command', '>hello')

bot.run(os.getenv("TOKEN"))
