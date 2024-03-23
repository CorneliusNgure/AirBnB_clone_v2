#!/usr/bin/python3

"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:

    """This class manages storage of hbnb models in JSON format"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is provided, returns a dictionary containing
        only objects of the specified class.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            return {key: obj for key, obj in FileStorage.__objects.items() if isinstance(obj, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key, val in FileStorage.__objects.items():
            temp[key] = val.to_dict()

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }

        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    class_name = val['__class__']
                    obj = classes[class_name](**val)
                    FileStorage.__objects[key] = obj

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        If obj is None, the method does nothing.
        """
        if obj is None:
            return

        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
