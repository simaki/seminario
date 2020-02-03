import pytest

from os.path import dirname
from pathlib import Path
import yaml

from seminario import Seminar, PosterMaker
from seminario.config import config

tests_path = Path(dirname(__file__))


params_path = [
    tests_path / 'cases/valid/01.yml',
    tests_path / 'cases/valid/02.yml',
    tests_path / 'cases/valid/03.yml',
]


@pytest.mark.parametrize('path', params_path)
def test_poster(path):
    config.path.css = tests_path / 'data/poster/css/poster.css'
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        seminar = Seminar(**data)
    PosterMaker().make_pdf(seminar)
