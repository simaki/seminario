from os.path import dirname
from pathlib import Path
import yaml

from ..utils import Bunch


lib_path = Path(dirname(__file__))


with open(lib_path / 'tba.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)
    tba = Bunch(**data)
    print(tba)

with open(lib_path / 'path.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    path = Bunch(**data)

with open(lib_path / 'seminar.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    seminar = Bunch(**data)
