from sqlalchemy import Column, Integer, String, Sequence
import uuid

from application.database.database_manager import DatabaseManager
from application.models.base import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    uuid = Column(String, unique=True)
    sender = Column(String)
    content = Column(String)

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.generate_unique_uuid()

    def generate_unique_uuid(self):
        self.uuid = str(uuid.uuid4())

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'sender': self.sender,
            'content': self.content
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(sender=json_data.get('sender'), content=json_data.get('content'))
