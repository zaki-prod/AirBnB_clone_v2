#!/usr/bin/python3
""" Determines storage depending on the condition.
"""
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
