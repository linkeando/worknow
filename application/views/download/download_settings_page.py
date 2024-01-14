import flet as ft
from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.services.preference import Preferences
from application.utils.constants import Constants
from application.utils.destination_provider import DestinationProvider
from application.widgets.navigationrail import NavigationRail


class DownloadSettings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = Preferences(self.page)
        self.option_download = ft.RadioGroup(content=ft.Row(
            [ft.Radio(value="Alta", label="Alta"), ft.Radio(value="Media", label="Media"),
             ft.Radio(value="Baja", label="Baja")]),
            value=PreferencesDB(self.session_manager).get_preference(
                Constants.TIPE_DOWNLOAD_QUALITY) or Constants.TIPE_DOWNLOAD_QUALITY)

    @staticmethod
    def create_info_page():
        return ft.Column([
            ft.Text("¿Dónde se guardan mis descargas?",
                    size=15, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text(
                "Puedes seleccionar la carpeta de descargas en las Preferencias. Especifica la ruta donde deseas almacenar tus archivos descargados.",
                size=15, selectable=True),
            ft.Text("Mis videos no se reproducen.",
                    size=15, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text(
                "Si encuentras problemas de reproducción, te recomendamos probar con reproductores como VLC. Algunos formatos pueden requerir códecs adicionales. Ademas procura que todo el contenido sea accesible publicamente",
                size=15, selectable=True),
            ft.Text(
                disabled=False,
                spans=[
                    ft.TextSpan(
                        "\nConsulta la lista completa de sitios soportados",
                        ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE, size=15, weight=ft.FontWeight.BOLD),
                        url="https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md",
                    )
                ],
            ),
        ], scroll=ft.ScrollMode.AUTO)

    def faq_page(self):
        dlg = ft.AlertDialog(title=ft.Text('Preguntas Frecuentes'), content=self.create_info_page(),
                             actions_alignment=ft.MainAxisAlignment.END)
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def settings_tile(self, title, icon=None, subtitle=None, on_click=None):
        return ft.ListTile(
            leading=icon,
            title=ft.Text(title),
            subtitle=ft.Text(subtitle) if subtitle else None,
            on_click=on_click,
        )

    def radio_options(self):
        return ft.Container(
            padding=ft.padding.all(20),
            content=ft.Row([
                ft.Icon(ft.icons.AUDIOTRACK),
                ft.Text('Calidad De Descarga Grupal', size=16),
                self.option_download
            ])
        )

    def create_content(self):
        path_to_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_DOWNLOAD_VIDEOS) or self.session_manager.get_app_data_dir()
        return ft.Column(
            [
                self.radio_options(),
                self.settings_tile(title='Ruta De Descarga', subtitle=path_to_download,
                                   icon=ft.Icon(ft.icons.FOLDER),
                                   on_click=lambda e: self.preferences.selected_path_download_videos()),
                self.settings_tile(title='Preguntas Frecuentes',
                                   subtitle='Descubre Preguntas Frecuentes Sobre la descarga de contenido',
                                   icon=ft.Icon(ft.icons.QUESTION_ANSWER),
                                   on_click=lambda e: self.faq_page()),
                ft.Row([
                    ft.Container(
                        alignment=ft.alignment.bottom_right,
                        content=ft.ElevatedButton(text="Predeterminado",
                                                  on_click=lambda
                                                      e: self.preferences.predeterminate_preference_download()),
                        padding=ft.padding.all(20),
                    ),
                    ft.Container(
                        alignment=ft.alignment.bottom_right,
                        content=ft.ElevatedButton(text="Guardar",
                                                  on_click=lambda e: self.preferences.save_preference_download(
                                                      self.option_download)),
                        padding=ft.padding.only(top=20, bottom=20),
                    ),
                ], expand=True)
            ],
            expand=True
        )

    def view(self):
        nav_rail = NavigationRail(self.page, DestinationProvider.update_page_downloader(self.page),
                                  Constants.INDEX_DOWNLOAD_RAIL).navigation(
            DestinationProvider.get_downloader_destinations())
        return ft.Row([nav_rail, ft.VerticalDivider(width=1), self.create_content()], expand=True)
