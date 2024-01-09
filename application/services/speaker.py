import os
from contextlib import suppress

import pygame
import pyttsx3

from application.database.database_manager import DatabaseManager
from application.database.preferences_db import PreferencesDB
from application.utils.constants import Constants


class Speaker:
    def __init__(self, frequency=11025, size=-16, channels=2):
        self.session_manager = DatabaseManager()
        self.preferences = PreferencesDB(self.session_manager)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', self.preferences.get_preference(Constants.RATE_PREFERENCE) or Constants.RATE_AUDIO)
        pygame.mixer.init(frequency=frequency, size=size, channels=channels)
        self.audio_cache = {}  # Diccionario para almacenar objetos pygame.mixer.Sound
        self.is_playing = False  # Variable para controlar el estado de reproducción

    def text_to_audio(self, text, file_name="file.mp3"):
        try:
            audio = self.audio_cache.get(text)
            if audio is not None:
                return audio

            self.engine.save_to_file(text, file_name)
            self.engine.runAndWait()

            with open(file_name, 'rb') as audio_file:
                mp3_bytes = audio_file.read()

            audio = pygame.mixer.Sound(buffer=mp3_bytes)
            self.audio_cache[text] = audio
            return audio
        except Exception as e:
            print(f"Error during text-to-audio conversion: {e}")
            return None
        finally:
            self.safe_remove(file_name)

    def play_audio(self, audio):
        if not self.is_playing:
            audio.play()
            self.is_playing = True

    def stop(self, audio):
        audio.stop()
        self.is_playing = False

    @staticmethod
    def safe_remove(file_path):
        with suppress(FileNotFoundError):
            os.remove(file_path)
