import flet as ft
from application.utils.destination_provider import DestinationProvider


class NavigationRail:
    def __init__(self, page: ft.Page, update_callback, session_key):
        self.page = page
        self.update_callback = update_callback
        self.session_key = session_key

    def _update_page(self, event):
        self.page.session.set(self.session_key, event.control.selected_index)
        self.update_callback()

    @staticmethod
    def create_destination(icon, selected_icon, label, label_content=None):
        return ft.NavigationRailDestination(
            icon=icon,
            selected_icon=selected_icon,
            label=label,
            label_content=label_content
        )

    def navigation(self, destinations=None):
        index = self.page.session.get(self.session_key)
        selected_index = 0 if index is None else index

        return ft.NavigationRail(
            group_alignment=-0.25,
            on_change=lambda event: self._update_page(event),
            selected_index=selected_index,
            destinations=destinations or DestinationProvider.get_default_destinations(),
        )
