import os
import pdfkit

from pandas import Timestamp

from pathlib import Path

from .config import config


class PosterMaker:
    """
    Generate poster.

    Parameters
    ----------
    - css : path-like
        Path of poster css.
    - tba : dict
        Default values.
    """
    tba = config.tba
    css = config.path.css

    def __init__(self, tba=None, css=None):
        self.css = Path(css or self.css)
        self.tba = tba or self.tba

    def make_pdf(self, seminar, path='poster.pdf'):
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
        - path : path-like, optional
            Write html file if specified.

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
        if not self.css.exists():
            raise FileNotFoundError(f'css file {self.css} does not exist.')

    def _get_maybe(self, seminar, attribute):
        return getattr(seminar, attribute, None) \
            or getattr(self.tba, attribute, '')

    def _get_seminar_name(self, seminar):
        """
        Return seminar name.

        Examples
        --------
        If exists:
        >>> seminar.name
        'Nice Seminar'
        >>> poster_generator._get_name(seminar)
        'Nice Seminar'

        If not:
        >>> seminar.name
        None
        >>> poster_generator.tba.name
        'Good Seminar'
        >>> poster_generator._get_name(seminar)
        'Good Seminar'
        """
        return config.seminar.seminar_name

    def _get_date_time(self, seminar):
        date = self._get_maybe(seminar, 'date')
        begin_time = self._get_maybe(seminar, 'begin_time')
        end_time = self._get_maybe(seminar, 'end_time')

        if date:
            date = Timestamp(date).strftime('%Y %b %d (%a)')
        if begin_time:
            begin_time = Timestamp(begin_time).strftime('%H:%M')
        if end_time:
            end_time = Timestamp(end_time).strftime('%H:%M')

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
