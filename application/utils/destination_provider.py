import flet as ft

from application.utils.constants import Constants
from application.utils.enums import TabRoutes


class DestinationProvider:

    @staticmethod
    def get_default_destinations():
        return [
            ft.NavigationRailDestination(
                icon=ft.icons.HOME, selected_icon=ft.icons.HOME_FILLED, label="Home", padding=ft.margin.only(bottom=30)
            )
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
    def update_page_chat(page):
        def update():
            index = page.session.get(Constants.INDEX_CHAT_RAIL)
            if index == 0:
                page.appbar.title = ft.Text('Chat')
                page.go(TabRoutes.CHAT.value)
            elif index == 1:
                page.appbar.title = ft.Text('Preferences')
                page.go(TabRoutes.CHAT_SETTINGS.value)
            elif index == 2:
                page.appbar.title = ft.Text('History')
                page.go(TabRoutes.CHAT_HISTORY.value)

        return update

    @staticmethod
    def update_page_downloader(page):
        def update():
            index = page.session.get(Constants.INDEX_DOWNLOAD_RAIL)
            if index == 0:
                page.appbar.title = ft.Text('Downloader')
                page.go(TabRoutes.DOWNLOAD.value)
            elif index == 1:
                page.appbar.title = ft.Text('Preferences')
                page.go(TabRoutes.DOWNLOAD_SETTINGS.value)
            elif index == 2:
                page.appbar.title = ft.Text('History')
                page.go(TabRoutes.DOWNLOAD_HISTORY.value)
        return update
