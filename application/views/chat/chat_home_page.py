import flet as ft
import g4f

from application.database.message_db import MessageDB
from application.database.preferences_db import PreferencesDB
from application.models.message import Message
from application.services.message import MessageService
from application.utils.constants import Constants
from application.database.database_manager import DatabaseManager
from application.utils.destination_provider import DestinationProvider
from application.widgets.contextualactionbar import ContextualActionBar
from application.widgets.navigationrail import NavigationRail


class Chat:
    def __init__(self, page: ft.Page):
        self.page = page
        self.session_manager = DatabaseManager()
        self.message_list_view: ft.ListView = self.create_list_view()
        self.text_field: ft.TextField = self.create_textfield()
        self.action_bar = ContextualActionBar(page=page, original_bar=page.appbar, on_element=self.on_element_action(),
                                              on_multiple_elements=self.on_multiple_elements())
        self.message_service = MessageService(self.page)
        self.container = self.create_container()
        self.actions = self.create_actions()
        self.load_existing_messages()

    def on_element_action(self):
        return [
            ft.PopupMenuButton(
                icon=ft.icons.DOWNLOAD,
                items=[
                    ft.PopupMenuItem(text="Audio", on_click=lambda e: self.message_service.download_audio(
                        self.action_bar.selected_controls[0])),
                    ft.PopupMenuItem(text="Message", on_click=lambda e: self.message_service.download_message(
                        self.action_bar.selected_controls[0])),
                ]
            ),
            ft.IconButton(icon=ft.icons.PLAY_CIRCLE,
                          on_click=lambda e: self.message_service.toggle_play(self.action_bar.selected_controls[0])),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: self.message_service.clean_message(self.action_bar,
                                                                                                      self.message_list_view)),
        ]

    def on_multiple_elements(self):
        return [
            ft.PopupMenuButton(
                icon=ft.icons.DOWNLOAD,
                items=[
                    ft.PopupMenuItem(text="Audio", on_click=lambda e: self.message_service.download_all_audio(
                        self.action_bar.selected_controls)),
                    ft.PopupMenuItem(text="Message", on_click=lambda e: self.message_service.download_all_messages(
                        self.action_bar.selected_controls)),
                ]
            ),
            ft.IconButton(icon=ft.icons.DELETE,
                          on_click=lambda e: self.message_service.clean_selected_messages(self.action_bar,
                                                                                          self.message_list_view))
        ]

    def load_existing_messages(self):
        with self.session_manager.session_scope() as session:
            messages = session.query(Message).all()
            self.message_list_view.controls.extend(
                self.create_gesture(message) for message in messages
            )

    def create_gesture(self, message: Message):
        color = ft.colors.with_opacity(0.5,
                                       ft.colors.INVERSE_PRIMARY) if message.sender == Constants.SEND_USER else ft.colors.with_opacity(
            0.5, ft.colors.GREEN)
        margin = ft.margin.only(right=45) if message.sender == Constants.SEND_USER else ft.margin.only(left=45)
        message_content = self.message_content(message)
        return self.action_bar.gesture_control(message_content, color, margin)

    def create_container(self):
        return ft.Container(
            border_radius=5,
            margin=ft.margin.all(15),
            content=self.message_list_view,
            border=ft.border.all(1, ft.colors.with_opacity(0.5, ft.colors.PRIMARY)),
            expand=True
        )

    def message_content(self, message: Message):
        text_value = PreferencesDB(self.session_manager).get_preference(
            Constants.TEXT_CHAT_PREFERENCE) or Constants.TEXT_CHAT
        return ft.Markdown(value=message.content, selectable=True, extension_set="gitHubWeb",
                           code_theme="atom-one-dark",
                           code_style=ft.TextStyle(font_family="Roboto Mono", size=text_value, italic=True),
                           key=message.to_json())

    def answer_gpt(self):
        with self.session_manager.session_scope() as session:
            messages = session.query(Message).all()
            message_list = [{'role': message.sender, 'content': message.content} for message in messages]

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_list,
            provider=g4f.Provider.GptGo,
            stream=True
        )

        with self.session_manager.session_scope() as session:
            message = MessageDB(self.session_manager).create_message(Constants.SEND_BOT, 'Esperando Respuesta...',
                                                                     session)
            gesture = self.create_gesture(message)
            self.message_list_view.controls.append(gesture)
            self.page.update()
            message.content = ''
            for texto in response:
                message.content += texto
                gesture.content = self.create_gesture(message)
                self.page.update()

    def send_message(self):
        with self.session_manager.session_scope() as session:
            message = MessageDB(self.session_manager).create_message(Constants.SEND_USER, self.text_field.value,
                                                                     session)
            self.update_message_list_view(message)
            self.answer_gpt()

        self.text_field.value = ""

    def update_message_list_view(self, new_message_content: Message):
        gesture = self.create_gesture(new_message_content)
        self.message_list_view.controls.append(gesture)
        self.page.update()

    def create_textfield(self):
        return ft.TextField(border_radius=20, expand=True, multiline=True)

    @staticmethod
    def create_btn_action(icon, tooltip, callback, *args, **kwargs):
        return ft.IconButton(
            icon=icon,
            bgcolor=ft.colors.PRIMARY,
            icon_color=ft.colors.INVERSE_PRIMARY,
            tooltip=tooltip,
            on_click=lambda e: callback(*args, **kwargs)
        )

    def create_actions(self):
        return ft.Container(
            margin=ft.margin.only(left=15, right=15),
            content=ft.Row([
                self.create_btn_action(ft.icons.DELETE, "Limpiar Mensajes", self.message_service.ask_clear_all_messages, self.message_list_view),
                self.text_field,
                self.create_btn_action(ft.icons.SEND, "Enviar Mensaje", self.send_message),
            ]),
        )

    def view(self):
        return ft.Row(
            [
                NavigationRail(self.page, DestinationProvider.update_page_chat(self.page),
                               Constants.INDEX_CHAT_RAIL).navigation(
                    DestinationProvider.get_chat_destinations()),
                ft.VerticalDivider(width=1),
                ft.Column([
                    self.container,
                    self.actions
                ], expand=True)
            ],
            expand=True,
        )

    @staticmethod
    def create_list_view():
        return ft.ListView(expand=1, spacing=25, padding=15, auto_scroll=False)
