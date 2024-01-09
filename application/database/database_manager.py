import sys
import os

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from application.models.base import Base
from appdirs import user_data_dir
from contextlib import contextmanager

from application.utils.page import UtilPage


class DatabaseManager:
    def __init__(self, db_filename='worknow.db'):
        self.db_filename = db_filename
        self.db_path = self.get_database_path()
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_database_path(self):
        db_path = os.path.join(self.get_app_data_dir(), self.db_filename)
        return db_path

    @staticmethod
    def get_app_data_dir():
        app_name = 'WorkNow'
        app_author = 'TecnoMagia_WorkNow'
        app_data_dir = user_data_dir(appname=app_name, appauthor=app_author)

        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)

        return app_data_dir

    @staticmethod
    def get_base_dir():
        if getattr(sys, 'frozen', False):
            return os.path.abspath(os.path.dirname(sys.argv[0]))
        elif __file__:
            return os.path.abspath(os.path.dirname(__file__))
        return os.getcwd()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()

    def download_database(self, destination_path=None):
        local_database_path = self.get_database_path()

        try:
            with open(local_database_path, 'rb') as local_db_file:
                new_database_content = local_db_file.read()

            target_path = os.path.join(destination_path or '', self.db_filename)

            with open(target_path, 'wb') as target_db_file:
                target_db_file.write(new_database_content)

        except Exception as e:
            print(f"Error al descargar o guardar la base de datos: {e}")

    def upload_database(self, source_path, page):
        try:
            with open(source_path, 'rb') as source_db_file:
                new_database_content = source_db_file.read()

            local_database_path = self.get_database_path()

            with open(local_database_path, 'wb') as local_db_file:
                local_db_file.write(new_database_content)

            dialog_modal = UtilPage(page).create_modal_simple('Base de datos subida y reemplazada exitosamente.')
            page.dialog = dialog_modal
            dialog_modal.open = True
            page.update()

        except Exception as e:
            print(f"Error al subir o reemplazar la base de datos: {e}")
