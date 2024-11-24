import logging

import flet as ft
from dotenv import load_dotenv
import os

from app.components.accounts.add import AddAccount
from app.components.messages.add import AddMessage
from app.components.sending.main import RunSending
from app.components.users.add import AddUser
from config import AppValues
from db.core import SyncCore


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Загрузка переменных из файла .env с выводом отладки
env_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"Loading .env file from: {env_path}")
load_dotenv(env_path)


def main(page: ft.Page):
    SyncCore.init_db(drop=False)

    page.title = "OFApp"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window.width = AppValues.WIDTH_APP
    page.window.height = AppValues.HEIGHT_APP
    page.theme_mode = ft.ThemeMode.LIGHT

    w_run = RunSending(page=page)

    t = ft.Tabs(
        scrollable=False,
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Messages",
                icon=ft.icons.MESSAGE,
                content=AddMessage(page=page, w_run=w_run),
            ),
            ft.Tab(
                text="Accounts",
                icon=ft.icons.VERIFIED_USER,
                content=AddAccount(page=page, w_run=w_run),
            ),
            ft.Tab(
                text="Users",
                icon=ft.icons.SUPERVISED_USER_CIRCLE,
                content=AddUser(page=page, w_run=w_run),
            ),
            ft.Tab(
                text="Sending",
                icon=ft.icons.SEND,
                content=w_run,
            ),
        ],
        expand=1,
    )

    page.add(t)


ft.app(main)
