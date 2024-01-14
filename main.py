import flet as ft

from application.utils.enums import TabRoutes
from application.utils.page import UtilPage
from application.utils.router import Router
from application.widgets.appbar import AppBar


def main(page: ft.Page):
    UtilPage(page).general_window_option()
    page.theme_mode = page.theme_mode.LIGHT
    page.appbar = AppBar(page, 'Chat').bar()
    router = Router(page)
    page.on_route_change = router.route_change
    page.add(router.body)
    page.go(TabRoutes.CHAT.value)


ft.app(target=main)
