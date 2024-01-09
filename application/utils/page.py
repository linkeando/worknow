import flet as ft


class UtilPage:
    MIN_HEIGHT = 600
    MIN_WIDTH = 800

    def __init__(self, page: ft.Page):
        self.page = page

    def general_window_option(self):
        self.page.title = 'WorkNow'
        self.page.window_center()
        self.page.window_width = self.MIN_WIDTH
        self.page.window_height = self.MIN_HEIGHT
        self.page.window_min_height = self.MIN_HEIGHT
        self.page.window_min_width = self.MIN_WIDTH
        self.page.update()

    def close_dlg(self):
        self.page.dialog.open = False
        self.page.update()

    def create_modal_option(self, text, content, buttons_and_callbacks):
        actions = [ft.TextButton(button, on_click=callback) for button, callback in buttons_and_callbacks]

        return ft.AlertDialog(
            title=ft.Text(text),
            content=ft.Text(content),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def create_modal_simple(self, text):
        return ft.AlertDialog(
            title=ft.Text(text), on_dismiss=lambda e: print("Dialog dismissed!")
        )