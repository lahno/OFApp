import flet as ft


def alert(
    page: ft.Page,
    error_str: str | None = None,
    color_alert=ft.colors.RED_400,
    color_font=ft.colors.BLACK,
    def_message="Error add new account",
    duration=7000,
):
    message = False
    if error_str and isinstance(error_str, str):
        message = error_str

    page.snack_bar = ft.SnackBar(
        content=ft.Text(
            (message if message else def_message),
            color=color_font,
        ),
        duration=duration,
        bgcolor=color_alert,
    )
    page.snack_bar.open = True
    page.update()


def start_loader_btn(obj, btn):
    btn.content = ft.ProgressRing(
        width=10, height=10, stroke_width=2, tooltip="Processing..."
    )
    obj.update()


def end_loader_btn(obj, btn, icon=None, content=None):
    btn.content = None
    if icon:
        btn.icon = icon
    if content:
        btn.content = content

    obj.update()
