import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants
from application.utils.page import UtilPage


class Preferences:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)

    def message_alert(self):
        dialog_modal = UtilPage(self.page).create_modal_simple(f'Configuraciones Guardadas')
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def predeterminate_preference_chat(self):
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_CHAT, Constants.TIPE_DOWNLOAD_CHAT)
        self.preferences.set_preference(Constants.TEXT_CHAT_PREFERENCE, Constants.TEXT_CHAT)
        self.preferences.set_preference(Constants.RATE_PREFERENCE, Constants.RATE_AUDIO)
        row_view: ft.Row = self.page.controls[0].content
        column_view: ft.Column = row_view.controls[2]

        row_quality: ft.Row = column_view.controls[0].content
        row_quality.controls[2].value = Constants.TIPE_DOWNLOAD_CHAT

        column_view.controls[2].value = Constants.TEXT_CHAT
        column_view.controls[4].value = Constants.RATE_AUDIO
        path: ft.ListTile = column_view.controls[5]
        path.subtitle.value = self.session_manager.get_app_data_dir()
        self.page.update()

    def save_preference_chat(self, option_download: ft.RadioGroup, text: ft.Slider, player: ft.Slider):
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_CHAT, option_download.value)
        self.preferences.set_preference(Constants.TEXT_CHAT_PREFERENCE, text.value)
        self.preferences.set_preference(Constants.RATE_PREFERENCE, player.value)
        self.message_alert()

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

    def _selected_path_download(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.preferences.set_preference(Constants.PATH_DOWNLOAD_VIDEOS, e.path)
            row_view: ft.Row = self.page.controls[0].content
            column_view: ft.Column = row_view.controls[2]
            column_view.controls[1].subtitle.value = e.path
            self.page.update()
        else:
            print("Error: No se seleccionó ningún archivo.")

    def selected_path_download_videos(self):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self._selected_path_download(e))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.get_directory_path('Selecciona Carpeta Donde Se Descargaran los videos')

    def predeterminate_preference_download(self):
        self.preferences.set_preference(Constants.PATH_DOWNLOAD_VIDEOS, self.session_manager.get_app_data_dir())
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_QUALITY, Constants.TIPE_DOWNLOAD_QUALITY)
        row_view: ft.Row = self.page.controls[0].content
        column_view: ft.Column = row_view.controls[2]
        row_quality: ft.Row = column_view.controls[0].content
        row_quality.controls[2].value = Constants.TIPE_DOWNLOAD_QUALITY
        column_view.controls[1].subtitle.value = self.session_manager.get_app_data_dir()
        self.page.update()

    def save_preference_download(self, option_download: ft.RadioGroup):
        self.preferences.set_preference(Constants.TIPE_DOWNLOAD_QUALITY, option_download.value)
        self.message_alert()
