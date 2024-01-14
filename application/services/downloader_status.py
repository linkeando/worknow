import re
import flet as ft

from application.utils.page import UtilPage


class LoggerDownload:
    WARNING_DASH_M4A = 'writing DASH m4a'

    def __init__(self, page: ft.Page):
        self.page = page
        self.progress_download = ft.ProgressRing(width=24, height=24, stroke_width=6)
        self.progress_download.visible = False
        self.info_row_added = False  # Variable para rastrear si info_row ya se ha agregado
        self.info_row = self.create_info_row()

    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def create_info_row(self):
        return ft.Row([self.progress_download, ft.Text("", size=18, weight=ft.FontWeight.BOLD)])

    def add_info_row(self):
        if not self.info_row_added:
            self.page.add(self.info_row)
            self.info_row_added = True


    def update_interface(self):
        self.info_row.controls[1].value = ''
        self.progress_download.visible = False
        self.page.update()

    def info(self, msg):
        self.add_info_row()
        self.info_row.controls[1].value = 'Downloading ...'
        self.page.update()
        self.progress_download.visible = True
        percentage_match = re.compile(r'(\d+\.\d+)%').search(msg)
        if percentage_match:
            percentage = float(percentage_match.group(1))
            self.progress_download.value = percentage
            self.info_row.controls[1].value = msg
            self.page.update()

    def show_message_dialog(self, msg):
        dialog_modal = UtilPage(self.page).create_modal_simple(msg)
        self.page.dialog = dialog_modal
        dialog_modal.open = True
        self.page.update()

    def warning(self, msg):
        if self.WARNING_DASH_M4A not in msg:
            self.show_message_dialog(msg)

    def error(self, msg):
        self.show_message_dialog(msg)

    def hook_download(self, event):
        if event['status'] == 'finished':
            self.update_interface()
            if self.info_row_added:
                self.page.remove(self.info_row)
                self.info_row_added = False

