import os
from pathlib import Path
from typing import Union, Optional

from .utils import Bunch
from datetime.datatime import strptime
import pandas as pd


class Seminar(Bunch):
    """
    Represent a seminar.

    Attribures
    ----------
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
    __dir_abstract = Path('./data/abstract/')
    # data_keys = (
    #     'name',
    #     'date',
    #     'begin_time',
    #     'end_time',
    #     'place',
    #     'speaker',
    #     'affiliation',
    #     'title',
    #     'abstract_file',
    #     'slide_file',
    # )
    def __init__(self, *kwargs):
        super().__init__(**kwargs)
        # self = self._check_data()  # not necessary

    def __check_data(self, data):
        self = self._check_keys()
        self = self._parse_date()
        self = self._parse_time()

    def _check_keys(self):
        """
        Check there is no invalid keys and fill absent key with None.

        Returns
        -------
        self : Seminar
            Seminar that has only and all valid keys.
        """
        # Check there is no invalid key
        for key in self.keys():
            if key not in self._valid_keys:
                raise ValueError(f'Data has an invalid key: {key}')

        # Fill absent value with None
        for key in self._valid_keys:
            if not hasattr(self, key):
                setattr(self, key, None)

        return self

    # def _parse_date(self):
    #     if self.date is None:
    #         return self

    #     if isinstance(self.date, datetime.date):
    #         return self

    #     try:
    #         self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    #     except ValueError:
    #         self.date = datetime.datetime.strptime(date, '%Y/%m/%d').date()

    #     return self

    # def _parse_time(self):
    #     if self.begin_time is None and self.end_time is None:
    #         return self

    #     for time in ('begin_time', 'end_time'):
    #         attr = getattr(self, time)
    #         if attr is not None:
    #             if isinstance(attr, datetime.date):
    #                 setattr(self, time, attr)
    #             else:
    #                 setattr(self, time, strptime(time, '%H:%M').time())
    #     return self


    #     if isinstance(time, datetime.time):
    #         return time
    #     return datetime.datetime.strptime(time, '%H:%M').time() \
    #         if time else None

    # @staticmethod
    # def __to_file(file):
    #     return pathlib.Path(file) if file else None

    # @staticmethod
    # def __to_other(value):
    #     return str(value) if value else None

    @property
    def abstract(self):
        """
        Return abstract sentences of self.

        Returns
        -------
        abstract : str
        """
        return self.__read_abstract()

    def __read_abstract(self):
        if self.abstract_file is None:
            return ''

        path = self.dir_abstract / self.abstract_file

        if not path.exists():
            raise FileNotFoundError(f'abstract_file {path} does not exist.')

        with open(path) as f:
            return f.read()

    def edit(self, data={}):
        """
        Edit self inplace.

        Parameters
        ----------
        - data : dict
            New data of the seminar.
        """
        for key, value in data.items():
            setattr(self, key, value)

    # def to_series(self):
    #     """
    #     Return self as ``pandas.Series``.

    #     Returns
    #     -------
    #     pandas.Series
    #     """
    #     return pd.Series(self.data)

    # def to_frame(self):
    #     """
    #     Return self as ``pandas.DataFrame`` with a single index.

    #     Returns
    #     -------
    #     pandas.DataFrame
    #     """
    #     return pd.DataFrame([self.to_series()], index=[0])
