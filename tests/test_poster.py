import pytest

from os.path import dirname
from pathlib import Path
import yaml

from seminario import Seminar, PosterMaker
from seminario.config import config

tests_path = Path(dirname(__file__))


params_seminardata = [
    tests_path / 'cases/seminar/01.yml',
    tests_path / 'cases/seminar/02.yml',
    tests_path / 'cases/seminar/03.yml',
    tests_path / 'cases/seminar/04.yml',
    tests_path / 'cases/seminar/05.yml',
    tests_path / 'cases/seminar/06.yml',
    tests_path / 'cases/seminar/07.yml',
    tests_path / 'cases/seminar/08.yml',
]

def yml_to_seminar(yml):
    """
    Parameters
    ----------
    - yml : path-like
        Yaml file of seminar data.

    Returns
    -------
    Seminar
    """
    with open(yml) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return Seminar(**data)


# --------------------------------------------------------------------------------


@pytest.fixture(scope='module', autouse=True)
def setup():
    config.path.abstract = tests_path / 'data/abstract/'
    config.path.css = tests_path / 'data/poster/poster.css'


@pytest.mark.parametrize('seminardata', params_seminardata)
def test_poster(seminardata):
    print(config.path.css)
    seminar = yml_to_seminar(seminardata)
    maker = PosterMaker()
    maker.make_pdf(seminar)
