from sqlalchemy import Column, String, Integer
from application.models.base import Base


class Preference(Base):
    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
    data_type = Column(String, nullable=False)