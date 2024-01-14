from enum import Enum


class TabLabels(Enum):
    CHAT = "Chat"
    DOWNLOAD = "Download"
    GENERATOR = "Generator"
    COUNTER = "Counter"
    SETTINGS = "Settings"


class TabRoutes(Enum):
    CHAT = '/chat'
    CHAT_SETTINGS = '/chat_settings'
    CHAT_HISTORY = '/chat_history'
    DOWNLOAD = '/descargas'
    DOWNLOAD_SETTINGS = '/descargas_settings'
    DOWNLOAD_FORMATS = '/descargas_formats'
    DOWNLOAD_HISTORY = '/descargas_history'
    GENERATOR = '/generator'
    COUNTER = '/counter'
    SETTINGS = '/settings'


class TabDrawer(Enum):
    CHAT = '/chat'
    DOWNLOAD = '/descargas'
    GENERATOR = '/generator'
    COUNTER = '/counter'
    SETTINGS = '/settings'


class IndexedTabDrawer:
    @staticmethod
    def get_route(index: int) -> str:
        routes = [route.value for route in TabDrawer]
        if 0 <= index < len(routes):
            return routes[index]
        else:
            raise ValueError("Index out of range")
