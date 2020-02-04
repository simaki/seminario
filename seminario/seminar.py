from .utils import Table

from .config import config
from pathlib import Path


class Seminar(Table):
    """
    Represent a seminar.

    Attributes
    ----------
    - date
    - begin_time
    - end_time
    - place
    - speaker
    - affiliation
    - title
    - abstract_file
    - slide_file
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def attributes(self):
        return (
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

    @property
    def abstract(self):
        """
        Return abstract sentences of self.

        Returns
        -------
        abstract : str
        """
        if self.abstract_file is None:
            return None

        path = Path(config.path.abstract) / self.abstract_file

        if not path.exists():
            raise FileNotFoundError(f'abstract_file {path} does not exist.')

        with open(path) as f:
            return f.read()
