import flet as ft

from app.components.sending.sending_comments import WidgetsSendComment


class RunSending(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.w_send_comment = WidgetsSendComment(page)
        self.controls = [
            self.w_send_comment.controls,
        ]
