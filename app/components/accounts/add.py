import flet as ft

from app.components.accounts.account import Account
from app.components.sending.main import RunSending
from app.utils.helper import alert
from config import AppValues
from db.orm import SyncORM


class AddAccount(ft.Column):
    def __init__(self, page: ft.Page, w_run: RunSending):
        super().__init__()
        self.page = page
        self.w_run = w_run
        self.new_account = ft.TextField(
            hint_text="Add E-mail account", on_submit=self.add_account, expand=True
        )
        self.account_controls = ft.Column()

        if accounts := SyncORM.get_accounts():
            for account in accounts:
                users = Account(
                    email=account.email,
                    account_delete=self.account_delete,
                    a_id=account.id,
                    w_run=self.w_run,
                )
                self.account_controls.controls.append(users)

        self.width = AppValues.WIDTH_APP
        self.controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.new_account,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_account
                        ),
                    ],
                ),
                padding=ft.padding.only(top=20, right=10, left=10),
            ),
            ft.Column(
                spacing=25,
                controls=[self.account_controls],
            ),
        ]

    def add_account(self, e):
        if self.new_account.value:
            if new_account := SyncORM.new_account(email=self.new_account.value):
                if isinstance(new_account, int):
                    new_account = Account(
                        email=self.new_account.value,
                        account_delete=self.account_delete,
                        a_id=new_account,
                        w_run=self.w_run,
                    )
                    self.account_controls.controls.append(new_account)
                    self.new_account.value = ""
                    self.new_account.focus()
                    self.update()
                    # Update message list in WidgetsSendComment
                    self.w_run.w_send_comment.update_accounts()
                    return

            alert(
                page=self.page,
                error_str=new_account if new_account else None,
                def_message="Error add new account",
            )

    def account_delete(self, account):
        self.account_controls.controls.remove(account)
        # Update message list in WidgetsSendComment
        self.w_run.w_send_comment.update_accounts()
        self.update()
