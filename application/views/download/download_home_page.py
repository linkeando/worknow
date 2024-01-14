import flet as ft

from concurrent.futures import ThreadPoolExecutor
from typing import List

from application.services.downloader_video import DownloaderVideo
from application.services.video import Video
from application.utils.constants import Constants
from application.utils.destination_provider import DestinationProvider
from application.utils.download import DownloadUtil
from application.widgets.contextualactionbar import ContextualActionBar
from application.widgets.navigationrail import NavigationRail


class Download:
    TEXT_WITHOUT_VIDEO = '¡Bienvenido! Busca videos para descargar y disfruta del contenido.'

    def __init__(self, page: ft.Page):
        self.page = page
        self.action_bar = ContextualActionBar(page=page, original_bar=page.appbar, on_element=self.on_element_action(),
                                              on_multiple_elements=self.on_multiple_elements())
        self.video_service = Video(self.page, self.action_bar)
        self.downloader_video = DownloaderVideo(self.page)
        self.video_list = self.video_service.preferences.get_preference(Constants.VIDEO_LIST) or []
        self.text_field: ft.TextField = self.create_textfield()

    def copy_text(self):
        video = str(self.action_bar.selected_controls[0].key)
        self.page.set_clipboard(video)
        self.page.snack_bar = ft.SnackBar(ft.Text("Informacion Copiado Al Portapapeles"))
        self.page.snack_bar.open = True
        self.page.update()

    def on_element_action(self):
        return [
            ft.IconButton(icon=ft.icons.COPY,
                          on_click=lambda e: self.downloader_video.copy_element(self.action_bar.selected_controls)),
        ]

    def on_multiple_elements(self):
        return [
            ft.PopupMenuButton(
                icon=ft.icons.DOWNLOAD,
                items=[
                    ft.PopupMenuItem(text="Video", icon=ft.icons.VIDEO_FILE,
                                     on_click=lambda e: self.downloader_video.download_all_video(
                                         self.action_bar.selected_controls)),
                    ft.PopupMenuItem(text="Audio", icon=ft.icons.AUDIO_FILE,
                                     on_click=lambda e: self.downloader_video.download_all_audio(
                                         self.action_bar.selected_controls)),
                    ft.PopupMenuItem(text="Solo Video", icon=ft.icons.VIDEO_STABLE,
                                     on_click=lambda e: self.downloader_video.download_all_only_video(
                                         self.action_bar.selected_controls)),

                ]
            ),
            ft.IconButton(icon=ft.icons.COPY,
                          on_click=lambda e: self.downloader_video.copy_elements(self.action_bar.selected_controls)),
        ]

    def _associate_gestures(self, videos: List[ft.Card]):
        with ThreadPoolExecutor() as executor:
            return list(executor.map(self.action_bar.gesture_control, videos))

    def create_grid_card_videos(self):
        grid_view = DownloadUtil.create_grid_view()
        videos = [DownloadUtil(self.page).create_card_video(video) for video in self.video_list]
        grid_view.controls = self._associate_gestures(videos)
        return grid_view

    def empty_videos(self):
        return ft.Container(alignment=ft.alignment.center, margin=ft.margin.all(15),
                            content=ft.Text(self.TEXT_WITHOUT_VIDEO, size=18, weight=ft.FontWeight.BOLD,
                                            italic=True), expand=True)

    def create_grid_videos(self):
        return ft.Container(
            content=self.create_grid_card_videos(),
            expand=True,
        )

    def grid_videos(self):
        return self.empty_videos() if not self.video_list else self.create_grid_videos()

    def create_textfield(self):
        return ft.TextField(border_radius=20, expand=True, multiline=True, max_lines=10)

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
                self.create_btn_action(ft.icons.UPLOAD_FILE, "Subir TXT", self.video_service.selected_path_read_txt),
                self.text_field,
                self.create_btn_action(ft.icons.SEND, "Buscar Video", self.video_service.search_video, self.text_field),
            ]),
        )

    def view(self):
        return ft.Row(
            [
                NavigationRail(self.page, DestinationProvider.update_page_downloader(self.page),
                               Constants.INDEX_DOWNLOAD_RAIL).navigation(
                    DestinationProvider.get_downloader_destinations()),
                ft.VerticalDivider(width=1),
                ft.Column([
                    self.grid_videos(),
                    self.create_actions()
                ], expand=True)
            ],
            expand=True,
        )
