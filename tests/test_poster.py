import pytest

import yaml

from seminario import Seminar, PosterMaker
from seminario.config import config


params_path = [
    'cases/valid/01.yml',
    'cases/valid/02.yml',
    'cases/valid/03.yml',
]


@pytest.mark.parametrize('path', params_path)
def test_poster(path):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        seminar = Seminar(**data)
    PosterMaker().make_pdf(seminar)
