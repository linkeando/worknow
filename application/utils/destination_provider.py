import flet as ft

from application.utils.constants import Constants
from application.utils.enums import TabRoutes


class DestinationProvider:

    @staticmethod
    def get_default_destinations():
        return [
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ]

    @staticmethod
    def get_chat_destinations():
        return [
            ft.NavigationRailDestination(
                icon=ft.icons.HOME, selected_icon=ft.icons.HOME_FILLED, label="Home", padding=ft.margin.only(bottom=30)
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS, selected_icon=ft.icons.SETTINGS_OUTLINED, label="Preferences",
                padding=ft.margin.only(bottom=30)
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HISTORY, selected_icon=ft.icons.HISTORY_ROUNDED, label="History",
                padding=ft.margin.only(bottom=30)
            ),
        ]

    @staticmethod
    def get_downloader_destinations():
        return [
            ft.NavigationRailDestination(
                icon=ft.icons.DOWNLOAD, selected_icon=ft.icons.DOWNLOAD, label="Downloads"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CLOUD, selected_icon=ft.icons.CLOUD, label="Cloud"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.DELETE, selected_icon=ft.icons.DELETE_SHARP, label="Trash"
            ),
        ]

    @staticmethod
    def update_page_chat(page):
        def update():
            index = page.session.get(Constants.INDEX_CHAT_RAIL)
            if index == 0:
                page.appbar.title = ft.Text('Home')
                page.go(TabRoutes.CHAT.value)
            elif index == 1:
                page.appbar.title = ft.Text('Preferences')
                page.go(TabRoutes.CHAT_SETTINGS.value)
            elif index == 2:
                page.appbar.title = ft.Text('History')
                page.go(TabRoutes.CHAT_HISTORY.value)
        return update
