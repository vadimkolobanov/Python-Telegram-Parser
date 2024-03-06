from raw_telegram_data_sort import MessageProcessor, UserProcessor, ChannelProcessor


def process_messages(message_list, database_instance, chat_data):
    channel_id = chat_data.id
    database_instance.connect()
    for message in message_list:
        processor = MessageProcessor(message)
        message_id = processor.get_message_id()
        sender_id = processor.get_sender_id()
        message_text = processor.get_message_text()
        message_date = processor.get_message_date()
        flag_is_outgoing = processor.is_outgoing()
        flag_is_mentioned = processor.is_mentioned()
        flag_has_media_unread = processor.has_media_unread()
        flag_is_silent = processor.is_silent()
        flag_is_post = processor.is_post()
        reply = processor.get_reply_to_message_id()
        views_count = processor.get_views_count()
        forwards_count = processor.get_forwards_count()

        database_instance.insert_message(message_id=message_id, user_id=sender_id, message=message_text,
                                         date=message_date,
                                         out=flag_is_outgoing, mentioned=flag_is_mentioned,
                                         media_unread=flag_has_media_unread, silent=flag_is_silent, post=flag_is_post,
                                         reply_to=reply, views=views_count, forwards=forwards_count,
                                         channel_id=channel_id)


def process_users(user_list, channel_data, database_instance):
    database_instance.connect()
    for user_data in user_list:
        processor = UserProcessor(user_data)
        user_id = processor.get_user_id()
        access_hash = processor.get_access_hash()
        first_name = processor.get_first_name()
        last_name = processor.get_last_name()
        username = processor.get_username()
        phone = processor.get_phone()
        photo_id = processor.get_photo_id()
        status = processor.get_status()
        channel_id = channel_data.id
        database_instance.insert_user(user_id, access_hash, first_name, last_name, username, phone, photo_id, status,
                                      channel_id)


def process_channels(channel_data, database_instance, link):
    database_instance.connect()
    processor = ChannelProcessor(channel_data)
    channel_id = processor.get_channel_id()
    channel_name = processor.get_channel_name()
    channel_date_created = processor.get_channel_date_created()

    database_instance.insert_channel(channel_id=channel_id, name=channel_name, date_created=channel_date_created,
                                     link=link)
