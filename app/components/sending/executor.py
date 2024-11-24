import logging
import random
from typing import Optional

from app.of_auth.client import OFAuthClient
from db.orm import SyncORM
from db.schemas import MessageDTO

logger = logging.getLogger(__name__)


class RunExecutor:
    def __init__(self, from_user_email: str, to_user_username: str):
        self.message = None
        self.from_user_email = from_user_email
        self.to_user_username = to_user_username
        self.api_client = OFAuthClient(email=self.from_user_email)

    @staticmethod
    def _get_random_mess() -> Optional[MessageDTO]:
        if messages := SyncORM.get_messages():
            return random.choice(messages)

    def send_comment(self, message=None) -> Optional[int]:
        self.message = message if message else self._get_random_mess()

        if not self.message:
            return None

        logger.info(f"Send message: {self.message.message} to {self.to_user_username}")
        if to_user := self.api_client.get_user(self.to_user_username):
            logger.info(f"To User ID: {to_user['id']}")
            if self.api_client.check_need_subscribe(to_user):
                self.api_client.subscribe_user(to_user["id"])

            if posts := self.api_client.get_posts(to_user["id"]):
                logger.info(f"Find: {len(posts['list'])} posts")
                if self.api_client.check_post_can_comment(posts_data=posts):
                    response = self.api_client.comment_post(
                        self.message.message, post_id=posts["list"][0]["id"]
                    )
                    return posts["list"][0]["id"] if response else None
