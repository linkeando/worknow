import flet as ft
from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.services.preferences import Preferences
from application.utils.constants import Constants
from application.utils.destination_provider import DestinationProvider
from application.widgets.navigationrail import NavigationRail


class ChatSettings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = Preferences(self.page)
        self.option_download = ft.RadioGroup(content=ft.Row(
            [ft.Radio(value="Zip", label="Archivo Zip"), ft.Radio(value="Unico", label="Archivo Único")]),
            value=PreferencesDB(self.session_manager).get_preference(Constants.TIPE_DOWNLOAD_CHAT) or Constants.TIPE_DOWNLOAD_CHAT)

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
                ft.Text('Preferencia Descarga', size=16),
                self.option_download
            ])
        )

    def create_content(self):
        path_download, text_slider, player_slider = self.value_settings()
        return ft.Column(
            [
                self.radio_options(),
                self.settings_tile(title='Tamaño Codigo', icon=ft.Icon(ft.icons.FORMAT_SIZE)),
                text_slider,
                self.settings_tile(title='Velocidad De Audio', icon=ft.Icon(ft.icons.RUN_CIRCLE)),
                player_slider,
                self.settings_tile(title='Ruta De Descarga', subtitle=path_download,
                                   icon=ft.Icon(ft.icons.FOLDER),
                                   on_click=lambda e: self.preferences.selected_path_download()),
                ft.Row([
                    ft.Container(
                        alignment=ft.alignment.bottom_right,
                        content=ft.ElevatedButton(text="Predeterminado",
                                                  on_click=lambda e: self.preferences.predeterminate_preference_chat()),
                        padding=ft.padding.all(20),
                    ),
                    ft.Container(
                        alignment=ft.alignment.bottom_right,
                        content=ft.ElevatedButton(text="Guardar",
                                                  on_click=lambda e: self.preferences.save_preference_chat(
                                                      self.option_download, text_slider,
                                                      player_slider)),
                        padding=ft.padding.only(top=20, bottom=20),
                    ),
                ], expand=True)
            ],
            expand=True
        )

    def view(self):
        nav_rail = NavigationRail(self.page, DestinationProvider.update_page_chat(self.page),
                                  Constants.INDEX_CHAT_RAIL).navigation(DestinationProvider.get_chat_destinations())
        return ft.Row([nav_rail, ft.VerticalDivider(width=1), self.create_content()], expand=True)

    def value_settings(self):
        path_to_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_SAVE_CHAT) or self.session_manager.get_app_data_dir()
        text_value = PreferencesDB(self.session_manager).get_preference(
            Constants.TEXT_CHAT_PREFERENCE) or Constants.TEXT_CHAT
        text_slider = ft.Slider(min=8, max=30, divisions=22, label="{value}%", value=text_value)
        player_value = PreferencesDB(self.session_manager).get_preference(
            Constants.RATE_PREFERENCE) or Constants.RATE_AUDIO
        player_slider = ft.Slider(min=50, max=300, divisions=15, label="{value}%", value=player_value)
        return path_to_download, text_slider, player_slider
