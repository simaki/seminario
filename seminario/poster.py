import os
import pdfkit
import pathlib


class PosterGenerator:
    """
    Parameters
    ----------
    - css : path-like
        The path of css of poster.
    - tba : dict
        The default values.
    """
    __tba = {
        'name': 'Seminar',
        'date': 'TBA',
        'begin_time': '',
        'end_time': '',
        'place': 'TBA',
        'speaker': 'TBA',
        'affiliation': '',
        'title': 'TBA',
        'abstract_file': None,
        'slide_file': None,
    }

    def __init__(self, css, tba=None):
        """Initialize self"""
        self.__class__.__check_css(css)
        self.css = css
        self.tba = tba or self.__class__.__tba

    @staticmethod
    def __check_css(css):
        """Check if css exists."""
        if not pathlib.Path(css).exists():
            raise FileNotFoundError(f'css file {css} does not exist.')

    def __name(self, name):
        return name or self.__tba['name']

    def __date_time(self, date, begin_time, end_time):
        date = date.strftime('%Y %b %d (%a)') if date is not None \
            else self.__tba['date']

        if begin_time is None and end_time is None:
            time = ''
        else:
            begin_time = begin_time.strftime('%H:%M') \
                if begin_time is not None \
                else self.__tba['begin_time']
            end_time = end_time.strftime('%H:%M') \
                if end_time is not None \
                else self.__tba['end_time']
            time = f', {begin_time} - {end_time}'

        return f'{date}{time}'

    def __place(self, place):
        return place or self.__tba['place']

    def __title(self, title):
        return title or self.__tba['title']

    def __abstract(self, abstract):
        return abstract.replace('\n', '<br>') if abstract is not None \
            else self.__tba['abstract']

    def __speaker_affiliation(self, speaker, affiliation):
        speaker = speaker or self.__tba['speaker']
        affiliation = f' ({affiliation})' if affiliation is not None \
            else ''
        return f'{speaker}{affiliation}'

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
        # str of data or TBA values
        name = self.name(seminar.data['name'])
        date_time = self.__date_time(
            seminar.data['date'],
            seminar.data['begin_time'],
            seminar.data['end_time'],
        )
        place = self.__place(seminar.data['place'])
        title = self.__title(seminar.data['title'])
        speaker_affiliation = self.__speaker_affiliation(
            seminar.data['speaker'],
            seminar.data['affiliation'],
        )
        abstract = self.__abstract(seminar.data['abstract'])

        # Paragraph
        p = {
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
        }

        # HTML
        html = f'''<!DOCTYPE html><html>
            <head>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{self.css}">
            </head>
            <body>
            <div id="contents">
            {p['name']}
            {p['date_time_place']}
            {p['title']}
            {p['speaker_affiliation']}
            {p['abstract']}
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
