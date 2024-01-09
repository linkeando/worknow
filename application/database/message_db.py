import logging
from sqlalchemy.exc import SQLAlchemyError

from application.models.message import Message


class MessageDB:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    @staticmethod
    def create_message(sender, content, session):
        try:
            new_message = Message(sender=sender, content=content)
            session.add(new_message)
            session.commit()
            return new_message
        except SQLAlchemyError as e:
            logging.error(f"Error creating message: {e}")
            return None

    def get_all_messages(self):
        try:
            with self.session_manager.session_scope() as session:
                messages = session.query(Message).all()
                return messages
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving messages: {e}")
            return []

    def delete_all_messages(self):
        try:
            with self.session_manager.session_scope() as session:
                session.query(Message).delete()
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error deleting messages: {e}")

    def get_message_by_id(self, message_id):
        try:
            with self.session_manager.session_scope() as session:
                message = session.query(Message).get(message_id)
                return message
        except SQLAlchemyError as e:
            logging.error(f"Error retrieving message by ID: {e}")
            return None

    def delete_message_by_uuid(self, uuid):
        try:
            with self.session_manager.session_scope() as session:
                message = session.query(Message).filter_by(uuid=uuid).first()
                if message:
                    session.delete(message)
                    session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error deleting message by UUID: {e}")

