import functools
from concurrent.futures import ThreadPoolExecutor

import flet as ft

from typing import Dict

import yt_dlp

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.services.process_video import ProcessVideo
from application.utils.constants import Constants
from application.utils.download import DownloadUtil
from application.utils.page import UtilPage
from application.widgets.contextualactionbar import ContextualActionBar


class Video:
    def __init__(self, page: ft.Page, action_bar: ContextualActionBar):
        self.page = page
        self.action_bar = action_bar
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)
        self.loading_animation = ft.ProgressRing(stroke_width=8)

    def message_alert(self):
        dialog_modal = UtilPage(self.page).create_modal_simple(f'Videos Cargados Correctamente')
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def load_animation(self):
        container_animation = ft.Container(
            alignment=ft.alignment.center,
            content=self.loading_animation
        )
        self.page.add(container_animation)

    @staticmethod
    def load_video(url):
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)

    def update_page(self, new_videos):
        row_view = self.page.controls[0].content
        column_view = row_view.controls[2]
        container_grid = column_view.controls[0]

        # Crear un nuevo GridView
        grid_view = ft.GridView(expand=1, max_extent=420, child_aspect_ratio=Constants.ASPECT_GRID, spacing=15,
                                run_spacing=15)

        with ThreadPoolExecutor() as executor:
            videos_update = list(executor.map(self.action_bar.gesture_control,[DownloadUtil(self.page).create_card_video(video) for video in new_videos]))

        grid_view.controls = videos_update

        # Reemplazar el contenido actual con el nuevo GridView
        container_grid.content = grid_view

        self.loading_animation.visible = False
        self.page.update()

    def search_video(self, video_search: ft.TextField):
        self.load_animation()
        videos = self._process_url(video_search.value)
        self.preferences.set_preference(Constants.VIDEO_LIST, videos)
        self.update_page(videos)

    def primary_data(self, data_video: Dict):
        return {
            'id': data_video.get('id'),
            'title': data_video.get('title'),
            'formats': self._extract_format_info(data_video),
            'channel': data_video.get('channel'),
            'description': data_video.get('description'),
            'original_url': data_video.get('original_url'),
            'time_video': data_video.get('duration_string'),
            'thumbnail': data_video.get('thumbnail')
        }

    def _extract_format_info(self, data_video: Dict):
        extracted_info = []
        format_note_sets = {}

        for video in data_video.get('formats', []):
            format_id, acodec, vcodec, note, filesize, ext = (video.get('format_id', ''), video.get('acodec', ''),
                                                              video.get('vcodec', ''), video.get('format_note', ''),
                                                              video.get('filesize', ''), video.get('ext', '')
                                                              )

            if self._should_skip_format(note):
                continue

            type_value = self._determine_type(acodec, vcodec)

            if self._should_add_format(type_value, note, format_note_sets):
                info_dict = self._get_info_dict_formats(format_id, note, filesize, ext, video.get('url'), type_value)
                if not info_dict.get('url').endswith('.m3u8'):
                    extracted_info.append(info_dict)
                    format_note_sets.setdefault(note, set()).add(type_value)

        return extracted_info

    @staticmethod
    def _get_info_dict_formats(format_id, note, filesize, ext, url, type_value):
        return {
            'format_id': format_id,
            'quality': note,
            'filesize': filesize,
            'ext': ext,
            'url': url,
            'type': type_value
        }

    @staticmethod
    def _should_skip_format(format_note):
        return format_note in ['Default', 'storyboard']

    @staticmethod
    def _determine_type(acodec, vcodec):
        return 'only_video' if acodec == 'none' and vcodec != 'none' else (
            'audio' if acodec != 'none' and vcodec == 'none' else 'video')

    @staticmethod
    def _should_add_format(type_value, format_note, format_note_sets):
        return type_value not in format_note_sets.get(format_note, set())

    def _read_file(self, e: ft.FilePickerResultEvent):
        self.load_animation()
        urls_data = ProcessVideo(e.files[0].path).read_file()

        with ThreadPoolExecutor() as executor:
            results = [video for sublist in executor.map(functools.partial(self._process_url), urls_data) if sublist for
                       video in sublist]

        self.preferences.set_preference(Constants.VIDEO_LIST, results)
        self.update_page(results)
        return results

    def _process_url(self, url):
        try:
            video = self.load_video(url)
            playlist_entries = video.get('entries', [])

            if playlist_entries:
                videos_data = [self.primary_data(entry) for entry in playlist_entries]
            else:
                videos_data = [self.primary_data(video)]

            return videos_data
        except Exception as e:
            print(f"Error al procesar la URL {url}: {e}")
            return []

    def selected_path_read_txt(self):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self._read_file(e))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.pick_files('Selecciona Archivo TXT', allowed_extensions=['txt'], allow_multiple=False)
