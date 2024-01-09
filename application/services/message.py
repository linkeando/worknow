import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from typing import List

import flet as ft
import pyttsx3

from application.database.database_manager import DatabaseManager
from application.database.message_db import MessageDB
from application.database.preferences_db import PreferencesDB
from application.models.message import Message
from application.services.speaker import Speaker
from application.utils.constants import Constants
from application.utils.page import UtilPage
from application.widgets.contextualactionbar import ContextualActionBar


class MessageService:
    def __init__(self, page: ft.Page):
        self.page = page
        self.speaker = Speaker()
        self.engine = pyttsx3.init()
        self.session_manager = DatabaseManager()
        self.is_playing = False

    @staticmethod
    def get_date():
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    @staticmethod
    def get_message(control: ft.Markdown):
        sender = control.key['sender']
        content = Message.from_json(control.key).content
        return f"{sender}: {content}"

    def update_icon(self, control: ft.Markdown, icon: ft.icons):
        self.page.appbar.actions[1] = ft.IconButton(icon=icon, on_click=lambda e: self.toggle_play(control))
        self.page.update()

    def toggle_play(self, control: ft.Markdown):
        if self.is_playing:
            self.stop(control)
        else:
            self.play(control)

    def ask_message_delete(self, bar: ContextualActionBar, messages: ft.ListView):
        services = [("Yes", lambda e: self.process_clean_message(bar, messages)),
                    ("No", lambda e: UtilPage(self.page).close_dlg())]
        dialog_modal = UtilPage(self.page).create_modal_option('Eliminar Mensaje', 'Se eliminara el mensaje', services)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def process_clean_message(self, bar: ContextualActionBar, messages: ft.ListView):
        control = bar.selected_controls[0]
        with self.session_manager.session_scope() as session:
            all_messages: List[Message] = session.query(Message).all()
            index_to_delete = next(
                (index for index, message in enumerate(all_messages) if message.uuid == control.key['uuid']), None)
            MessageDB(self.session_manager).delete_message_by_uuid(control.key['uuid'])
            messages.controls.pop(index_to_delete)
        bar.exit_selection_mode()
        self.show_message_deleted_modal('Mensaje Eliminado Exitosamente')

    def show_message_deleted_modal(self, text):
        dialog_modal = UtilPage(self.page).create_modal_simple(text)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def clean_message(self, bar: ContextualActionBar, messages: ft.ListView):
        self.ask_message_delete(bar, messages)

    def download_message(self, control: ft.Markdown):
        message_content = self.get_message(control)
        path_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_SAVE_CHAT) or self.session_manager.get_app_data_dir()
        filename = f"Mensaje {self.get_date()}.txt"
        destiny = os.path.join(path_download, filename)
        with open(destiny, 'w', encoding='utf-8') as archivo:
            archivo.write(message_content)
        self.save_path_download_history('mensaje', destiny)
        dialog_modal = UtilPage(self.page).create_modal_simple(f'Mensaje Descargado Correctamente\n{destiny}')
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def download_audio(self, control: ft.Markdown):
        message_content = Message.from_json(control.key).content
        path_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_SAVE_CHAT) or self.session_manager.get_app_data_dir()
        filename = f"Audio {self.get_date()}.mp3"
        destiny = os.path.join(path_download, filename)
        self.engine.save_to_file(message_content, destiny)
        self.engine.runAndWait()
        self.save_path_download_history('audio', destiny)
        dialog_modal = UtilPage(self.page).create_modal_simple(f'Audio Descargado Correctamente\n{destiny}')
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    @staticmethod
    def download_all_messages_process(ruta_archivo, list_control: List[ft.Markdown]):
        message_to_download = ''
        for markdown_element in list_control:
            sender = markdown_element.key.get('sender', '')
            content = markdown_element.key.get('content', '')
            message_to_download += f"{sender}: {content}\n\n"
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(message_to_download)

    def download_all_messages(self, list_control: List[ft.Markdown]):
        type_download = PreferencesDB(self.session_manager).get_preference(
            Constants.TIPE_DOWNLOAD_CHAT) or Constants.TIPE_DOWNLOAD_CHAT
        path_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_SAVE_CHAT) or self.session_manager.get_app_data_dir()
        nombre_archivo = f"Mensajes {self.get_date()}.txt"
        if type_download == Constants.TIPE_DOWNLOAD_CHAT:
            path_zip = os.path.join(path_download, f"Mensajes {self.get_date()}.zip")
            with zipfile.ZipFile(path_zip, 'w') as zip_file:
                for idx, control in enumerate(list_control, start=1):
                    message_content = self.get_message(control)
                    nombre_archivo = f"Mensaje_{idx}_{self.get_date()}.txt"
                    zip_file.writestr(nombre_archivo, message_content)
            self.save_path_download_history('mensaje', path_zip)
            dialog_modal = UtilPage(self.page).create_modal_simple(f'Mensaje Descargado Como Zip\n{path_zip}')
            self.page.dialog = dialog_modal
            dialog_modal.open = True
            self.page.update()
        else:
            destiny = os.path.join(path_download, nombre_archivo)
            self.download_all_messages_process(destiny, list_control)
            self.save_path_download_history('mensaje', destiny)
            dialog_modal = UtilPage(self.page).create_modal_simple(f'Mensaje Descargado Unido\n{destiny}')
            self.page.dialog = dialog_modal
            dialog_modal.open = True
            self.page.update()

    def download_all_audio(self, list_control: List[ft.Markdown]):
        type_download = PreferencesDB(self.session_manager).get_preference(
            Constants.TIPE_DOWNLOAD_CHAT) or Constants.TIPE_DOWNLOAD_CHAT
        path_download = PreferencesDB(self.session_manager).get_preference(
            Constants.PATH_SAVE_CHAT) or self.session_manager.get_app_data_dir()
        nombre_archivo_zip = f"Audio_Combinado_{self.get_date()}.zip"
        nombre_archivo = f"Audio_Combinado_{self.get_date()}.mp3"

        if type_download == Constants.TIPE_DOWNLOAD_CHAT:
            with tempfile.TemporaryDirectory() as temp_dir:
                for idx, control in enumerate(list_control, start=1):
                    audio_content = Message.from_json(control.key).content
                    nombre_archivo = f"Audio_{idx}_{self.get_date()}.mp3"
                    ruta_archivo = os.path.join(temp_dir, nombre_archivo)
                    self.engine.save_to_file(audio_content, ruta_archivo)
                    self.engine.runAndWait()
                path_zip = os.path.join(path_download, nombre_archivo_zip)
                with zipfile.ZipFile(path_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_name in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file_name)
                        zip_file.write(file_path, arcname=file_name)
                    shutil.rmtree(temp_dir)
                self.save_path_download_history('audio', path_zip)
                dialog_modal = UtilPage(self.page).create_modal_simple(f'Audio Descargado Como Zip\n{path_zip}')
                self.page.dialog = dialog_modal
                dialog_modal.open = True
                self.page.update()
        else:
            content_list = [markdown_element.key.get('content', '') for markdown_element in list_control]
            super_content = ', '.join(content_list)
            destiny = os.path.join(path_download, nombre_archivo)
            self.engine.save_to_file(super_content, destiny)
            self.engine.runAndWait()
            self.save_path_download_history('audio', destiny)
            dialog_modal = UtilPage(self.page).create_modal_simple(f'Audio Descargado Unido\n{destiny}')
            self.page.dialog = dialog_modal
            dialog_modal.open = True
            self.page.update()

    def play(self, control: ft.Markdown):
        audio = self._get_audio(control)
        if audio:
            self.speaker.play_audio(audio)
            self.is_playing = True
            self.update_icon(control, ft.icons.PAUSE)

    def stop(self, control: ft.Markdown):
        audio = self._get_audio(control)
        if audio:
            self.speaker.stop(audio)
            self.is_playing = False
            self.update_icon(control, ft.icons.PLAY_CIRCLE)

    def _get_audio(self, control: ft.Markdown):
        message_content = Message.from_json(control.key).content
        audio = self.speaker.text_to_audio(message_content)
        return audio

    def ask_clean_selected_messages(self, bar: ContextualActionBar, messages: ft.ListView):
        services = [("Yes", lambda e: self.process_clean_selected_messages(bar, messages)),
                    ("No", lambda e: UtilPage(self.page).close_dlg())]
        dialog_modal = UtilPage(self.page).create_modal_option('Eliminar Mensajes',
                                                               'Se eliminarán los mensajes seleccionados', services)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def process_clean_selected_messages(self, bar: ContextualActionBar, messages: ft.ListView):
        controls_to_remove = list(bar.selected_controls)
        indices_to_remove = []

        with self.session_manager.session_scope() as session:
            all_messages: List[Message] = session.query(Message).all()
            message_db = MessageDB(self.session_manager)

            for control in controls_to_remove:
                uuid_to_remove = control.key.get('uuid', '')
                index_to_delete = next(
                    (index for index, message in enumerate(all_messages) if message.uuid == control.key['uuid']), None)
                message_db.delete_message_by_uuid(uuid_to_remove)
                if index_to_delete is not None:
                    indices_to_remove.append(index_to_delete)

            for index in reversed(indices_to_remove):
                messages.controls.pop(index)

        bar.exit_selection_mode()
        self.show_message_deleted_modal('Mensajes Eliminados Exitosamente')

    def clean_selected_messages(self, bar: ContextualActionBar, messages: ft.ListView):
        self.ask_clean_selected_messages(bar, messages)

    def ask_clear_all_messages(self, message_list_view):
        services = [("Yes", lambda e: self.clear_all_messages(message_list_view)),
                    ("No", lambda e: UtilPage(self.page).close_dlg())]
        dialog_modal = UtilPage(self.page).create_modal_option('Limpiar Mensajes', 'Se eliminarán todos los mensajes',
                                                               services)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def clear_all_messages(self, message_list_view):
        MessageDB(self.session_manager).delete_all_messages()
        message_list_view.controls = []
        self.page.update()
        self.show_message_deleted_modal('Mensajes Limpiados Con Exito')

    def save_path_download_history(self, tipo_archivo, filename):
        historial_descargas = PreferencesDB(self.session_manager).get_preference(Constants.TYPE_SAVE_FILE,
                                                                                 {'mensaje': [], 'audio': []})

        nuevo_elemento_descargado = {tipo_archivo.capitalize(): filename}
        historial_descargas[tipo_archivo].append(nuevo_elemento_descargado)

        PreferencesDB(self.session_manager).set_preference(Constants.TYPE_SAVE_FILE, historial_descargas)
