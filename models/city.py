#!/usr/bin/python3
""" Defines city. """
from sqlalchemy import Column, String
from sqlalchemy.schema import ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Defines city class.
    Attributes:
        name (Column): name of state, string of max 128 chars
        state_id (Column): string of max 60 chars, foreign key to `states.id`
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship('Place', backref='cities',
                          cascade='all, delete-orphan')
