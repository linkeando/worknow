import flet as ft


class GeneratorService:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_translation(self, text_to_translate):
        print()
