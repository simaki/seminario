import re

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
    def read_csv(cls, csv, **kwargs):
        data = pd.read_csv(csv, index_col=0, **kwargs)
        data = cls.__check_data(data)
        return cls(data=data)

    def add(self, seminar):
        """Add a new seminar inplace."""
        self.__data = pd.concat([
            self.data, seminar.to_frame()
        ]).reset_index(drop=True)

    def edit(self, index, seminar):
        """Edit a seminar inplace."""
        self.__data.iloc[index] = seminar.to_series()
