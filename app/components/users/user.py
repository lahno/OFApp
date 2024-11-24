import flet as ft

from app.components.sending.main import RunSending
from db.orm import SyncORM


class User(ft.Column):
    def __init__(self, username, user_delete, u_id: int, w_run: RunSending):
        super().__init__()
        self.id = u_id
        self.w_run = w_run
        self.username = username
        self.user_delete = user_delete
        self.display_user = ft.Text(self.username)
        self.edit_user = ft.TextField(expand=1, multiline=True)

        self.display_view = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_user,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ACCOUNT_BOX_OUTLINED,
                                tooltip="Profile",
                                url=f"https://onlyfans.com/{self.username}",
                            ),
                            ft.IconButton(
                                icon=ft.icons.CREATE_OUTLINED,
                                tooltip="Edit user",
                                on_click=self.edit_clicked,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete user",
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            ),
            padding=ft.padding.only(left=15, top=0, bottom=0),
            bgcolor=ft.colors.GREY_100,
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_user,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update user",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_user.value = self.username
        self.display_view.visible = False
        self.edit_view.visible = True
        # Update users list in WidgetsSendComment
        self.w_run.w_send_comment.update_users()
        self.update()

    def save_clicked(self, e):
        SyncORM.update_user({"username": self.edit_user.value}, self.id)
        self.username = self.edit_user.value
        self.display_user.value = self.edit_user.value
        self.display_view.visible = True
        self.edit_view.visible = False
        # Update users list in WidgetsSendComment
        self.w_run.w_send_comment.update_users()
        self.update()

    def delete_clicked(self, e):
        SyncORM.delete_user(self.id)
        self.user_delete(self)
