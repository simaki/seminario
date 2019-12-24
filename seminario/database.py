import pandas as pd

from .seminar import Seminar


class Database:

    data_keys = Seminar.data_keys

    def __init__(self, data=None):
        self.__data = data

    @property
    def data(self):
        return self.__data

    @classmethod
    def __check_data(cls, data):
        # Check columns
        if not set(data.columns) == cls.data_keys:
            raise ValueError('Invalid columns')
        return data

    @classmethod
    def read_csv(cls, path, **kwargs):
        data = pd.read_csv(path, index_col=0, **kwargs)
        data = cls.__check_data(data)
        return cls(data=data)

    def to_csv(self, path):
        self.data.to_csv(path)

    def add(self, seminar):
        """Add a new seminar inplace."""
        self.__data = pd.concat([
            self.data, seminar.to_frame()
        ]).reset_index(drop=True)

    def edit(self, index, seminar):
        """Edit a seminar inplace."""
        self.__data.iloc[index] = seminar.to_series()
