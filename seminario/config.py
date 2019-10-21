import os
import pathlib


def setup(**kwargs):
    """
    Setup configurations.

    Parameters
    ----------
    - database : str
        Path of the seminar database.
    - poster_css : str
        Path of the poster css.
    - dir_abstract : str
    - dir_slide : str
    - dir_poster : str
        Directories to save abstracts, slides and posters.
    - tba_date : str
    - tba_begin_time : str
    - tba_end_time : str
    - tba_place : str
    - tba_speaker : str
    - tba_affiliation : str
    - tba_title : str
    - tba_abstract : str
        Default values to show on posters if these are not given.
    """
    _Config.setup(**kwargs)


class _Config():

    name = 'Seminar'
    database = None
    poster_css = None

    dir_abstract = pathlib.Path('./')
    dir_slide = pathlib.Path('./')
    dir_poster = pathlib.Path('./')

    tba_date = 'TBA'
    tba_begin_time = None
    tba_end_time = None
    tba_place = 'TBA'
    tba_speaker = 'TBA'
    tba_affiliation = None
    tba_title = 'TBA'
    tba_abstract = 'TBA'

    @staticmethod
    def check_path_exist(name, path):
        if not os.path.exists(path):
            raise FileNotFoundError((
                '{} does not exist: {}'.format(name.capitalize(), path)
            ))

    @classmethod
    def _items(cls):
        return [
            'name',
            'database',
            'poster_css',
            'dir_abstract',
            'dir_poster',
            'dir_slide',
            'tba_date',
            'tba_begin_time',
            'tba_end_time',
            'tba_place',
            'tba_speaker',
            'tba_affiliation',
            'tba_title',
            'tba_abstract',
        ]

    @classmethod
    def setup(
        cls,
        name=None,
        database=None,
        poster_css=None,
        dir_abstract=None,
        dir_slide=None,
        dir_poster=None,
        tba_date=None,
        tba_begin_time=None,
        tba_end_time=None,
        tba_place=None,
        tba_speaker=None,
        tba_affiliation=None,
        tba_title=None,
        tba_abstract=None,
    ):
        paths = {
            'database': database,
            'poster css': poster_css,
            'abstract directory': dir_abstract,
            'slide directory': dir_slide,
            'poster directory': dir_poster,
        }
        for key, path in paths.items():
            if path is not None:
                _Config.check_path_exist(key, path)

        def _to_path(s):
            if s is None:
                return None
            else:
                return pathlib.Path(s)

        cls.name = name or cls.name
        cls.database = _to_path(database) or cls.database
        cls.poster_css = _to_path(poster_css) or cls.poster_css

        cls.dir_abstract = _to_path(dir_abstract) or cls.dir_abstract
        cls.dir_slide = _to_path(dir_slide) or cls.dir_slide
        cls.dir_poster = _to_path(dir_poster) or cls.dir_poster

        cls.tba_date = tba_date or cls.tba_date
        cls.tba_begin_time = tba_begin_time or cls.tba_begin_time
        cls.tba_end_time = tba_end_time or cls.tba_end_time
        cls.tba_place = tba_place or cls.tba_place
        cls.tba_speaker = tba_speaker or cls.tba_speaker
        cls.tba_affiliation = tba_affiliation or cls.tba_affiliation
        cls.tba_title = tba_title or cls.tba_title
        cls.tba_abstract = tba_abstract or cls.tba_abstract
