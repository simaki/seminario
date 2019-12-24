import os
from typing import Union

import pandas as pd
import pdfkit

from seminario.config import _Config
from seminario._io import _read_data, _edit_data


Pathlike = Optional[Union[str, os.PathLike]]


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
        - abstract_file : str
        - slide_file : str
    """
    __data_key = (
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
    def __init__(self, data=None):
        data = self.__class__.__check_data(data)
        self.__data = data

    @classmethod
    def __check_data(cls, data):
        if isinstance(data, dict):
            raise TypeError('Parameter "data" must be dict.')
        # Check typing
        for key, value in data.items():
            if key in ('date', ):
                if not isinstance(value, Optional[datetime.date]):
                    raise TypeError(f'{key} must be datetime.date or None.')
            if key in ('begin_time', 'end_time', ):
                if not isinstance(value, Optional[datetime.time]):
                    raise TypeError(f'{key} must be datetime.time or None.')
            if key in ('abstract_file', 'slide_file', ):
                if not isinstance(value, PathLike):
                    raise TypeError(f'{key} must be path-like or None.')
            if key in cls.__data_keys:
                if not isinstance(value, Optional[str]):
                    raise TypeError(f'{key} must be str or None.')
            raise ValueError(f'Invalid key: {key}')
        # Fill missing key with None
        for key in cls.__data_keys:
            data[key] = data.get(key, None)
        return data

    @property
    def data(self):
        return self.__data

    @property
    def abstract(self):
        """Return abstract sentences of self."""
        if self.data['abstract_file'] is None:
            return None
        path = _Config.dir_abstract / self.data['abstract_file']
        if not path.exists():
            raise FileNotFoundError(f'abstract_file {path} does not exist.')
        with open(path) as f:
            return f.read()

    def __str__(self):
        pass

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

    def as_series(self):
        """
        Return self as ``pandas.Series``.

        Returns
        -------
        pandas.Series
        """
        return pd.Series(self.data)

    def as_frame(self):
        """
        Return self as ``pandas.DataFrame`` with a single index.

        Returns
        -------
        pandas.DataFrame
        """
        return pd.DataFrame([self.as_series()], index=[0])
