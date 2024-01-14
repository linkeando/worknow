import flet as ft
from application.utils.enums import TabRoutes
from application.views.chat.chat_home_page import Chat
from application.views.chat.chat_history_page import ChatHistory
from application.views.chat.chat_settings_page import ChatSettings
from application.views.counter import Counter
from application.views.download.download_formats_page import DownloadFormat
from application.views.download.download_history_page import DownloadHistory
from application.views.download.download_home_page import Download
from application.views.download.download_settings_page import DownloadSettings
from application.views.settings import Settings
from application.views.generator import Generator


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.flet = ft
        self.routes = {
            TabRoutes.CHAT.value: Chat,
            TabRoutes.CHAT_SETTINGS.value: ChatSettings,
            TabRoutes.CHAT_HISTORY.value: ChatHistory,
            TabRoutes.DOWNLOAD.value: Download,
            TabRoutes.DOWNLOAD_SETTINGS.value: DownloadSettings,
            TabRoutes.DOWNLOAD_FORMATS.value: DownloadFormat,
            TabRoutes.DOWNLOAD_HISTORY.value: DownloadHistory,
            TabRoutes.GENERATOR.value: Generator,
            TabRoutes.COUNTER.value: Counter,
            TabRoutes.SETTINGS.value: Settings
        }
        initial_route = self.routes[TabRoutes.CHAT.value](page).view()
        self.body = ft.Container(content=initial_route, expand=True)

    def route_change(self, route):
        view_instance = self.routes[route.route](self.page).view()
        self.body.content = view_instance
        self.body.update()
