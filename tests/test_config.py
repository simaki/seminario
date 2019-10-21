import unittest

import pathlib

import seminario
from seminario.config import _Config


from context import (
    config,
    absent,
)


class TestConfig(unittest.TestCase):

    def test_config(self):
        seminario.setup(
            name            = config['name'],
            database        = config['database'],
            poster_css      = config['poster_css'],
            dir_abstract    = config['dir_abstract'],
            dir_slide       = config['dir_slide'],
            dir_poster      = config['dir_poster'],
            tba_date        = config['tba_date'],
            tba_begin_time  = config['tba_begin_time'],
            tba_end_time    = config['tba_end_time'],
            tba_place       = config['tba_place'],
            tba_speaker     = config['tba_speaker'],
            tba_affiliation = config['tba_affiliation'],
            tba_title       = config['tba_title'],
            tba_abstract    = config['tba_abstract'],
        )

        for k in ['database', 'poster_css', 'dir_abstract', 'dir_slide', 'dir_poster']:
            config[k] = pathlib.Path(config[k])

        items = [
            (getattr(_Config, item), config[item])
            for item in _Config._items()
        ]
        for item, item_expected in items:
            self.assertEqual(item, item_expected)

    def test_filenotfounderror(self):
        with self.assertRaises(FileNotFoundError):
            seminario.setup(database=absent['database'])
        with self.assertRaises(FileNotFoundError):
            seminario.setup(poster_css=absent['poster_css'])
        with self.assertRaises(FileNotFoundError):
            seminario.setup(dir_abstract=absent['dir_abstract'])
        with self.assertRaises(FileNotFoundError):
            seminario.setup(dir_slide=absent['dir_slide'])
        with self.assertRaises(FileNotFoundError):
            seminario.setup(dir_poster=absent['dir_poster'])


if __name__ == '__main__':
    unittest.main()
