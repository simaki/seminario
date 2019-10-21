import datetime
import os
import re

import pandas as pd
import pdfkit

from seminario.config import _Config
from seminario._io import _read_item, _read_data, _edit_data


class Seminar():
    """
    Represent a seminar.

    Paramteres
    ----------
    - date : datetime.date
        Date of the seminar.
    - begin_time : datetime.time
        Beginnig time of the seminar.
    - end_time : datetime.time
        End time of the seminar.
    - place : str
        Place of the seminar.
    - speaker : str
        Name of the speaker.
    - affiliation : str
        Affiliation of the speaker.
    - title : str
        Title of the seminar talk.
    - abstract_file : str
        Relative path of the abstract file to ``_Config.dir_abstract``.
    - slide_file : str
        Relative path of the slide file to ``_Config.dir_slide``.
    - abstract : str
        Abstract sentences.
        It is automatically read if ``self.abstract_file`` is not None.
    """
    def __init__(
        self,
        data=None,
        interactive=False,
        date=None,
        begin_time=None,
        end_time=None,
        place=None,
        speaker=None,
        affiliation=None,
        title=None,
        abstract_file=None,
        slide_file=None
    ):
        """
        Initialize self.

        Examples
        --------

        >>> seminar = seminario.Seminar(
        ...         date            = datetime.date(2019, 1, 1),
        ...         begin_time      = datetime.time(12, 0),
        ...         end_time        = datetime.time(13, 0),
        ...         place           = '101A'
        ...         speaker         = 'Alice Speaker',
        ...         affiliation     = 'Alabama University',
        ...         title           = 'Apple Effect',
        ...         abstract_file   = 'alice.txt'
        ...         slide_file      = 'alice.pdf'
        ... )
        >>> type(seminar)
        <class 'seminario.Seminar'>
        >>> seminar
        - date          : 2019-01-01
        - begin time    : 12:00
        - end_time      : 13:00
        - place         : 101A
        - speaker       : Alice Speaker
        - affiliation   : Alabama University
        - title         : Apple Effect
        - abstract file : alice.txt
        - slide file    : alice.pdf

        The following example initializes the same ``Seminar`` from ``dict``.

        >>> data = {
        ...     'date':             datetime.date(2019, 1, 1),
        ...     'begin time':       datetime.time(12, 0),
        ...     'end time':         datetime.time(13, 0),
        ...     'place':            '101A',
        ...     'speaker':          'Alice Speaker',
        ...     'affiliation':      'Alabama University',
        ...     'title':            'Apple Effect',
        ...     'abstract file':    'alice.txt'
        ...     'slide file':       'alice.pdf'
        ... }
        >>> seminar = seminario.Seminar(data=data)
        """
        if interactive:
            self.__init__(data=_read_data())
            self.edit(interactive=True)  # confirm
        elif data is None:
            self.date = date
            self.begin_time = begin_time
            self.end_time = end_time
            self.place = place
            self.speaker = speaker
            self.affiliation = affiliation
            self.title = title
            self.abstract_file = abstract_file
            self.slide_file = slide_file
        elif isinstance(data, dict):
            self.__init__(
                data=None,
                date=data.get('date'),
                begin_time=data.get('begin time'),
                end_time=data.get('end time'),
                place=data.get('place'),
                speaker=data.get('speaker'),
                affiliation=data.get('affiliation'),
                title=data.get('title'),
                abstract_file=data.get('abstract file'),
                slide_file=data.get('slide file'),
            )
        elif isinstance(data, pd.Series):
            self.__init__(
                data=None,
                date=data['date'],
                begin_time=data['begin time'],
                end_time=data['end time'],
                place=data['place'],
                speaker=data['speaker'],
                affiliation=data['affiliation'],
                title=data['title'],
                abstract_file=data['abstract file'],
                slide_file=data['slide file'],
            )
        else:
            raise TypeError('Invalid type of data: ', type(data))

    @property
    def abstract(self):
        """Return abstract sentences of self."""
        if self.abstract_file is None:
            return None
        try:
            path = _Config.dir_abstract / self.abstract_file
            with open(path) as f:
                abstract = f.read()
        except FileNotFoundError as e:
            print(e)
            return None
        else:
            return abstract

    @property
    def _dict(self):
        """Return ``dict`` of parameters."""
        return {
            'date':             self.date,
            'begin time':       self.begin_time,
            'end time':         self.end_time,
            'place':            self.place,
            'speaker':          self.speaker,
            'affiliation':      self.affiliation,
            'title':            self.title,
            'abstract file':    self.abstract_file,
            'slide file':       self.slide_file,
        }

    def __str__(self):
        return '\n'.join([
            '- {} : {}'.format(key.ljust(13), value)
            for key, value in self._dict.items()
        ])

    def __eq__(self, other):
        for key, value in self._dict.items():
            if value != getattr(other, key.replace(' ', '_')):
                return False
        return True

    def _update_inplace(self, data):
        """
        Parameters
        ----------
        - data : Seminar
            New data of seminar.
        """
        for key, value in data._dict.items():
            k = key.replace(' ', '_')
            v = value or getattr(self, k)
            setattr(self, k, v)

    def edit(
        self,
        data: dict = {},
        interactive=False,
        inplace=False,
    ):
        """
        Edit ``self`` inplace.

        Parameters
        ----------
        - data : dict
            New information of the seminar.
        - interactive : bool, default False
            If True, edit interactively.
        - inplace : bool, default False
            If True, edit inplace.
        """
        if interactive:
            result = Seminar(data=_edit_data(self._dict))
        else:
            result = Seminar(data=data)

        if inplace:
            self._update_inplace(result)
        else:
            return result

    def to_Series(self):
        """
        Return self as ``pandas.Series``.

        Returns
        -------
        pandas.Series

        Example
        -------

        >>> seminar
        date          : 2019-01-01
        begin time    : 12:00
        end time      : 13:00
        place         : 101A
        speaker       : Alice Speaker
        title         : Apple Effect
        abstract file : alice.txt
        slide file    : alice.pdf
        >>> seminar.to_SeminarDataFrame()
                date begin time end time place        speaker ...
        0 2019-01-01      12:00    13:00  101A  Alice Speaker ...
                 title abstract file slide file
        0 Apple Effect     alice.txt  alice.pdf
        """
        return pd.Series(data=self._dict)

    def to_DataFrame(self):
        """
        Return self as ``pandas.DataFrame`` with a single index.

        Returns
        -------
        pandas.DataFrame
        """
        return pd.DataFrame([self.to_Series()], index=[0])

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
            'datetime_and_place': (
                '<p class="datetime_and_place">'
                '{}, at {}'
                '</p>'.format(date_time, place)
            ),
            'title': (
                '<p class="title">'
                '{}'
                '</p>'.format(title)
            ),
            'speaker_and_affiliation': (
                '<p class="speaker_and_affiliation">'
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
                   p['datetime_and_place'],
                   p['title'],
                   p['speaker_and_affiliation'],
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
