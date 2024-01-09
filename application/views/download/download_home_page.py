from concurrent.futures import ThreadPoolExecutor

import flet as ft

from application.utils.constants import Constants
from application.widgets.contextualactionbar import ContextualActionBar
from application.widgets.navigationrail import NavigationRail


class Download:
    def __init__(self, page: ft.Page):
        self.page = page
        self.num_images = 1
        self.contextual_action_bar = ContextualActionBar(page=page, original_bar=page.appbar, on_element=[],
                                                         on_multiple_elements=[])

    @staticmethod
    def _create_image(image_index):
        return ft.Card(
            ft.Column([
                ft.Container(
                    expand=True,
                    content=ft.Image(
                        src=f"https://picsum.photos/200/200?0",
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                        width=300,
                        expand=True
                    ),
                ),
                ft.Container(
                    margin=ft.margin.all(10),
                    expand=True,
                    alignment=ft.alignment.top_right,
                    content=ft.Text(
                        'Lorem ipsum es el texto que se usa habitualmente en diseño gráfico en demostraciones de tipografías o de borradores de diseño para probar el diseño visual',
                    ),
                ),
                ft.Row([
                    ft.TextButton('Descargar'),
                    ft.TextButton('Video')
                ])
            ])
        )

    @staticmethod
    def _create_grid_view():
        return ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=Constants.ASPECT_GRID,
            spacing=3,
            run_spacing=3,
        )

    def _associate_gestures(self, images_list):
        with ThreadPoolExecutor() as executor:
            return list(executor.map(self.contextual_action_bar.gesture_control, images_list))

    def _create_text_field(self):
        ft.Container(
            expand=True,
            margin=ft.margin.all(10),
            content=ft.Row([

            ])
        )

    def create_image_gallery(self):
        # Create a grid view to display the images
        images = self._create_grid_view()

        # Create a list of images for the grid
        images_list = [self._create_image(i) for i in range(self.num_images)]

        # Associate gestures if needed, otherwise use the original images list
        images.controls = self._associate_gestures(images_list)  # Comment this line and use the original images_list

        return images

    def view(self):
        return ft.Row(
            [
                NavigationRail(self.page, self._update_body_content, Constants.INDEX_DOWNLOAD_RAIL).navigation(),
                ft.VerticalDivider(width=1),
                ft.Column([
                    ft.Container(
                        content=self.create_image_gallery(),
                        expand=True
                    ),
                    ft.TextField()
                ], expand=True)
            ],
            expand=True,
        )

    def _update_body_content(self):
        print(self.page.session.get(Constants.INDEX_DOWNLOAD_RAIL))
