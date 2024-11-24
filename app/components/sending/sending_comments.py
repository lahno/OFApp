import logging

import flet as ft

from app.components.sending.executor import RunExecutor
from app.of_auth.client import OFAuthClient
from app.utils.helper import start_loader_btn, end_loader_btn
from config import AppValues
from datetime import datetime

from db.orm import SyncORM
from db.schemas import UserDTO, AccountDTO, MessageDTO

logger = logging.getLogger(__name__)


class WidgetsSendComment:
    def __init__(self, page: ft.Page):
        self.page = page
        self.messages = SyncORM.get_messages()
        self.accounts = SyncORM.get_accounts()
        self.users = SyncORM.get_users()
        self.list_messages = (
            ft.ListView(
                controls=[ft.Text(f"{m.id}) {m.message}") for m in self.messages],
                padding=ft.padding.only(left=20, right=20, bottom=20),
                spacing=10,
            )
            if self.messages
            else ft.ListView(
                padding=ft.padding.only(left=20, right=20, bottom=20), spacing=10
            )
        )
        self.list_accounts = (
            ft.ListView(
                controls=[ft.Text(f"{a.id}) {a.email}") for a in self.accounts],
                padding=ft.padding.only(left=20, right=20),
                spacing=10,
            )
            if self.accounts
            else ft.ListView(
                padding=ft.padding.only(left=20, right=20, bottom=20), spacing=10
            )
        )
        self.list_users = (
            ft.ListView(
                controls=[ft.Text(f"{u.id}) {u.username}") for u in self.users],
                padding=ft.padding.only(left=20, right=20),
                spacing=10,
            )
            if self.users
            else ft.ListView(
                padding=ft.padding.only(left=20, right=20, bottom=20), spacing=10
            )
        )
        self.btn_start = ft.ElevatedButton(text="Start sending", on_click=self.start)
        self.btn_clear = ft.ElevatedButton(
            text="Clear Log", on_click=self.clear_log, visible=False
        )
        self.log_column = ft.Column()
        self.info_column = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Column(
                            controls=[
                                ft.Card(
                                    content=ft.Container(
                                        width=AppValues.WIDTH_APP / 2,
                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    title=ft.Text("List accounts:")
                                                ),
                                                self.list_accounts,
                                            ],
                                            spacing=0,
                                        ),
                                        padding=ft.padding.symmetric(vertical=10),
                                    )
                                ),
                                ft.Card(
                                    content=ft.Container(
                                        width=AppValues.WIDTH_APP / 2,
                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    title=ft.Text("List messages:"),
                                                ),
                                                self.list_messages,
                                            ],
                                            spacing=0,
                                        ),
                                        padding=ft.padding.symmetric(vertical=10),
                                    )
                                ),
                            ]
                        ),
                        ft.Card(
                            content=ft.Container(
                                width=AppValues.WIDTH_APP / 2,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            title=ft.Text("List users:"),
                                        ),
                                        self.list_users,
                                    ],
                                    spacing=0,
                                ),
                                padding=ft.padding.symmetric(vertical=10),
                            )
                        ),
                    ],
                    width=AppValues.WIDTH_APP,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            ]
        )
        self.controls = ft.Column(
            [
                ft.Container(
                    content=self.info_column,
                    padding=ft.padding.only(top=20, right=10, left=10),
                ),
                ft.Container(
                    content=self.log_column,
                    padding=ft.padding.only(top=20, right=10, left=10),
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        ft.Row(
                            controls=[
                                self.btn_start,
                                self.btn_clear,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                ),
            ]
        )
        self.count_success_comments = 0
        self.count_failed_comments = 0

    def update(self):
        self.btn_clear.visible = bool(len(self.log_column.controls))
        self.page.update()

    def update_messages(self):
        self.messages = SyncORM.get_messages()
        if self.check_list_models(self.messages, MessageDTO):
            self.list_messages.controls = [
                ft.Text(f"{m.id}) {m.message}") for m in self.messages
            ]
        else:
            self.list_messages.controls = []
        self.update()

    def update_accounts(self):
        self.accounts = SyncORM.get_accounts()
        if self.check_list_models(self.accounts, AccountDTO):
            self.list_accounts.controls = [
                ft.Text(f"{a.id}) {a.email}") for a in self.accounts
            ]
        else:
            self.list_accounts.controls = []
        self.update()

    def update_users(self):
        self.users = SyncORM.get_users()
        if self.check_list_models(self.users, UserDTO):
            self.list_users.controls = [
                ft.Text(f"{u.id}) {u.username}") for u in self.users
            ]
        else:
            self.list_users.controls = []
        self.update()

    def start(self, e):
        start_loader_btn(self, self.btn_start)

        # Проходим по всем аккаунтам в базе
        for account in self.accounts:
            # Создаём объект клиента АПИ
            if of_api_client := OFAuthClient(email=account.email):
                # Если есть в БД список юзеров
                if self.check_list_models(self.users, UserDTO):
                    for user in self.users:
                        # Создаём объект "исполнителя"
                        if executor := RunExecutor(account.email, user.username):
                            # Запускаем процесс отправки комментария на самый первый пост юзера
                            post_id = executor.send_comment()
                            self.count_success_comments += 1 if post_id else 0
                            self.count_failed_comments += 1 if not post_id else 0
                            self.get_new_line(post_id, user.username)
                else:
                    # Получаем всех друзей аккаунта
                    if friends := of_api_client.get_friends():
                        # Проходимся по списку друзей
                        for friend in friends["list"]:
                            # Создаём объект "исполнителя"
                            if executor := RunExecutor(
                                account.email, friend["username"]
                            ):
                                # Запускаем процесс отправки комментария на самый первый пост друга
                                post_id = executor.send_comment()
                                self.count_success_comments += 1 if post_id else 0
                                self.count_failed_comments += 1 if not post_id else 0
                                self.get_new_line(post_id, friend["username"])

        self.page.open(self.get_modal("Complete sending!", True))
        end_loader_btn(self, self.btn_start, content=ft.Text("Start sending"))

    def get_new_line(self, post_id: int | None, username: str):
        now = datetime.now()
        title = (
            f"Comment success send to User: {username}"
            if post_id
            else f"Not send comment to User: {username}"
        )

        logger.info(title)

        btn_url = (
            f"https://onlyfans.com/{post_id}/{username}"
            if post_id
            else f"https://onlyfans.com/{username}"
        )

        icon_status = (
            ft.icons.PLAYLIST_ADD_CHECK_CIRCLE_OUTLINED
            if post_id
            else ft.icons.ERROR_OUTLINE_OUTLINED
        )
        color_status = ft.colors.GREEN if post_id else ft.colors.YELLOW
        self.log_column.controls.append(
            ft.Row(
                [
                    ft.CupertinoListTile(
                        additional_info=ft.Text(
                            now.strftime("%Y-%m-%d %H:%M:%S"), size=12
                        ),
                        leading=ft.Icon(
                            name=icon_status,
                            color=color_status,
                        ),
                        title=ft.Text(title, size=14),
                        subtitle=ft.OutlinedButton(
                            text="Post URL" if post_id else "Profile", url=btn_url
                        ),
                        trailing=ft.Icon(name=ft.cupertino_icons.ALARM, size=12),
                        width=AppValues.WIDTH_APP - 20,
                    )
                ],
                width=AppValues.WIDTH_APP - 20,
            )
        )
        self.update()

    def get_modal(self, message: str, status: bool):
        content = (
            f"Успешных: {self.count_success_comments}\n"
            f"Неудачных: {self.count_failed_comments}"
        )
        return ft.AlertDialog(
            title=ft.Text(message, size=20),
            content=ft.Text(content),
            icon=(
                ft.Icon(ft.icons.INFO_OUTLINED, color=ft.colors.GREEN)
                if status
                else ft.Icon(ft.icons.ERROR_OUTLINED, color=ft.colors.YELLOW)
            ),
        )

    def clear_log(self, e):
        self.log_column.controls.clear()
        self.update()

    @staticmethod
    def check_list_models(list_models, type_object) -> bool:
        if isinstance(list_models, list) and all(
            isinstance(item, type_object) for item in list_models
        ):
            return True
