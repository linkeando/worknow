from application.utils.constants import Constants
from application.utils.enums import TabLabels, TabRoutes, IndexedTabDrawer
import flet as ft


class NavigationDrawer:
    ICON_HOME = ft.icons.CHAT_BUBBLE
    ICON_DOWNLOAD = ft.icons.DOWNLOAD
    ICON_SETTINGS = ft.icons.SETTINGS

    def __init__(self, page: ft.Page):
        self.page = page

    def open_drawer(self):
        destinations = [
            ft.NavigationDrawerDestination(icon=self.ICON_HOME, label=TabLabels.CHAT.value),
            ft.NavigationDrawerDestination(icon=self.ICON_DOWNLOAD, label=TabLabels.DOWNLOAD.value),
            ft.NavigationDrawerDestination(icon=self.ICON_SETTINGS, label=TabLabels.SETTINGS.value)
        ]
        drawer = ft.NavigationDrawer(on_change=lambda event: self._change_tab_drawer(event),
                                     controls=destinations, selected_index=self.page.session.get("index_drawer"))
        self.page.show_end_drawer(drawer)

    def _update_page(self, selected_tab_route):
        if selected_tab_route == TabRoutes.CHAT.value:
            self.page.appbar.title = ft.Text('Chat', overflow=ft.TextOverflow.ELLIPSIS)
            self.page.session.set(Constants.INDEX_CHAT_RAIL, 0)
        elif selected_tab_route == TabRoutes.DOWNLOAD.value:
            self.page.appbar.title = ft.Text('Downloader', overflow=ft.TextOverflow.ELLIPSIS)
            self.page.session.set(Constants.INDEX_DOWNLOAD_RAIL, 0)
        elif selected_tab_route == TabRoutes.SETTINGS.value:
            self.page.appbar.title = ft.Text('Settings', overflow=ft.TextOverflow.ELLIPSIS)
        self.page.go(selected_tab_route)

    def _change_tab_drawer(self, drawer_event):
        selected_tab_route = IndexedTabDrawer.get_route(drawer_event.control.selected_index)
        self.page.end_drawer.open = False
        self.page.session.set('index_drawer', drawer_event.control.selected_index)
        self._update_page(selected_tab_route)
