import flet as ft

from app.components.sending.main import RunSending
from db.orm import SyncORM


class Message(ft.Column):
    def __init__(
        self,
        message_text,
        task_status_change,
        task_delete,
        m_id: int,
        w_run: RunSending,
        m_status=True,
    ):
        super().__init__()
        self.id = m_id
        self.w_run = w_run
        self.active = m_status
        self.message_text = message_text
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.display_message = ft.Checkbox(
            value=m_status, label=self.message_text[:70], on_change=self.status_changed
        )
        self.edit_message = ft.TextField(expand=1, multiline=True)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_message,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit Message",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete Message",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_message,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update Message",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_message.value = self.message_text
        self.display_view.visible = False
        self.edit_view.visible = True
        # Update message list in WidgetsSendComment
        self.w_run.w_send_comment.update_messages()
        self.update()

    def save_clicked(self, e):
        SyncORM.update_message({"message": self.edit_message.value}, self.id)
        self.message_text = self.edit_message.value
        self.display_message.label = self.edit_message.value[:70]
        self.display_view.visible = True
        self.edit_view.visible = False
        # Update message list in WidgetsSendComment
        self.w_run.w_send_comment.update_messages()
        self.update()

    def status_changed(self, e):
        self.active = self.display_message.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        SyncORM.delete_message(self.id)
        self.task_delete(self)
