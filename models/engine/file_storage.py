#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base


class DBStorage:
    """This class manages storage of hbnb models in a MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, database),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Query on the current database session"""
        from models import classes
        objects = {}
        if cls:
            query = self.__session.query(classes[cls])
            for obj in query.all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query.all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current
        database session from the engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
