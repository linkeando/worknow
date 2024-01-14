import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.services.counter import CounterService
from application.utils.constants import Constants


class Counter:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)
        self.counter_service = CounterService(self.page)
        self.evaluate_text = self.create_text_to_evaluate()
        self.text_to_search = self.create_text_to_search()
        self.total_words = self.create_card_value(icon=ft.icons.BOOK, title='Total de Palabras', value='0')
        self.all_characters = self.create_card_value(icon=ft.icons.ALL_OUT, title='Total de Caracter', value='0')
        self.unic_words = self.create_card_value(icon=ft.icons.HISTORY, title='Palabras Únicas', value='0')
        self.search_word = self.create_card_value(icon=ft.icons.SEARCH_OFF_ROUNDED, title='Palabra Buscada', value='0')

    def create_text_to_search(self):
        return ft.TextField(expand=True, border_radius=25,
                            on_change=lambda e: self.counter_service.on_text_change_input(e, self.evaluate_text))

    def create_top_options(self):
        return ft.Container(
            margin=ft.margin.all(10),
            content=ft.Row([
                ft.ElevatedButton(icon=ft.icons.MARK_CHAT_READ_OUTLINED, text='Leer TXT', expand=True,
                                  height=58,
                                  on_click=lambda e: self.counter_service.read(self.evaluate_text)),
                ft.ElevatedButton(icon=ft.icons.CLEAR_ALL, text='Limpiar', expand=True, height=58,
                                  on_click=lambda e: self.counter_service.clean(self.evaluate_text)),
                ft.ElevatedButton(icon=ft.icons.COPY, text='Copiar', expand=True, height=58,
                                  on_click=lambda e: self.counter_service.copy(self.evaluate_text)),
                self.text_to_search,
            ])
        )

    def create_text_to_evaluate(self):
        value_preference = self.preferences.get_preference(Constants.COUNTER_STATE)
        return ft.Container(margin=ft.margin.all(10), expand=True,
                            content=ft.TextField(multiline=True, min_lines=1280, value=value_preference,
                                                 on_change=lambda e: self.counter_service.on_text_change_main(e)))

    @staticmethod
    def create_card_value(icon: ft.icons, title: str, value: str):
        return ft.Card(
            expand=True,
            content=ft.Column([
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Icon(icon),
                ),
                ft.Container(
                    padding=ft.padding.all(15),
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                ),
                ft.Container(
                    padding=ft.padding.all(15),
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text(value, size=16, weight=ft.FontWeight.BOLD),
                )
            ]),
        )

    def create_card_show_counter(self):
        return ft.Container(
            expand=True,
            margin=ft.margin.all(10),
            content=ft.Row([
                self.total_words,
                self.all_characters,
                self.unic_words,
                self.search_word
            ], expand=True)
        )

    def view(self):
        return ft.Column([
            self.create_top_options(),
            self.evaluate_text,
            self.create_card_show_counter()
        ], expand=True)
