from os.path import dirname
from pathlib import Path
import yaml

from seminario.utils import Bunch

module_path = Path(dirname(__file__))


class Config:
    """
    Configuration.

    Attributes
    ----------
    - seminar_name : str
    - tba : dict
    - path
    """
    def __init__(self):
        with open(module_path / 'default.yml') as f:
            default = yaml.load(f, Loader=yaml.FullLoader)

        self.seminar_name = default['seminar_name']
        self.tba = Bunch(**default['tba'])
        self.path = Bunch(**default['path'])

    def setup(self, yml):
        """
        Read yml file to setconfiguration.

        Parameters
        ----------
        - yml : path-like
            yml file.

        Notes
        -----
        Sample of yml file:
        ```
        seminar_name: Seminar
        tba:
            date: TBA
        path:
            abstract:
        ```
        """
        with open(yml) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            data_tba = data.get('tba', None) or {}
            data_path = data.get('path', None) or {}

        self.seminar_name = data.get('seminar_name', None) or self.seminar_name
        for key, value in data_tba.items():
            setattr(self.tba, key, value)
        for key, value in data_path.items():
            setattr(self.path, key, value)


config = Config()
