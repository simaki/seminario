import datetime
import re
from copy import copy

from .seminar import Seminar


class IOSeminarData:
    """
    IO
    """
    data_keys = Seminar.data_keys

    __symbols = {
        'N': 'name',
        'D': 'date',
        'B': 'begin_time',
        'E': 'end_time',
        'P': 'place',
        'S': 'speaker',
        'F': 'affiliation',
        'T': 'title',
        'A': 'abstract_file',
        'L': 'slide_file',
    }

    def __init__(self):
        pass

    def read_data(self):
        return {
            key: self.__read_value(key)
            for key in self.__class__.data_keys
        }

    def __read_value(self, key):
        if key in ('date', ):
            return self.__read_date(key)
        if key in ('begin_time', 'end_time'):
            return self.__read_time(key)
        if key in self.__class__.data_keys:
            return self.__read_else(key)

    def __read_date(self, key):
        re_date = r'\d{4}[-/]\d{2}[-/]\d{2}'
        while True:
            enter = 'date (YYYY-MM-DD)'
            i = input(f'- Enter {enter:<18} : ') or None
            if i is None:
                return None
            if re.match(re_date, i):
                y, m, d = int(i[:4]), int(i[5:7]), int(i[8:])
                try:
                    return datetime.date(y, m, d)
                except ValueError:  # eg i = '9999-99-99'
                    pass
            else:
                print('Invalid input: {i}')

    def __read_time(self, key):
        re_time = r'\d{2}:\d{2}'
        while True:
            enter = f'{key} (HH:MM)'
            i = input(f'- Enter {enter:<18} : ') or None
            if i is None:
                return None
            elif re.match(re_time, i):
                h, m = int(i[:2]), int(i[3:])
                try:
                    return datetime.time(h, m)
                except ValueError:  # eg i = '99:99'
                    pass
            else:
                print('Invalid input: {i}')

    def __read_else(self, key):
        return input(f'- Enter {key:<18} : ') or None

    def update_data(self, seminar):
        re_symbols = r'(?i)[DBEPSFTAL]$'

        data = copy(seminar.data)
        correct = False

        while not correct:
            self.__print_symbols(data)
            valid_input = False

            while not valid_input:
                i = input('- Correct?  Press Y (Yes) or key to edit: ')
                if re.fullmatch(r'(?i)[Y]$', i):
                    correct = True
                    valid_input = True
                elif re.fullmatch(re_symbols, i):
                    key = self.__class__.__symbols[i]
                    data[key] = self.__read_value(key)
                    valid_input = True
                else:
                    print('Invalid input: {}'.format(i))

        return data

    def __print_symbols(self, data):
        print(
            '\n'.join([
                f'({symbol}) {key}: {data[key]}'
                for symbol, key in self.__class__.__symbols.items()
            ])
        )

    def choose_index(self, database):
        num_show = 5
        data = database.data.copy()

        while len(data.index):
            print(data.tail(num_show))

            index = input('- Enter index : ') or None
            index = int(index) if index else None
            if index in data.index:
                return index
            data = data.iloc[:-num_show]

        return index
