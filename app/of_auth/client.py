import logging
import os
import requests
import time
import functools
from dotenv import load_dotenv

# Загрузка переменных из файла .env
load_dotenv()

logger = logging.getLogger(__name__)


def add_delay(delay_seconds: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(delay_seconds)
            return func(*args, **kwargs)

        return wrapper

    return decorator


class OFAuthClient:
    def __init__(
        self,
        email: str,
        base_url="https://ofapi.fly.dev",
        api_key="0x0f_rIkghPns1EhJOj4Shw7KYfMho8CZmqkaP6r",
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            # "Content-Type": "application/json",
            "X-Email": f"{email}",
            "ApiKey": f"{self.api_key}",
        }

        self.me = self.get(endpoint="users/me")
        self.friends = dict

    @add_delay(2)
    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"GET {url} with params {params}")
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    @add_delay(3)
    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"POST {url} with data {data}")
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    @add_delay(3)
    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"PUT {url} with data {data}")
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    @add_delay(3)
    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response) -> dict:
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return response.content
        else:
            logger.error(
                f"Request failed with status {response.status_code}: {response.reason}"
            )
            response.raise_for_status()

    @staticmethod
    def check_post_can_comment(posts_data: dict) -> bool:
        for post in posts_data["list"]:
            if "canComment" in post and post["canComment"]:
                return True

    @staticmethod
    def check_need_subscribe(user_data: dict) -> bool:
        if "canAddSubscriber" in user_data and user_data["canAddSubscriber"]:
            return True

    def get_friends(
        self, user_id: int = None, limit: int = 100, offset: int = 0
    ) -> dict:
        if user_id is None:
            user_id = self.me["id"]

        self.friends = self.get(
            endpoint=f"users/{user_id}/friends?limit={limit}&offset={offset}"
        )
        return self.friends

    def get_user(self, user_name: str) -> dict:
        return self.get(endpoint=f"users/{user_name}")

    def get_posts(
        self,
        user_id: int,
        limit: int = 10,
        order="publish_date_asc",
        skip_users="all",
        format_type="infinite",
        pinned=0,
        counters=1,
    ) -> dict:
        params = {
            "limit": limit,
            "order": order,
            "skip_users": skip_users,
            "format": format_type,
            "pinned": pinned,
            "counters": counters,
        }
        return self.get(endpoint=f"users/{user_id}/posts", params=params)

    def subscribe_user(self, user_id: int) -> dict:
        response = self.post(
            endpoint=f"users/{user_id}/subscribe",
            data={"source": "profile"},
        )
        logger.info(f"subscribe_user: {response=}")
        return response

    def comment_post(self, message: str, post_id: int) -> dict:
        response = self.post(
            endpoint=f"posts/{post_id}/comments",
            data={"text": message, "answerTo": None, "giphyId": None},
        )
        logger.info(f"comment_post: {response=}")
        return response
