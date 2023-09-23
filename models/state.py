#!/usr/bin/python3
""" State Module for HBNB project """
from .base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .city import City
from os import getenv


class State(BaseModel, Base):
    """ State class 

    Attr:
        name: name of state
        cities: one-to-many-association to City
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan",
                          backref="state")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """ Getter for list of all `City` objects when in file storage
            mode.
            """
            from module import storage
            cities = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
