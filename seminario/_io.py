import datetime
import re


_ticker_item = {
    'D': 'date',
    'B': 'begin time',
    'E': 'end time',
    'P': 'place',
    'S': 'speaker',
    'F': 'affiliation',
    'T': 'title',
    'A': 'abstract file',
    'L': 'slide file',
}
_list_ticker = _ticker_item.keys()
_list_item = _ticker_item.values()
_re_ticker = r'(?i)[DBEPSFTAL]$'


def _print_ticker(data: dict):
    """
    Print seminar data with tickers.
    """
    print('\n'.join([
        '({}) {:<13} : {}'.format(ticker, item, data[item])
        for ticker, item in _ticker_item.items()
    ]))


def _read_item(item: str):
    """
    Read standard input of ``item`` and return it.
    If not entered, return ``None``.

    Parameters
    ----------
    - item : {'date', 'begin time', ...}
        Item to read.

    Returns
    -------
    datetime.date, datetime.time or str
        Value of ``item``.
    """

    re_date = r'\d{4}[-/]\d{2}[-/]\d{2}'
    re_time = r'\d{2}:\d{2}'

    def _read_date():
        while True:
            i = input('- Enter {:<18} : '.format('date (YYYY-MM-DD)')) or None
            if i is None:
                return None
            elif re.match(re_date, i):
                y, m, d = int(i[:4]), int(i[5:7]), int(i[8:])
                try:
                    date = datetime.date(y, m, d)
                except ValueError:  # eg i = '9999-99-99'
                    pass
                else:
                    return date
            else:
                print('Invalid input: {}'.format(i))

    def _read_time(item):
        while True:
            i = input('- Enter {:<18} : '.format(item + ' (HH:MM)')) or None
            if i is None:
                return None
            elif re.match(re_time, i):
                h, m = int(i[:2]), int(i[3:])
                try:
                    time = datetime.time(h, m)
                except ValueError:  # eg i = '99:99'
                    pass
                else:
                    return time
            else:
                print('Invalid input: {} '.format(i))

    def _read_else(item):
        return input('- Enter {:<18} : '.format(item)) or None

    if item in ('date'):
        return _read_date()
    elif item in ('begin time', 'end time'):
        return _read_time(item)
    elif item in _list_item:
        return _read_else(item)
    else:
        raise ValueError('Invalid item: ', item)


def _read_data():
    """
    Read seminar data from standard input.

    Returns
    -------
    dict
        Data of a seminar.
    """
    return {item: _read_item(item) for item in _list_item}


def _edit_data(data: dict):
    """
    Edit seminar data interactively.

    Parameters
    ----------
    - data : dict
        Old data of a seminar.

    Returns
    -------
    dict
        New data of a seminar.
    """
    new_data = data
    correct = False
    while not correct:
        _print_ticker(new_data)
        valid_input = False
        while not valid_input:
            i = input('- Correct? Press Y or key for item to edit: ')
            if re.match(r'(?i)[Y]$', i):
                correct = True
                valid_input = True
            elif re.match(_re_ticker, i):
                item = _ticker_item[i.upper()]
                new_data[item] = _read_item(item)
                valid_input = True
            else:
                print('Invalid input: {}'.format(i))
    return new_data
