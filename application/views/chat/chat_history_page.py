import os
import platform
import subprocess

import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants
from application.utils.destination_provider import DestinationProvider
from application.utils.page import UtilPage
from application.widgets.navigationrail import NavigationRail


class ChatHistory:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()

    def on_tap_callback(self, file_path):
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Linux":
                subprocess.run(["xdg-open", file_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:
                print("Sistema operativo no compatible. No se pudo abrir la carpeta.")
        except FileNotFoundError:
            dialog_modal = UtilPage(self.page).create_modal_simple(
                f"El Archivo \n\n{file_path}\n\n Se Traslado Y No Se Pudo Abrir")
            self.page.dialog = dialog_modal
            dialog_modal.open = True
            self.page.update()

    def create_row(self, file_type: str, file_path: str):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(file_type)),
                ft.DataCell(ft.Text(file_path), on_tap=lambda e: self.on_tap_callback(file_path))
            ]
        )

    def ask_clean_history(self):
        services = [("Yes", lambda e: self.clean_history()),
                    ("No", lambda e: UtilPage(self.page).close_dlg())]
        dialog_modal = UtilPage(self.page).create_modal_option('Limpiar Historial',
                                                               '¿Está seguro de que desea eliminar el historial?',
                                                               services)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def clean_history(self):
        PreferencesDB(self.session_manager).delete_preference(Constants.TYPE_SAVE_FILE)
        row_view: ft.Row = self.page.controls[0].content
        column_view: ft.Column = row_view.controls[2]
        list_view: ft.ListView = column_view.controls[1]
        list_view.controls = []
        self.page.update()
        dialog_modal = UtilPage(self.page).create_modal_simple(f"Historial Limpiado Exitosamente")
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def create_rows(self):
        history_download = PreferencesDB(self.session_manager).get_preference(Constants.TYPE_SAVE_FILE)
        messages = [item.get('Mensaje') for item in history_download.get('mensaje', [])] if history_download else []
        audios = [item.get('Audio') for item in history_download.get('audio', [])] if history_download else []

        rows = [self.create_row("Mensaje", message) for message in messages]
        rows += [self.create_row("Audio", audio) for audio in audios]

        return rows

    def create_table(self):
        return ft.DataTable(
            border_radius=10,
            divider_thickness=0,
            column_spacing=200,
            expand=True,
            columns=[
                ft.DataColumn(ft.Text("Tipo De Archivo")),
                ft.DataColumn(ft.Text("Ruta De Descarga"))
            ],
            rows=self.create_rows()
        )

    def history_view(self):
        table = self.create_table()
        lv = ft.ListView(expand=1, spacing=15, padding=10, auto_scroll=False)
        lv.controls.append(table)
        return lv

    def view(self):
        nav_rail = NavigationRail(self.page, DestinationProvider.update_page_chat(self.page), Constants.INDEX_CHAT_RAIL)
        clear_button = ft.Container(
            alignment=ft.alignment.top_right,
            content=ft.FilledButton("Clear History", icon="DELETE", on_click=lambda e: self.ask_clean_history(),
                                    expand=True)
        )

        content_column = ft.Column([
            clear_button,
            self.history_view()
        ], expand=True)

        return ft.Row(
            [nav_rail.navigation(DestinationProvider.get_chat_destinations()),
             ft.VerticalDivider(width=1),
             content_column],
            expand=True,
        )
