import flet as ft

from application.controllers.page import PageController
from application.widgets.navigationdrawer import NavigationDrawer


class AppBar:
    def __init__(self, page: ft.Page, title):
        self.page = page
        self.title = title

    def bar(self):
        return ft.AppBar(
            title=ft.Text(self.title, overflow=ft.TextOverflow.ELLIPSIS),
            center_title=True,
            actions=[
                ft.IconButton(ft.icons.DARK_MODE_OUTLINED, on_click=lambda e: PageController(self.page).theme_mode()),
                ft.IconButton(ft.icons.CENTER_FOCUS_WEAK, on_click=lambda e: self.page.window_center()),
                ft.IconButton(ft.icons.MENU_OPEN, on_click=lambda e: NavigationDrawer(self.page).open_drawer()),
            ],
        )
