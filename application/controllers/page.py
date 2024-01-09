import flet as ft


class PageController:
    def __init__(self, page: ft.Page):
        self.page = page

    def theme_mode(self):
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.page.appbar.actions[0].icon = self.change_icon_button()
        self.page.update()

    def change_icon_button(self):
        return ft.icons.DARK_MODE if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
