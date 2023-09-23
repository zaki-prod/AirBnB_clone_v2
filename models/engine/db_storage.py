#!/usr/bin/python3
""" New engine database storage """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage():
    """ Defines DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiation of the DBStorage class """
        MySQL_user = getenv('HBNB_MYSQL_USER')
        MySQL_pwd = getenv('HBNB_MYSQL_PWD')
        MySQL_host = getenv('HBNB_MYSQL_HOST')
        MySQL_db = getenv('HBNB_MYSQL_DB')
        MySQL_env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            MySQL_user, MySQL_pwd, MySQL_host, MySQL_db), pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if MySQL_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Shows all the class objects in the DBStorage or
        the specified class if given
        """
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            objects = []
            for c in classes:
                objects += self.__session.query(c)
        my_dict = {}
        for obj in objects:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """ Appends the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commits all the changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and creates the current database
        session from the engine """
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Closes current SQLAlchemy session, discarding unsaved changes and
        updating `storage` with current state of DB.
        """
        self.__session.close()
