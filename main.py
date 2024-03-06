import asyncio
from config import API_ID, API_HASH
from database import Database
from push_data_in_database import process_messages, process_users, process_channels
from telegram_factory import TelegramAPI


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
