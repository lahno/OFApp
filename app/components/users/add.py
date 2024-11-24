import logging

import flet as ft

from app.components.sending.main import RunSending
from app.components.users.user import User
from app.of_auth.client import OFAuthClient
from app.utils.helper import alert, start_loader_btn, end_loader_btn
from config import AppValues
from db.orm import SyncORM

logger = logging.getLogger(__name__)


class AddUser(ft.Column):
    def __init__(self, page: ft.Page, w_run: RunSending):
        super().__init__()
        self.page = page
        self.w_run = w_run
        self.count_success_add_new_user = 0
        self.count_failed_add_new_user = 0
        self.btn_find_user = ft.FloatingActionButton(
            icon=ft.icons.FIND_IN_PAGE, on_click=self.find_users
        )
        self.new_user = ft.TextField(
            hint_text="Add account username", on_submit=self.add_user, expand=True
        )
        self.user_controls = ft.Column()

        if users := SyncORM.get_users():
            for user in users:
                users = User(
                    username=user.username,
                    user_delete=self.user_delete,
                    u_id=user.id,
                    w_run=self.w_run,
                )
                self.user_controls.controls.append(users)

        self.width = AppValues.WIDTH_APP
        self.controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.btn_find_user,
                        self.new_user,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_user
                        ),
                    ],
                ),
                padding=ft.padding.only(top=20, right=10, left=10),
            ),
            self.user_controls,
        ]

    def find_users(self, e):
        start_loader_btn(self, self.btn_find_user)

        if app_accounts := SyncORM.get_accounts():
            for account in app_accounts:
                if of_api_client := OFAuthClient(email=account.email):
                    if friends_accounts := of_api_client.get_friends():
                        for a in friends_accounts["list"]:
                            new_users_id = None
                            if a["isVerified"]:
                                new_users_id = SyncORM.new_user(username=a["username"])
                                if new_users_id and isinstance(new_users_id, int):
                                    new_users = User(
                                        username=a["username"],
                                        user_delete=self.user_delete,
                                        u_id=new_users_id,
                                        w_run=self.w_run,
                                    )
                                    self.user_controls.controls.append(new_users)

                            self.count_success_add_new_user += (
                                1
                                if a["isVerified"] and isinstance(new_users_id, int)
                                else 0
                            )
                            self.count_failed_add_new_user += (
                                1
                                if a["isVerified"] and not isinstance(new_users_id, int)
                                else 0
                            )

        self.page.open(self.get_modal("Complete find new user!", True))
        end_loader_btn(self, self.btn_find_user, icon=ft.icons.FIND_IN_PAGE)

    def add_user(self, e):
        if self.new_user.value:
            if new_user := SyncORM.new_user(username=self.new_user.value):
                if isinstance(new_user, int):
                    new_user = User(
                        username=self.new_user.value,
                        user_delete=self.user_delete,
                        u_id=new_user,
                        w_run=self.w_run,
                    )
                    self.user_controls.controls.append(new_user)
                    self.new_user.value = ""
                    self.new_user.focus()
                    self.update()
                    # Update users list in WidgetsSendComment
                    self.w_run.w_send_comment.update_users()
                    return

            alert(
                page=self.page,
                error_str=new_user if new_user else None,
                def_message="Error add new user",
            )

    def user_delete(self, account):
        self.user_controls.controls.remove(account)
        # Update users list in WidgetsSendComment
        self.w_run.w_send_comment.update_users()
        self.update()

    def get_modal(self, message: str, status: bool):
        content = (
            f"Добавлено: {self.count_success_add_new_user}\n"
            f"Неудачных: {self.count_failed_add_new_user}"
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
