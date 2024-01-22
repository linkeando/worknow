from typing import List, TypeVar, Dict, Optional
import flet as ft

T = TypeVar('T')


class ContextualActionBar:
    def __init__(self, page: ft.Page, enable_single_vert: bool = True,
                 on_element=None, on_multiple_elements=None, original_bar=None):
        self.page = page
        self.original_bar = original_bar
        self.on_element = on_element
        self.on_multiple_elements = on_multiple_elements

        # CONTROLS
        self.selected_controls: List[T] = []
        self.selection_mode = False
        self.controls: Dict[T, Dict[str, ft.Container]] = {}

        # VERT CONTROL
        self.enable_single_vert = enable_single_vert

    def _select_all(self):
        print(self.on_element)
        self.selected_controls = list(self.controls.keys())
        self._update_bar()
        self._update_color_all_elements()

    def _copy_text(self, text):
        self.page.set_clipboard(text)
        self.page.snack_bar = ft.SnackBar(ft.Text("Mensaje Copiado Al Portapapeles"))
        self.page.snack_bar.open = True
        self.page.update()

    def _default_one_element(self, item):
        menu_items = [
            ft.PopupMenuItem(icon=ft.icons.SELECT_ALL, text="Select All.", on_click=lambda e: self._select_all()),
        ]

        if getattr(item, 'value', None):
            menu_items.append(ft.PopupMenuItem(icon=ft.icons.COPY, text="Copiar",
                                               on_click=lambda e: self._copy_text(item.value)))

        return [ft.PopupMenuButton(items=menu_items)]

    def _on_element(self, item):
        if not self.enable_single_vert:
            return self.on_element if self.on_element is not None else []
        return self.on_element + self._default_one_element(item)

    def _on_multiple_element(self):
        return self.on_multiple_elements if self.on_multiple_elements is not None else []

    def _action_items(self, items):
        if len(items) == 1:
            return self._on_element(items[0])
        elif len(items) > 1:
            return self._on_multiple_element()

    def _appbar_control(self, selected_items, background_color):
        return ft.AppBar(
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: self.exit_selection_mode()),
            title=ft.Text(str(len(selected_items))),
            actions=self._action_items(selected_items),
        )

    def _update_bar(self):
        color_preferred = ft.colors.with_opacity(0.25,
                                                 ft.colors.LIGHT_BLUE) if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.with_opacity(
            0.25, ft.colors.PURPLE)
        self.page.appbar = self._appbar_control(self.selected_controls,
                                                color_preferred) if self.selected_controls else self.original_bar
        self.page.update()

    @staticmethod
    def _content_control(control: T, bgcolor, margin: Optional[ft.Margin] = None):
        return ft.Container(
            content=control,
            padding=15,
            border_radius=15,
            bgcolor=bgcolor,
            margin=margin,
        )

    def _handle_long_press(self, e, control: T):
        if control not in self.selected_controls:
            self.selected_controls.append(control)
            self.selection_mode = True
            self._update_bar()
            self._update_control_colors(control)

    def _handle_tap(self, e, control: T):
        if self.selection_mode:
            self.selected_controls.remove(
                control) if control in self.selected_controls else self.selected_controls.append(control)
            self.selection_mode = len(self.selected_controls) > 0
            self._update_bar()
            self._update_control_colors(control)

    def _update_control_colors(self, control: T):
        control_info = self.controls.get(control)
        if control_info:
            container = control_info['container']
            color_preferred = ft.colors.with_opacity(0.75,
                                                     ft.colors.YELLOW) if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.with_opacity(
                0.25, ft.colors.PURPLE)
            color = color_preferred if control in self.selected_controls else control_info['bgcolor']
            container.bgcolor = color
            self.page.update()

    def _update_color_all_elements(self):
        for control_info in self.controls.values():
            container = control_info['container']
            color_preferred = ft.colors.with_opacity(0.75,
                                                     ft.colors.YELLOW) if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.colors.with_opacity(
                0.25, ft.colors.PURPLE)
            color = color_preferred if control_info['control'] in self.selected_controls else control_info['bgcolor']
            container.bgcolor = color

        self.page.update()

    def _original_color_elements(self):
        for control_info in self.controls.values():
            container = control_info['container']
            container.bgcolor = control_info['bgcolor']

    def exit_selection_mode(self):
        self._original_color_elements()
        self.selected_controls = []
        self.selection_mode = False
        self.page.appbar = self.original_bar
        self.page.update()

    def gesture_control(self, control: T, container_bgcolor = None,
                        margin: Optional[ft.Margin] = None):
        container = self._content_control(control, container_bgcolor, margin)
        self.controls[control] = {'container': container, 'bgcolor': container_bgcolor, 'control': control}
        gesture_detector = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_long_press_start=lambda e: self._handle_long_press(e, control),
            on_tap=lambda e: self._handle_tap(e, control),
            content=container
        )
        return gesture_detector
