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

    def _to_html(self, css):
        """
        Return html of the seminar poster of self.

        Parameters
        ----------
        - css : str, path object or file-like object
            Path of the css file. If None, ``_Config.poster_css``.

        Returns
        -------
        str
        """
        if self.date is not None:
            date = self.date.strftime('%Y %b %d (%a)')
        else:
            date = _Config.tba_date or ''
        if self.begin_time is not None:
            begin_time = self.begin_time.strftime('%H:%M')
        else:
            begin_time = _Config.tba_begin_time or ''
        if self.end_time is not None:
            end_time = self.end_time.strftime('%H:%M')
        else:
            end_time = _Config.tba_end_time or ''
        place = self.place or _Config.tba_place or ''
        speaker = self.speaker or _Config.tba_speaker or ''
        affiliation = self.affiliation or _Config.tba_affiliation or ''
        title = self.title or _Config.tba_title or ''
        abstract = self.abstract or _Config.tba_abstract or ''
        css = css or _Config.poster_css or None

        if self.begin_time is None and self.end_time is None:
            date_time = date
        else:
            time = '{} - {}'.format(begin_time, end_time)
            date_time = '{} {}'.format(date, time)

        if self.affiliation is None:
            speaker_and_affiliation = speaker
        else:
            speaker_and_affiliation = '{} ({})'.format(speaker, affiliation)

        p = {
            'name': (
                '<p class="name">'
                '{}'
                '</p>'.format(_Config.name)
            ),
            'datetime_place': (
                '<p class="datetime_place">'
                '{}, at {}'
                '</p>'.format(date_time, place)
            ),
            'title': (
                '<p class="title">'
                '{}'
                '</p>'.format(title)
            ),
            'speaker': (
                '<p class="speaker">'
                'by {}'
                '</p>'.format(speaker_and_affiliation)
            ),
            'abstract': (
                '<p class="abstract">'
                'Abstract: {}'
                '</p>'.format(abstract.replace('\n', '<br>'))
            ),
        }

        html = '''
            <!DOCTYPE html><html>
            <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{}">
            </head>
            <body>
            <div id="contents">{}{}{}{}{}</div>
            </body>
            </html>
        '''.format(css,
                   p['name'],
                   p['datetime_place'],
                   p['title'],
                   p['speaker'],
                   p['abstract'],
                   )
        return html

    def make_poster(
        self,
        path=None,
        css=None
    ):
        """
        Make a poster of self.

        Parameters
        ----------
        - path : str, path object or file-like object
            Path of the output poster.
            If None, the directory is ``_Config.dir_poster`` and
            the filename is ``YYYYMMDD.pdf`` (if date is not None) or
            ``poster.pdf`` (if date is None).
        - css : str, path object or file-like object
            Path of the css file. If None, ``_Config.poster_css``.
        """
        if path is None:
            if self.date is None:
                path = _Config.dir_poster / 'poster.pdf'
            else:
                yyyymmdd = self.date.strftime('%Y%m%d')
                path = _Config.dir_poster / (yyyymmdd + '.pdf')

        css = css or _Config.poster_css or None
        if css is None:
            raise ValueError('css file is neither set nor specified.')
        if not os.path.exists(css):
            raise FileNotFoundError('css file not found: ' + css)

        tmp = 'tmp.html'
        with open(tmp, 'w', encoding='utf-8') as h:
            h.write(self._to_html(css=css))
        pdfkit.from_file(tmp, path)
        os.remove(tmp)
