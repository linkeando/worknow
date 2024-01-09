import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants
from application.utils.enums import TabRoutes


class Preferences:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)

    def predeterminate_preference_chat(self):
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_CHAT, Constants.TIPE_DOWNLOAD_CHAT)
        self.preferences.set_preference(Constants.TEXT_CHAT_PREFERENCE, Constants.TEXT_CHAT)
        self.preferences.set_preference(Constants.RATE_PREFERENCE, Constants.RATE_AUDIO)

    def save_preference_chat(self, option_download: ft.RadioGroup, text: ft.Slider, player: ft.Slider):
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_CHAT, option_download.value)
        self.preferences.set_preference(Constants.TEXT_CHAT_PREFERENCE, text.value)
        self.preferences.set_preference(Constants.RATE_PREFERENCE, player.value)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.preferences.set_preference(Constants.PATH_SAVE_CHAT, e.path)
            row_view: ft.Row = self.page.controls[0].content
            list_tile: ft.ListTile = row_view.controls[2].controls[5]
            list_tile.subtitle.value = e.path
            self.page.update()
        else:
            print('no selecciono archivo')

    def selected_path_download(self):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self.pick_files_result(e))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.get_directory_path('Selecciona Carpeta Para Guardar Archivos')
