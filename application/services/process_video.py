from urllib.parse import urlparse
from pathlib import Path


class ProcessVideo:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    @staticmethod
    def _is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def read_file(self):
        try:
            content = self.file_path.read_text()
            return [url for url in content.split() if self._is_valid_url(url)]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"El archivo '{self.file_path}' no fue encontrado.") from e
        except Exception as e:
            raise Exception(f"Ocurrió un error al leer el archivo: {e}") from e
