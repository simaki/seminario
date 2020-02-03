from .utils import Bunch

from .config import config
from pathlib import Path


class Seminar(Bunch):
    """
    Represent a seminar.

    Parameters
    ----------
    - date : datetime.date
    - begin_time : datetime.time
    - end_time : datetime.time
    - place : str
    - speaker : str
    - affiliation : str
    - title : str
    - abstract_file : pathlib.PosixPath
    - slide_file : pathlib.PosixPath
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def abstract(self):
        """
        Return abstract sentences of self.

        Returns
        -------
        abstract : str
        """
        return self.__read_abstract()

    def __read_abstract(self):
        if self.abstract_file is None:
            return ''

        path = Path(config.path.abstract) / self.abstract_file

        if not path.exists():
            raise FileNotFoundError(f'abstract_file {path} does not exist.')

        with open(path) as f:
            return f.read()
