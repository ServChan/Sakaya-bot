# Репозиторий не активен.

# Sakaya-bot

Асинхронный Discord-бот на discord.py 2.x с логированием действий и устойчивой обработкой ошибок. 



## Возможности
- Логирование удаления и редактирования сообщений (в канал и в .log файлы)
- Уведомления о создании/редактировании/удалении каналов
- Кэш каналов с быстрым поиском по ID
- Команды: `>hello`, `>help`, `>get_channel_name <id>`

## Требования
- Python 3.10+
- Discord Bot Token с включёнными Privileged Gateway Intents:
  - Server Members не требуется
  - Message Content — **включить** в Dev Portal (Required для чтения текста сообщений)

## Установка
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Настройка
Создайте файл `.env` по образцу:
```
TOKEN=ваш_токен_бота
```

Убедитесь, что в Discord Developer Portal для приложения включён **Message Content Intent**.

## Запуск
```bash
python main.py
```

## Журналы
- `deleted_messages.log`
- `edited_messages.log`

## Деплой
Любая среда, где доступен Python 3.10+ и переменная окружения `TOKEN`. Для systemd:
```
[Unit]
Description=Sakaya-bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/sakaya-bot
ExecStart=/opt/sakaya-bot/.venv/bin/python /opt/sakaya-bot/main.py
Restart=always
Environment=TOKEN=your_token_here

[Install]
WantedBy=multi-user.target
```

