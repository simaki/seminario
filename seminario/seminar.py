import os
import pathlib
from typing import Union, Optional

import datetime
import pandas as pd


PathLike = Optional[Union[str, os.PathLike]]


class Seminar():
    """
    Represent a seminar.

    Paramteres
    ----------
    - data : dict
        The data of the seminar.
        - name : str
        - date : datetime.date
        - begin_time : datetime.time
        - end_time : datetime.time
        - place : str
        - speaker : str
        - affiliation : str
        - title : str
        - abstract_file : pathlib.PosixPath
        - slide_file : pathlib.PosixPath
    """
    data_keys = (
        'name',
        'date',
        'begin_time',
        'end_time',
        'place',
        'speaker',
        'affiliation',
        'title',
        'abstract_file',
        'slide_file',
    )

    def __init__(self, data, dir_abstract='./data/abstract/'):
        data = self.__class__.__typing_data(data)
        self.__data = data
        self.dir_abstract = pathlib.Path(dir_abstract)

    @staticmethod
    def __to_date(date):
        if not date:  # empty
            return None
        if isinstance(date, datetime.date):
            return date
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return datetime.datetime.strptime(date, '%Y/%m/%d').date()

    @staticmethod
    def __to_time(time):
        if isinstance(time, datetime.time):
            return time
        return datetime.datetime.strptime(time, '%H:%M').time() \
            if time else None

    @staticmethod
    def __to_file(file):
        return pathlib.Path(file) if file else None

    @staticmethod
    def __to_other(value):
        return str(value) if value else None

    @classmethod
    def __typing_data(cls, data):
        if not isinstance(data, dict):
            raise TypeError('data must be dict.')

        # Check and convert typing
        for key, value in data.items():
            if key in ('date', ):
                data[key] = cls.__to_date(value)
            elif key in ('begin_time', 'end_time', ):
                data[key] = cls.__to_time(value)
            elif key in ('abstract_file', 'slide_file', ):
                data[key] = cls.__to_file(value)
            elif key in cls.data_keys:
                data[key] = cls.__to_other(value)
            else:
                raise ValueError(f'Invalid key: {key}')

        # Fill missing key with None
        for key in cls.data_keys:
            data[key] = data.get(key, None)

        return data

    @property
    def data(self):
        """Return data of self."""
        return self.__data

    @property
    def abstract(self):
        """Return abstract sentences of self."""
        if self.data['abstract_file'] is None:
            return None
        path = self.dir_abstract / self.data['abstract_file']
        if not path.exists():
            raise FileNotFoundError(f'abstract_file {path} does not exist.')
        with open(path) as f:
            return f.read()

    def __str__(self):
        pass  # TODO

    def edit(self, data={}):
        """
        Edit self inplace.

        Parameters
        ----------
        - data : dict
            New data of the seminar.
        """
        for key, value in data.items():
            self.__data[key] = value

    def to_series(self):
        """
        Return self as ``pandas.Series``.

        Returns
        -------
        pandas.Series
        """
        return pd.Series(self.data)

    def to_frame(self):
        """
        Return self as ``pandas.DataFrame`` with a single index.

        Returns
        -------
        pandas.DataFrame
        """
        return pd.DataFrame([self.to_series()], index=[0])
