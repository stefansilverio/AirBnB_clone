#!/usr/bin/python3
"""base class for project"""
from datetime import datetime
import uuid


class BaseModel:
    """creates BaseModel class for project"""

    def __init__(self, *args, **kwargs):
        """Initialize instance variables"""
        from models import storage
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) == 0:
            storage.new(self)
        else:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k in ['created_at', 'updated_at']:
                        if type(v) == str:
                            v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                        else:
                            if k == 'created_at':
                                v = self.created_at
                            elif k == 'updated_at':
                                v = self.updated_at
                    if k == 'id':
                        v = str(v)
                    setattr(self, k, v)
                if k == 'id':
                    existing = storage.all()
                    id_str = self.__class__.__name__ + '.' + str(v)
                    if id_str not in existing.keys():
                        storage.new(self)

    def __str__(self):
        """Define print() and str() output"""
        return '[{:s}] ({:s}) {:s}'.format(
                self.__class__.__name__, self.id, str(self.__dict__))

    def save(self):
        """Update updated_at and call storage.save()"""
        from models import storage
        self.updated_at = datetime.today()
        storage.save()

    def to_dict(self):
        """Update and return dictionary of instance"""
        new_dict = {k: v for k, v in self.__dict__.items()}
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
