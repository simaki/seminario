import unittest

import seminario

from context import (
    config,
    dict_seminar_A,
    dict_seminar_B,
    dict_seminar_C,
)

# TODO nan data


class TestIO(unittest.TestCase):

    def setUp(self):
        seminario.setup(dir_abstract=config['dir_abstract'])
        self.seminar_A = seminario.Seminar(dict_seminar_A)
        self.seminar_B = seminario.Seminar(dict_seminar_B)
        self.seminar_C = seminario.Seminar(dict_seminar_C)

    def test_read_withsetup(self):
        seminario.setup(database=config['database'])
        sdf = seminario.SeminarDataFrame.read_database()

        self.assertIsInstance(sdf, seminario.SeminarDataFrame)
        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_B)

    def test_read_withoutsetup(self):
        sdf = seminario.SeminarDataFrame.read_database(config['database'])

        self.assertIsInstance(sdf, seminario.SeminarDataFrame)
        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_B)

    def test_to_database(self):
        sdf = seminario.SeminarDataFrame.read_database(config['database'])
        sdf.to_database(database='./data/database_new.csv')
        sdf_new = seminario.SeminarDataFrame.read_database('./data/database_new.csv')

        self.assertEqual(seminario.Seminar(sdf_new.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[1, :]), self.seminar_B)

class TestAdd(unittest.TestCase):

    def setUp(self):
        seminario.setup(database=config['database'])
        self.sdf = seminario.SeminarDataFrame.read_database(config['database'])
        self.seminar_A = seminario.Seminar(dict_seminar_A)
        self.seminar_B = seminario.Seminar(dict_seminar_B)
        self.seminar_C = seminario.Seminar(dict_seminar_C)

    def test_add_inplace(self):
        sdf = self.sdf
        sdf.add(self.seminar_C, inplace=True)

        self.assertIsInstance(sdf, seminario.SeminarDataFrame)
        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_B)
        self.assertEqual(seminario.Seminar(sdf.iloc[2, :]), self.seminar_C)

    def test_add_notinplace(self):
        sdf = self.sdf
        sdf_new = sdf.add(self.seminar_C, inplace=False)

        self.assertIsInstance(sdf_new, seminario.SeminarDataFrame)
        self.assertEqual(len(sdf.index), 2)
        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_B)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[1, :]), self.seminar_B)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[2, :]), self.seminar_C)

    def test_add_fromnull(self):
        sdf_null = seminario.SeminarDataFrame()
        sdf_null.add(self.seminar_A, inplace=True)
        sdf_null.add(self.seminar_B, inplace=True)

        self.assertEqual(seminario.Seminar(sdf_null.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf_null.iloc[1, :]), self.seminar_B)

class TestEdit(unittest.TestCase):

    def setUp(self):
        seminario.setup(dir_abstract=config['dir_abstract'])
        self.sdf = seminario.SeminarDataFrame.read_database(config['database'])
        self.seminar_A = seminario.Seminar(dict_seminar_A)
        self.seminar_B = seminario.Seminar(dict_seminar_B)
        self.seminar_C = seminario.Seminar(dict_seminar_C)

    def test_edit_inplace(self):
        sdf = self.sdf
        sdf.edit(index=1, data=dict_seminar_C, inplace=True)

        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_C)

    def test_edit_notinplace(self):
        sdf = self.sdf
        sdf_new = sdf.edit(index=1, data=dict_seminar_C, inplace=False)

        self.assertEqual(seminario.Seminar(sdf.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf.iloc[1, :]), self.seminar_B)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[0, :]), self.seminar_A)
        self.assertEqual(seminario.Seminar(sdf_new.iloc[1, :]), self.seminar_C)


if __name__ == '__main__':
    unittest.main()
