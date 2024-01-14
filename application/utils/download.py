import webbrowser
from typing import Dict

import flet as ft

from application.services.downloader_video import DownloaderVideo
from application.utils.constants import Constants


class DownloadUtil:
    def __init__(self, page: ft.Page):
        self.page = page
        self.downloader_video = DownloaderVideo(self.page)

    def create_menu_download(self, video: Dict):
        return ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=ft.Text("Download"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text("Audio"),
                            leading=ft.Icon(ft.icons.AUDIOTRACK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.HOVERED: ft.colors.with_opacity(0.5, ft.colors.GREEN_100)}),
                            on_click=lambda e: self.downloader_video.download_audio(video)
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Video"),
                            leading=ft.Icon(ft.icons.VIDEO_CAMERA_BACK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.HOVERED: ft.colors.with_opacity(0.5, ft.colors.BLUE_100)}),
                            on_click=lambda e: self.downloader_video.download_video(video)
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Only Video"),
                            leading=ft.Icon(ft.icons.CAMERA),
                            style=ft.ButtonStyle(
                                bgcolor={ft.MaterialState.HOVERED: ft.colors.with_opacity(0.5, ft.colors.RED_100)}),
                            on_click=lambda e: self.downloader_video.download_only_video(video)
                        )
                    ]
                ),
            ]
        )

    @staticmethod
    def create_grid_view():
        return ft.GridView(
            expand=1,
            max_extent=420,  # Ajusta el tamaño máximo de la tarjeta
            child_aspect_ratio=Constants.ASPECT_GRID,
            spacing=15,  # Ajusta el espaciado entre las tarjetas
            run_spacing=15,  # Ajusta el espaciado entre las filas de tarjetas
        )

    def create_card_video(self, video: Dict):
        return ft.Card(
            ft.Column([
                ft.Image(
                    src=video.get('thumbnail'),
                    width=420,
                    height=125,
                    fit=ft.ImageFit.FILL,
                ),
                ft.Container(
                    padding=ft.padding.all(15),
                    expand=True,
                    alignment=ft.alignment.top_center,
                    content=ft.Text(video.get('title'), size=14, weight=ft.FontWeight.BOLD),
                ),
                ft.Row([
                    self.create_menu_download(video),
                    ft.TextButton('Video', on_click=lambda e: webbrowser.open(video.get('original_url'))),
                    ft.TextButton('Info', on_click=lambda e: self.downloader_video.details_video(video)),
                ])
            ]),
            key=video
        )
