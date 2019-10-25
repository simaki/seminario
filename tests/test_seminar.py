import unittest

import pandas as pd
import seminario

from context import (
    dict_seminar_A,
    dict_seminar_B,
    dict_seminar_n,
)

seminario.setup(
    dir_abstract='./data/abstract/',
    dir_poster='./data/poster/',
)


def assertEqual_seminar(self, seminar, dict_expected):
    pairs_items = [
        (value, dict_expected[key.replace('_', ' ')])
        for key, value in seminar.__dict__.items()
        if key != '_abstract'
    ]
    for value, value_expected in pairs_items:
        self.assertEqual(value, value_expected)


class TestSeminarInit(unittest.TestCase):

    def setUp(self):
        self.items_A = {k: v for k, v in dict_seminar_A.items() if k != 'abstract'}
        self.abstract_A = dict_seminar_A['abstract']

    def test_init_direct(self):
        seminar_A = seminario.Seminar(
            date            = dict_seminar_A['date'],
            begin_time      = dict_seminar_A['begin time'],
            end_time        = dict_seminar_A['end time'],
            place           = dict_seminar_A['place'],
            speaker         = dict_seminar_A['speaker'],
            affiliation     = dict_seminar_A['affiliation'],
            title           = dict_seminar_A['title'],
            abstract_file   = dict_seminar_A['abstract file'],
            slide_file      = dict_seminar_A['slide file'],
        )

        self.assertIsInstance(seminar_A, seminario.Seminar)
        self.assertEqual(seminar_A._dict, self.items_A)
        self.assertEqual(seminar_A.abstract, self.abstract_A)

    def test_init_dict(self):
        seminar_A = seminario.Seminar(data=dict_seminar_A)

        self.assertEqual(seminar_A._dict, self.items_A)
        self.assertEqual(seminar_A.abstract, self.abstract_A)

    def test_init_Series(self):
        series_A = pd.Series(self.items_A)
        seminar_A = seminario.Seminar(data=series_A)

        self.assertEqual(seminar_A._dict, self.items_A)
        self.assertEqual(seminar_A.abstract, self.abstract_A)


class TestSeminarEdit(unittest.TestCase):

    def setUp(self):
        self.seminar_A = seminario.Seminar(dict_seminar_A)
        self.seminar_B = seminario.Seminar(dict_seminar_B)

    def test_edit_notinplace(self):
        seminar_A_old = self.seminar_A
        seminar_A_new = seminar_A_old.edit(data=dict_seminar_B, inplace=False)

        self.assertEqual(seminar_A_old, self.seminar_A)
        self.assertEqual(seminar_A_new, self.seminar_B)

    def test_edit_inplace(self):
        seminar_A = self.seminar_A
        seminar_A.edit(data=dict_seminar_B, inplace=True)

        self.assertEqual(seminar_A, self.seminar_B)

    def test_edit_none(self):
        seminar_A = self.seminar_A
        seminar_A.edit(data=dict_seminar_n, inplace=True)

        self.assertEqual(seminar_A, self.seminar_A)


class TestSeminarConvert(unittest.TestCase):

    def setUp(self):
        self.seminar_A = seminario.Seminar(dict_seminar_A)

    def test_to_series(self):
        series_A = self.seminar_A.to_Series()

        self.assertIsInstance(series_A, pd.core.series.Series)
        self.assertEqual(dict(series_A), self.seminar_A._dict)

    def test_to_dataframe(self):
        dataframe_A = self.seminar_A.to_DataFrame()

        self.assertIsInstance(dataframe_A, pd.core.frame.DataFrame)
        self.assertEqual(dict(dataframe_A.iloc[0, :]), self.seminar_A._dict)


if __name__ == '__main__':
    unittest.main()
