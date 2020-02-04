from abc import abstractmethod, ABCMeta

from .bunch import Bunch


class Table(Bunch, metaclass=ABCMeta):
    """
    Bunch object that is allowed to have only limited attributes.
    """
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise AttributeError(key)
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def attributes(self):
        """
        Attributes that self is allowed to have.
        """

    def __setattr__(self, key, value):
        if key not in self.attributes:
            raise AttributeError(key)
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            if key in self.attributes:
                return None
            raise AttributeError(key)
