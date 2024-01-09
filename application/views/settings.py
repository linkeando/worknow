import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants
from application.utils.enums import TabDrawer
from application.utils.page import UtilPage


class Settings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)

    @staticmethod
    def settings_tile(title, icon=None, subtitle=None, on_click=None):
        return ft.Container(
            content=ft.ListTile(
                leading=icon,
                title=ft.Text(title),
                subtitle=ft.Text(subtitle) if subtitle else None,
                on_click=on_click,
            ),
            margin=ft.margin.all(15)
        )

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.preferences.set_preference(Constants.PATH_DOWNLOAD_DB, e.path)
            column_view: ft.Column = self.page.controls[0].content
            column_view.controls[2].content.subtitle.value = e.path
            self.page.update()
        else:
            print("Error: No se seleccionó ningún archivo.")

    def replace_db_now(self, e: ft.FilePickerResultEvent):
        if e.files and e.files[0].path:
            self.session_manager.upload_database(e.files[0].path, self.page)
        else:
            print("Error: No se seleccionó ningún archivo.")

    def export_database_service(self, path):
        self.session_manager.download_database(path)
        dialog_modal = UtilPage(self.page).create_modal_simple(f'Descarga Completada En \n{path}')
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def modal_export_db(self, services):
        path_to_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_DOWNLOAD_DB) or self.session_manager.get_app_data_dir()
        dialog_modal = UtilPage(self.page).create_modal_option('Descarga De Configuracion',
                                                               f'Se Descargara En {path_to_download}', services)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def export_database(self):
        path_to_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_DOWNLOAD_DB) or self.session_manager.get_app_data_dir()
        services = [("Yes", lambda e: self.export_database_service(path_to_download)),
                    ("No", lambda e: UtilPage(self.page).close_dlg())]
        self.modal_export_db(services)

    def upload_database(self):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self.replace_db_now(e))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.pick_files('Selecciona Archivo De BD', allowed_extensions=['db'], allow_multiple=False)

    def define_path_to_save(self):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self.pick_files_result(e))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.get_directory_path('Selecciona Carpeta Donde Se Descargara La DB')

    def view(self):
        path_to_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_DOWNLOAD_DB) or self.session_manager.get_app_data_dir()
        return ft.Column([
            self.settings_tile(title='Descargar Configuracion', icon=ft.Icon(ft.icons.DOWNLOAD),
                               on_click=lambda e: self.export_database()),
            self.settings_tile(title='Subir Configuracion', icon=ft.Icon(ft.icons.UPLOAD),
                               on_click=lambda e: self.upload_database()),
            self.settings_tile(title='Ruta De Guardado', subtitle=path_to_download, icon=ft.Icon(ft.icons.FOLDER),
                               on_click=lambda e: self.define_path_to_save())
        ], expand=True)
