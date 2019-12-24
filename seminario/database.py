from datetime.datetime import strptime
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
        # Convert date, time to datetime objects
        data['date'] = data['date'].map(cls.__to_date)
        data['begin_time'] = data['begin_time'].map(cls.__to_time)
        data['end_time'] = data['end_time'].map(cls.__to_time)
        # np.nan -> None
        return data

    @staticmethod
    def __to_date(date):
        if not date:  # empty
            return None
        if not re.fullmatch(r'\d\d\d\d[-/]\d\d[-/]\d\d'):
            raise ValueError('Invalid date value: {date}')
        try:
            return strptime(date, '%Y-%m-%d')
        except ValueError:
            pass
        try:
            return strptime(date, '%Y/%m/%d')
        except ValueError:
            return None

    @staticmethod
    def __to_time(time):
        if not time:  # empty
            return None
        if not re.fullmatch(r'\d\d:\d\d'):
            raise ValueError('Invalid time value: {time}')
        try:
            return strptime(time, '%H:%M')
        except ValueError:
            return None

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
