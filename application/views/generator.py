import flet as ft


class Generator:
    def __init__(self, page: ft.Page):
        self.page = page

    def view(self):
        return ft.Column([
            ft.Container()
        ], expand=True)
