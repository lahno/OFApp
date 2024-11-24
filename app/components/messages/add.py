import logging

import flet as ft

from app.components.messages.message import Message
from app.components.sending.main import RunSending
from app.utils.helper import alert
from config import AppValues
from db.orm import SyncORM

logger = logging.getLogger(__name__)


class AddMessage(ft.Column):
    def __init__(self, page: ft.Page, w_run: RunSending):
        super().__init__()
        self.page = page
        self.w_run = w_run
        self.new_message = ft.TextField(
            hint_text="Message text", on_submit=self.add_message, expand=True
        )
        self.messages = ft.Column()

        if messages := SyncORM.get_all_messages():
            for message in messages:
                m = Message(
                    message.message,
                    self.message_status_change,
                    self.message_delete,
                    m_id=message.id,
                    w_run=self.w_run,
                    m_status=message.status,
                )
                self.messages.controls.append(m)

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=1,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active")],
        )

        self.items_left = ft.Text("0 not active message")

        self.width = AppValues.WIDTH_APP
        self.controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.new_message,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_message
                        ),
                    ],
                ),
                padding=ft.padding.only(top=20, right=10, left=10),
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.messages,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[self.items_left],
                    ),
                ],
            ),
        ]

    def add_message(self, e):
        if self.new_message.value:
            if mew_message := SyncORM.new_message(message=self.new_message.value):
                if isinstance(mew_message, int):
                    task = Message(
                        self.new_message.value,
                        self.message_status_change,
                        self.message_delete,
                        m_id=mew_message,
                        w_run=self.w_run,
                    )
                    self.messages.controls.append(task)
                    self.new_message.value = ""
                    self.new_message.focus()
                    self.update()
                    # Update message list in WidgetsSendComment
                    self.w_run.w_send_comment.update_messages()
                    return

            alert(
                page=self.page,
                error_str=mew_message if mew_message else None,
                def_message="Error add new message",
            )

    def message_status_change(self, message):
        SyncORM.update_message({"status": message.display_message.value}, message.id)
        # Update message list in WidgetsSendComment
        self.w_run.w_send_comment.update_messages()
        self.page.update()

    def message_delete(self, message):
        self.messages.controls.remove(message)
        # Update message list in WidgetsSendComment
        self.w_run.w_send_comment.update_messages()
        self.page.update()

    def tabs_changed(self, e):
        self.page.update()

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        self.items_left.color = ft.colors.BLACK
        count = 0
        for task in self.messages.controls:
            task.visible = status == "all" or (
                status == "active" and task.active == True
            )
            if not task.active:
                count += 1
        self.items_left.value = f"{count} not active message(s)"
        if count > 0:
            self.items_left.color = ft.colors.RED
