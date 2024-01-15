import os
import zipfile
from typing import Dict, List

import flet as ft
import yt_dlp

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.services.downloader_status import LoggerDownload
from application.utils.constants import Constants


class DownloaderVideo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.logger = LoggerDownload(self.page)
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)
        self.quality_download = self.preferences.get_preference(
            Constants.TIPE_DOWNLOAD_QUALITY) or Constants.TIPE_DOWNLOAD_QUALITY
        self.path_download_videos = self.preferences.get_preference(
            Constants.PATH_DOWNLOAD_VIDEOS) or self.session_manager.get_app_data_dir()

    @staticmethod
    def determinate_format(video, type):
        return [enlace for enlace in video.get('formats', []) if 'type' in enlace and enlace['type'] == type]

    @staticmethod
    def format_filesize(filesize):
        if filesize is None or filesize == '':
            return 'N/A'

        try:
            filesize = float(filesize)
        except ValueError:
            return 'Invalid Filesize'

        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while filesize >= 1024 and i < len(units) - 1:
            filesize /= 1024.0
            i += 1

        return "{:.2f}{}".format(filesize, units[i])

    def download_option(self, video: Dict, output: str, url_original: str, type_download=''):
        output = f'{output}.{video.get('ext')}'
        if len(type_download) > 0:
            self.save_path_download_video_history(type_download, output)
        ydl_opts = {
            'format': video.get('format_id'),
            'outtmpl': output,
            'logger': self.logger,
            'progress_hooks': [lambda e: self.logger.hook_download(e)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url_original)

    def create_generic_table(self, columns: List[str], data: List[Dict], on_select_func, *args, **kwargs):
        ft_columns = [ft.DataColumn(ft.Text(column)) for column in columns]

        def get_cell_value(column, row):
            if column == 'filesize':
                return self.format_filesize(row.get('filesize'))
            else:
                return str(row.get(column, ''))

        ft_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(get_cell_value(column, row)))
                    for column in columns
                ],
                on_select_changed=lambda e, video=row: on_select_func(video, *args, **kwargs)
            ) for row in data
        ]

        return ft.Column([
            ft.DataTable(
                columns=ft_columns,
                rows=ft_rows,
            ),
        ], scroll=ft.ScrollMode.AUTO)

    def update_download_modal(self, title, data: List[Dict], on_select_func, *args, **kwargs):
        columns = ['quality', 'filesize', 'ext']
        dlg = ft.AlertDialog(title=ft.Text(title),
                             content=self.create_generic_table(columns, data, on_select_func, *args, **kwargs),
                             actions_alignment=ft.MainAxisAlignment.END)
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def download_video(self, video: Dict):
        videos = self.determinate_format(video, 'video')
        output = os.path.join(self.path_download_videos, video.get('title'))
        self.update_download_modal('Video', videos, self.download_option, output, video.get('original_url'), 'video')

    def download_audio(self, video: Dict):
        audios = self.determinate_format(video, 'audio')
        output = os.path.join(self.path_download_videos, f'{video.get('title')}')
        self.update_download_modal('Audio', audios, self.download_option, output, video.get('original_url'), 'audio')

    def download_only_video(self, video: Dict):
        only_video = self.determinate_format(video, 'only_video')
        output = os.path.join(self.path_download_videos, video.get('title'))
        self.update_download_modal('Video Sin Audio', only_video, self.download_option, output,
                                   video.get('original_url'), 'solo_video')

    def create_details_view(self, video: dict):
        return ft.Column([
            ft.Text(f'Titulo: {video.get('title')}\n', size=15, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text(f'Descripcion: {video.get('description')}\n', size=15, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text(f'Duracion: {video.get('time_video')} Min\n', size=15, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Container(alignment=ft.alignment.center,
                         content=ft.Image(src=video.get('thumbnail'), height=130, width=130))
        ], scroll=ft.ScrollMode.AUTO)

    def details_video(self, video: Dict):
        dlg = ft.AlertDialog(title=ft.Text('Detalles'), content=self.create_details_view(video),
                             actions_alignment=ft.MainAxisAlignment.END)
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def copy_element(self, controls: List[ft.Control]):
        video = str(controls[0].key)
        self.copy_clipboard(video)

    def copy_elements(self, controls: List[ft.Control]):
        video_list = [video.key for video in controls]
        self.copy_clipboard(str(video_list))

    def copy_clipboard(self, text):
        self.page.set_clipboard(text)
        self.page.snack_bar = ft.SnackBar(ft.Text("Informacion Copiado Al Portapapeles"))
        self.page.snack_bar.open = True
        self.page.update()

    @staticmethod
    def get_best_format_id(videos):
        return max(int(video['format_id']) for video in videos)

    @staticmethod
    def get_middle_format_id(videos):
        format_ids = [int(video['format_id']) for video in videos]
        middle_index = len(format_ids) // 2

        if len(format_ids) % 2 == 0:
            return format_ids[middle_index]
        else:
            return format_ids[middle_index]

    @staticmethod
    def get_worst_format_id(videos):
        return min(int(video['format_id']) for video in videos)

    def define_type_download(self, formats):
        quality_mapping = {
            'Alta': self.get_best_format_id,
            'Media': self.get_middle_format_id,
            'Baja': self.get_middle_format_id,
        }

        quality_function = quality_mapping.get(self.quality_download, self.get_middle_format_id)
        return quality_function(formats)

    def download_all_audio(self, controls: List[ft.Control]):
        video_list: List[Dict] = [video.key for video in controls]
        url_list = [video.get('original_url') for video in video_list]
        title_list = [video.get('title') for video in video_list]
        audio_list = [self.determinate_format(video, 'audio') for video in video_list]

        zip_filename = os.path.join(self.path_download_videos, 'audio_files.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for formats, url, title in zip(audio_list, url_list, title_list):
                format_id = self.define_type_download(formats)
                ext = formats[0]['ext']
                output_path = f'{title}.{ext}'

                download_info = {
                    'format_id': str(format_id),
                    'url': url,
                    'title': title,
                    'ext': ext,
                }

                self.download_option(download_info, download_info.get('title'),
                                     download_info.get('url'))
                zip_file.write(output_path)
                os.remove(output_path)
        self.save_path_download_video_history('audio', zip_filename)

    def download_all_video(self, controls: List[ft.Control]):
        video_list: List[Dict] = [video.key for video in controls]
        url_list = [video.get('original_url') for video in video_list]
        title_list = [video.get('title') for video in video_list]
        videos = [self.determinate_format(video, 'video') for video in video_list]

        zip_filename = os.path.join(self.path_download_videos, 'video_files.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for formats, url, title in zip(videos, url_list, title_list):
                format_id = self.define_type_download(formats)
                ext = formats[0]['ext']
                output_path = f'{title}.{ext}'

                download_info = {
                    'format_id': str(format_id),
                    'url': url,
                    'title': title,
                    'ext': ext,
                }

                self.download_option(download_info, download_info.get('title'),
                                     download_info.get('url'))
                zip_file.write(output_path)
                os.remove(output_path)
        self.save_path_download_video_history('video', zip_filename)

    def download_all_only_video(self, controls: List[ft.Control]):
        video_list: List[Dict] = [video.key for video in controls]
        url_list = [video.get('original_url') for video in video_list]
        title_list = [video.get('title') for video in video_list]
        videos_without_audio = [self.determinate_format(video, 'only_video') for video in video_list]

        zip_filename = os.path.join(self.path_download_videos, 'video_without_audio_files.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for formats, url, title in zip(videos_without_audio, url_list, title_list):
                format_id = self.define_type_download(formats)
                ext = formats[0]['ext']
                output_path = f'{title}.{ext}'

                download_info = {
                    'format_id': str(format_id),
                    'url': url,
                    'title': title,
                    'ext': ext,
                }

                self.download_option(download_info, download_info.get('title'),
                                     download_info.get('url'))
                zip_file.write(output_path)
                os.remove(output_path)
        self.save_path_download_video_history('solo_video', zip_filename)

    def save_path_download_video_history(self, tipo_archivo, filename):
        historial_descargas_video = PreferencesDB(self.session_manager).get_preference(
            Constants.DOWNLOAD_TYPE_SAVE_FILE,
            {'video': [], 'audio': [], 'solo_video': []})

        nuevo_elemento_descargado = {tipo_archivo.capitalize(): filename}
        historial_descargas_video[tipo_archivo].append(nuevo_elemento_descargado)

        PreferencesDB(self.session_manager).set_preference(Constants.DOWNLOAD_TYPE_SAVE_FILE, historial_descargas_video)
