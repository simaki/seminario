import unittest

import pandas as pd
import seminario
from seminario._io import(
    _print_ticker,
    _read_data,
    _edit_data,
)

from context import(
    config,
    dict_seminar_A,
)


class TestIO(unittest.TestCase):

    def test_print_ticker(self):
        _print_ticker(dict_seminar_A)

    def test_read_data(self):
        print(_read_data())

    def test_edit_data(self):
        d = _edit_data(dict_seminar_A)
        print(d)

    def test_choose_index(self):
        sdf = seminario.SeminarDataFrame.read_database(config['database'])
        sdf = pd.concat([sdf] * 10, ignore_index=True)
        i = sdf._choose_index()
        print(i)

if __name__ == '__main__':
    # TestIO().test_print_ticker()
    # TestIO().test_read_data()
    # TestIO().test_edit_data()
    # TestIO().test_choose_index()
    unittest.main()
