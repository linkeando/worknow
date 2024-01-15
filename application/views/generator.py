import flet as ft

from application.services.generator import GeneratorService
from application.utils.constants import Constants


class Generator:
    def __init__(self, page: ft.Page):
        self.page = page
        self.generator_service = GeneratorService(self.page)
        self.option_selected = self.dropdown_generator()
        self.longitud_selected = self.longitud_password()
        self.terminacion_selected = self.end_mail()
        self.total_selected = self.quantity_output()
        self.output_text = self.output_generator()

    @staticmethod
    def dropdown_generator():
        return ft.Dropdown(
            value='Password',
            options=[
                ft.dropdown.Option("Password"),
                ft.dropdown.Option("Mail"),
            ],
            expand=True
        )

    def longitud_password(self):
        value_longitud = self.generator_service.preferences.get_preference(Constants.LONGITUD_GENERATOR)
        return ft.TextField(expand=True, label="Longitud", hint_text="Ingrese Longitud", value=value_longitud,
                            input_filter=ft.NumbersOnlyInputFilter())

    def end_mail(self):
        value_mail = self.generator_service.preferences.get_preference(Constants.TERMINACION_GENERATOR)
        return ft.TextField(expand=True, label='Terminacion (correo)', hint_text='Ingrese Terminacion',
                            value=value_mail)

    def quantity_output(self):
        value_quantity = self.generator_service.preferences.get_preference(Constants.RESULTADOS_GENERATOR)
        return ft.TextField(expand=True, label='Resultados', hint_text='Ingrese Total De Resultados',
                            value=value_quantity,
                            input_filter=ft.NumbersOnlyInputFilter())

    def output_generator(self):
        value_output = self.generator_service.preferences.get_preference(Constants.CONTAINER_GENERATOR)
        return ft.Container(margin=ft.margin.all(10), expand=True,
                            content=ft.TextField(multiline=True, min_lines=1280, value=value_output
                                                 ))

    def create_option_generator(self):
        return ft.Row([
            ft.Container(margin=ft.margin.all(10), content=self.option_selected, expand=True),
            ft.Container(margin=ft.margin.all(10), content=self.longitud_selected, expand=True),
            ft.Container(margin=ft.margin.all(10), content=self.terminacion_selected, expand=True),
            ft.Container(margin=ft.margin.all(10), content=self.total_selected, expand=True),
        ])

    def create_action_output(self):
        return ft.Row([
            ft.Container(margin=ft.margin.all(10),
                         content=ft.ElevatedButton(icon=ft.icons.CLEAR_ALL, text='Limpiar Todo',
                                                   on_click=lambda e: self.generator_service.clear_all(
                                                       self.output_text,
                                                       self.longitud_selected,
                                                       self.terminacion_selected, self.total_selected,
                                                   )), expand=True),
            ft.Container(margin=ft.margin.all(10),
                         content=ft.ElevatedButton(icon=ft.icons.COPY, text='Copiar Resultados',
                                                   on_click=lambda e: self.generator_service.copy_results(
                                                       self.output_text)),
                         expand=True),
            ft.Container(margin=ft.margin.all(10),
                         content=ft.ElevatedButton(icon=ft.icons.SEND, text='Generar Valores',
                                                   on_click=lambda e: self.generator_service.generator(
                                                       self.output_text,
                                                       self.option_selected, self.longitud_selected,
                                                       self.terminacion_selected, self.total_selected,
                                                   )),
                         expand=True)
        ])

    def view(self):
        return ft.Column([
            self.create_option_generator(),
            self.output_text,
            self.create_action_output()
        ], expand=True)
