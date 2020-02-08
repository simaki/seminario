import os
from pathlib import Path

import pdfkit

from pandas import Timestamp
from .config import config


class PosterMaker:
    """
    Generate poster.

    Parameters
    ----------
    - css : path-like, default None
        Path of poster css.
        If None, use `config.path.css`.
    - tba : dict
        Default values.
        If None, use `config.tba`.
    """
    def __init__(self, css=None, tba=None):
        self.css = css or config.path.css
        self.tba = tba or config.tba

    def make_poster(self, seminar, path='poster.pdf'):
        """
        Make a poster.

        Parameters
        ----------
        - seminar : Seminar
            Seminar to make a poster.
        - path : path-like, default 'poster.pdf'
            Path to make a poster.

        Returns
        -------
        None
        """
        tmp = 'tmp.html'
        with open(tmp, 'w') as f:
            f.write(self._to_html(seminar))
        pdfkit.from_file(tmp, path)
        os.remove(tmp)

    def _to_html(self, seminar):
        """
        Return html of a seminar poster.

        Parameters
        ----------
        - seminar : Seminar
            Seminar to make a poster html.

        Returns
        -------
        html : str
        """
        self._check_css()

        seminar_name = self._get_seminar_name(seminar)
        date_time = self._get_date_time(seminar)
        place = self._get_place(seminar)
        title = self._get_title(seminar)
        speaker_affiliation = self._get_speaker_affiliation(seminar)
        abstract = self._get_abstract(seminar)

        p = {
            'name': (
                '<p class="name">'
                f'{seminar_name}'
                '</p>'
            ),
            'date_time_place': (
                '<p class="date_time_place">'
                f'{date_time}, at {place}'
                '</p>'
            ),
            'title': (
                '<p class="title">'
                f'{title}'
                '</p>'
            ),
            'speaker': (
                '<p class="speaker">'
                f'by {speaker_affiliation}'
                '</p>'
            ),
            'abstract': (
                '<p class="abstract">'
                f'Abstract: {abstract}'
                '</p>'
            ),
        }

        return f'''<!DOCTYPE html><html>
            <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{self.css}">
            </head>
            <body>
            <div id="contents">
            {p['name']}
            {p['date_time_place']}
            {p['title']}
            {p['speaker']}
            {p['abstract']}
            </div>
            </body>
            </html>'''

    def _check_css(self):
        """
        Check if css exists.

        Returns
        -------
        None
        """
        if not Path(self.css).exists():
            raise FileNotFoundError(f'css file {self.css} does not exist.')

    def _get_maybe(self, seminar, attribute):
        return getattr(seminar, attribute, None) \
            or getattr(self.tba, attribute)

    def _get_seminar_name(self, seminar):
        """
        Return seminar name from config.

        Returns
        -------
        seminar_name : str
        """
        return config.seminar_name

    def _get_date_time(self, seminar):
        date = self._get_maybe(seminar, 'date')
        begin_time = self._get_maybe(seminar, 'begin_time')
        end_time = self._get_maybe(seminar, 'end_time')

        if date:
            try:
                date = Timestamp(date).strftime('%Y %b %d (%a)')
            except ValueError:
                date = date
        if begin_time:
            try:
                begin_time = Timestamp(begin_time).strftime('%H:%M')
            except ValueError:
                begin_time = begin_time
        if end_time:
            try:
                end_time = Timestamp(end_time).strftime('%H:%M')
            except ValueError:
                end_time = end_time

        if begin_time or end_time:
            return f'{date}, {begin_time} - {end_time}'
        else:
            return f'{date}'

    def _get_place(self, seminar):
        return self._get_maybe(seminar, 'place')

    def _get_title(self, seminar):
        return self._get_maybe(seminar, 'title')

    def _get_abstract(self, seminar):
        abstract = self._get_maybe(seminar, 'abstract')
        return abstract.replace('\n', '<br>')

    def _get_speaker_affiliation(self, seminar):
        speaker = self._get_maybe(seminar, 'speaker')
        affiliation = self._get_maybe(seminar, 'affiliation')

        if affiliation:
            return f'{speaker} ({affiliation})'
        else:
            return f'{speaker}'
