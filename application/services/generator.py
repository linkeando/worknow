import random
import string

import flet as ft

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants


class GeneratorService:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)

    @staticmethod
    def generate_password(longitud):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(caracteres) for _ in range(longitud))

    @staticmethod
    def generate_mail(longitud, terminacion):
        usuario = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(longitud))
        return f'{usuario}{terminacion}'

    def generate_values(self, data):
        tipo = data['type']
        longitud = data['longitud']
        terminacion = data['terminacion']
        resultados = data['resultados']

        generated_values = []

        if tipo == 'Password':
            generated_values = [self.generate_password(longitud) for _ in range(resultados)]
        elif tipo == 'Mail':
            generated_values = [self.generate_mail(longitud, terminacion) for _ in range(resultados)]

        return generated_values

    def clear_all(self, container_to_update: ft.Container, longitud="", terminacion="", resultados=""):
        container_to_update.content.value = ''
        longitud.value = ''
        terminacion.value = ''
        resultados.value = ''
        self.page.update()

    def copy_results(self, container_to_update: ft.Container):
        value_to_copy = container_to_update.content.value
        self.page.set_clipboard(value_to_copy)
        self.page.snack_bar = ft.SnackBar(ft.Text('Texto Copiado Al Portapapeles'))
        self.page.snack_bar.open = True
        self.page.update()

    def generate_password_values(self):
        print()

    def generator(self, container_to_update: ft.Container, type, longitud="", terminacion="", resultados=""):
        longitud = int(longitud.value) if longitud.value.isdigit() and int(
            longitud.value) > 0 else 10  # Valor por defecto: 10
        terminacion = str(terminacion.value) if terminacion.value else "@gmail.com"
        resultados = int(resultados.value) if resultados.value.isdigit() and int(resultados.value) > 0 else 5

        data = {'type': type.value, 'longitud': longitud, 'terminacion': terminacion, 'resultados': resultados}

        generated_values = self.generate_values(data)

        cadena_resultante = '\n\n'.join(generated_values)
        container_to_update.content.value = cadena_resultante
        self.preferences.set_preference(Constants.LONGITUD_GENERATOR, str(longitud))
        self.preferences.set_preference(Constants.TERMINACION_GENERATOR, terminacion)
        self.preferences.set_preference(Constants.RESULTADOS_GENERATOR, str(resultados))
        self.preferences.set_preference(Constants.CONTAINER_GENERATOR, str(resultados))
        self.page.update()
