import flet as ft

from app.components.sending.main import RunSending
from db.orm import SyncORM


class Account(ft.Column):
    def __init__(self, email, account_delete, a_id: int, w_run: RunSending):
        super().__init__()
        self.id = a_id
        self.w_run = w_run
        self.email = email
        self.account_delete = account_delete
        self.display_account = ft.Text(self.email)
        self.edit_account = ft.TextField(expand=1, multiline=True)

        self.display_view = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_account,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.CREATE_OUTLINED,
                                tooltip="Edit Account",
                                on_click=self.edit_clicked,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete Account",
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            ),
            padding=ft.padding.only(left=15),
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_account,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update Account",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_account.value = self.email
        self.display_view.visible = False
        self.edit_view.visible = True
        # Update account list in WidgetsSendComment
        self.w_run.w_send_comment.update_accounts()
        self.update()

    def save_clicked(self, e):
        SyncORM.update_account({"email": self.edit_account.value}, self.id)
        self.email = self.edit_account.value
        self.display_account.value = self.edit_account.value[:70]
        self.display_view.visible = True
        self.edit_view.visible = False
        # Update account list in WidgetsSendComment
        self.w_run.w_send_comment.update_accounts()
        self.update()

    def delete_clicked(self, e):
        SyncORM.delete_account(self.id)
        self.account_delete(self)
