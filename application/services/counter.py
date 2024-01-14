from collections import Counter

import flet as ft


class CounterService:
    def __init__(self, page: ft.Page):
        self.page = page

    def update_all(self, text_to_count: str):
        self.update_word_count(text_to_count)
        self.update_character_count(text_to_count)
        self.update_unique_words_count(text_to_count)
        self.page.update()

    def read_txt_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return f"El archivo '{path}' no fue encontrado."
        except Exception as e:
            return f"Error al leer el archivo: {e}"

    def _read_txt(self, e: ft.FilePickerResultEvent, input_text):
        if e.files and e.files[0].path:
            read_text = self.read_txt_file(e.files[0].path)
            input_text.content.value = read_text
            self.update_all(read_text)
        else:
            print("Error: No se seleccionó ningún archivo.")

    def read(self, input_text: ft.Container):
        pick_files_dialog = ft.FilePicker(on_result=lambda e: self._read_txt(e, input_text))
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        pick_files_dialog.pick_files('Selecciona Archivo TXT', allowed_extensions=['txt'], allow_multiple=False)

    def clean(self, input_text: ft.Container):
        input_text.content.value = ''
        self.update_card_content(0, '0')
        self.update_card_content(1, '0')
        self.update_card_content(2, '0')
        self.update_card_content(3, '0')
        self.page.update()

    def copy(self, input_text: ft.Container):
        text_to_copy = input_text.content.value
        self.page.set_clipboard(text_to_copy)
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Texto Copiado En El Portapapeles"))
        self.page.snack_bar.open = True
        self.page.update()

    def on_text_change_input(self, e: ft.ControlEvent, input_text: ft.Container):
        text_to_search: str = input_text.content.value
        words_to_search: str = e.control.value

        word_frequencies = Counter(text_to_search.split())
        frequency_of_word = word_frequencies.get(words_to_search, 0)

        self.update_card_content(3, str(frequency_of_word))
        self.page.update()

    def on_text_change_main(self, e: ft.ControlEvent):
        text_to_count: str = e.control.value
        self.update_all(text_to_count)

    def update_word_count(self, text: str):
        words = len(text.split())
        self.update_card_content(0, str(words))

    def update_character_count(self, text: str):
        total_characters = len(text)
        self.update_card_content(1, str(total_characters))

    def update_unique_words_count(self, text: str):
        words = text.split()
        unique_words = len(set(words))
        self.update_card_content(2, str(unique_words))

    def update_card_content(self, card_index: int, new_value: str):
        column: ft.Column = self.page.controls[0].content
        container_cards: ft.Container = column.controls[2]
        list_cards = container_cards.content.controls

        card: ft.Card = list_cards[card_index]
        card_column: ft.Column = card.content
        card_container_change: ft.Container = card_column.controls[2]
        card_container_change.content.value = new_value
