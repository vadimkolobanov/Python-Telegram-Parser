from datetime import datetime
from typing import Optional

from telethon.tl.types import PeerUser, PeerChannel, UserStatusOffline, UserStatusOnline, UserProfilePhoto, \
    UserProfilePhotoEmpty, MessageReplyHeader


class MessageProcessor:
    def __init__(self, message):
        self.message = message

    def get_message_id(self) -> Optional[int]:
        return getattr(self.message, 'id', None)

    def get_sender_id(self) -> Optional[int]:
        from_id = getattr(self.message, 'from_id', None)
        if from_id:
            if isinstance(from_id, PeerUser):
                return from_id.user_id
            elif isinstance(from_id, PeerChannel):
                return from_id.channel_id
        return None

    def get_message_text(self) -> Optional[str]:
        return getattr(self.message, 'message', None)

    def get_message_date(self) -> Optional[datetime]:
        return getattr(self.message, 'date', None)

    def is_outgoing(self) -> bool:
        return getattr(self.message, 'out', False)

    def is_mentioned(self) -> bool:
        return getattr(self.message, 'mentioned', False)

    def has_media_unread(self) -> bool:
        return getattr(self.message, 'media_unread', False)

    def is_silent(self) -> bool:
        return getattr(self.message, 'silent', False)

    def is_post(self) -> bool:
        return getattr(self.message, 'post', False)

    def get_reply_to_message_id(self) -> Optional[int]:
        reply_to = getattr(self.message, 'reply_to', None)
        if reply_to and isinstance(reply_to, MessageReplyHeader):
            return reply_to.reply_to_msg_id
        return None

    def get_views_count(self) -> Optional[int]:
        return getattr(self.message, 'views', None)

    def get_forwards_count(self) -> Optional[int]:
        return getattr(self.message, 'forwards', None)

class UserProcessor:
    def __init__(self, user):
        self.user = user

    def get_user_id(self):
        return self.user.id

    def get_access_hash(self):
        return self.user.access_hash

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_username(self):
        return self.user.username

    def get_phone(self):
        return self.user.phone

    def get_photo_id(self):
        if self.user.photo and not isinstance(self.user.photo, UserProfilePhotoEmpty):
            return self.user.photo.photo_id
        else:
            return None

    def get_status(self):
        if isinstance(self.user.status, UserStatusOffline):
            return "Offline"
        elif isinstance(self.user.status, UserStatusOnline):
            return "Online"
        else:
            return None


class ChannelProcessor:
    def __init__(self, channel):
        self.channel = channel

    def get_channel_id(self):
        return self.channel.id

    def get_channel_name(self):
        return self.channel.title

    def get_channel_date_created(self):
        return self.channel.date
