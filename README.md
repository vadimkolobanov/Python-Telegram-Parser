
# Парсер чатов и пользователей Telegram

Данный проект представляет собой парсер для чатов и пользователей в Telegram. Он предназначен для извлечения и анализа данных из чатов и профилей пользователей в Telegram.

## Возможности
- Парсинг и извлечение данных из чатов Telegram
- Парсинг и анализ данных профилей пользователей в Telegram
- Сохранение и обновление отработанных чатов

## Установка
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/telegram-parser.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd telegram-parser
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование
Главный файл проекта. Смените ссылку для загрузки другого чата
```python
async def main():
    telegram_api = TelegramAPI(API_ID, API_HASH)
    db = Database('mydatabase.db')
    db.connect()
    db.create_tables()

    await telegram_api.auth()
    chat_https_link = 'https://t.me/learnpythonforfun_chat'

    all_info_about_chat_raw = await telegram_api.get_channel_data_from_link(chat_https_link)
    tasks = [
        telegram_api.get_messages(all_info_about_chat_raw.id),
        telegram_api.get_users(all_info_about_chat_raw.id)
    ]
    result = await asyncio.gather(*tasks)
    all_messages_in_chat_raw = result[0]
    all_users_in_chat_raw = result[1]
    process_messages(all_messages_in_chat_raw, db, all_info_about_chat_raw)
    process_users(all_users_in_chat_raw, all_info_about_chat_raw, db)
    process_channels(all_info_about_chat_raw, db, chat_https_link)
    db.close()
    await telegram_api.stop()


# Запуск основного кода в асинхронной среде
asyncio.run(main())
```

Пожалуйста, ознакомьтесь с полным уроком на [сайте](https://happypython.ru/), чтобы получить более подробную информацию о функциях и использовании парсера.

## Лицензия
Этот проект лицензирован по лицензии MIT. Подробности смотрите в файле [LICENSE](LICENSE).

## Авторы
- Вадим Колобанов - [Профиль на GitHub](https://github.com/vadimkolobanov)
- Большу парсеров и уроков по Python - [Telegram](https://t.me/happypython_team)

Мы хотели бы поблагодарить всех авторов и участников, которые внесли свой вклад в развитие этого проекта.
```
