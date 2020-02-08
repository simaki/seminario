import pytest

from os.path import dirname
from pathlib import Path
import yaml

from seminario import Seminar, PosterMaker
from seminario.config import config

tests_path = Path(dirname(__file__))


params_seminardata = list((tests_path / 'cases/seminar/').glob('*.yml'))


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
    config.setup(tests_path / 'data/config/default.yml')
    config.path.abstract = tests_path / 'data/abstract/'
    config.path.css = tests_path / 'data/poster/poster.css'


@pytest.mark.parametrize('seminardata', params_seminardata)
def test_poster(seminardata):
    seminar = yml_to_seminar(seminardata)
    maker = PosterMaker()
    path = tests_path / f'outputs/{seminardata.stem}.pdf'
    maker.make_poster(seminar, path=path)


@pytest.mark.parametrize('seminardata', params_seminardata[:1])
def test_absent_css(seminardata):
    config.path.css = tests_path / 'data/poster/absent.css'
    seminar = yml_to_seminar(seminardata)
    maker = PosterMaker()

    with pytest.raises(FileNotFoundError):
        maker.make_poster(seminar)
