import os
import pdfkit

from os.path import dirname
from pathlib import Path

from .utils import Bunch
from .config import config



class PosterGenerator:
    """
    Generate poster.

    Parameters
    ----------
    - css : path-like
        The path of css of poster.
    - tba : dict
        The default values.
    """
    tba = config.tba
    css = config.path['css']

    def __init__(self, tba=None, css=css):
        """Initialize self"""
        self.css = Path(css)
        self.tba = tba or self.tba

    @staticmethod
    def __check_css(css):
        """
        Check if css exists.

        Returns
        -------
        None
        """
        if not pathlib.Path(css).exists():
            raise FileNotFoundError(f'css file {css} does not exist.')

    def _get_maybe(self, seminar, attribute):
        return getattr(seminar, attribute, None) or getattr(self.tba, attribute, '')

    def _get_name(self, seminar):
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
        return self._get_maybe(seminar, 'name')

    def _get_date_time(self, seminar):
        date = self._get_maybe(seminar, 'date')
        begin_time = self._get_maybe(seminar, 'begin_time')
        end_time = self._get_maybe(seminar, 'end_time')

        if date:
            date = date.strftime('%Y %b %d (%a)')
        if begin_time:
            begin_time = begin_time.strftime('%H:%M')
        if end_time:
            end_time = end_time.strftime('%H:%M')

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
            return f'{spaker} ({affiliation})'
        else:
            return f'{spaker}'

    def to_html(self, seminar, path=None):
        """
        Return or write html of the poster.

        Parameters
        ----------
        - seminar : Seminar
            Seminar to make a poster html.
        - path : path-like, optional
            Write html file if specified.
        """
        self.__check_css(css)

        # str of data or TBA values
        name = self.get_name(seminar)
        date_time = self._get_date_time(seminar)
        place = self._get_place(seminar)
        title = self._get_title(seminar)
        speaker_affiliation = self._get_speaker_affiliation(seminar)
        abstract = self._get_abstract(seminar)

        # Paragraph
        p = Bunch({
            'name': (
                '<p class="name">'
                f'{name}'
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
                '<p class="speaker_affiliation">'
                f'by {speaker_affiliation}'
                '</p>'
            ),
            'abstract': (
                '<p class="abstract">'
                f'Abstract: {abstract}'
                '</p>'
            ),
        })

        # HTML
        html = f'''<!DOCTYPE html><html>
            <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{self.css}">
            </head>
            <body>
            <div id="contents">
            {p.name}
            {p.date_time_place}
            {p.title}
            {p.speaker_affiliation}
            {p.abstract}
            </div>
            </body>
            </html>'''

        if path is not None:
            with open(path, 'w') as f:
                f.write(html)

        return html

    def to_pdf(self, seminar, path='poster.pdf'):
        """
        Generate pdf file of poster.

        Parameters
        ----------
        - seminar : Seminar
            Seminar to make a poster.
        - path : path-like, optional
            Path to make a poster.
        """
        tmp = 'tmp.html'
        self.to_html(seminar, tmp)
        pdfkit.from_file(tmp, path)
        os.remove(tmp)
