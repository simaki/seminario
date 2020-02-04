import pytest  # flake8: noqa

from os.path import dirname
from pathlib import Path

from seminario.config import config


tests_path = Path(dirname(__file__))


default_seminar_name = 'Seminar'
default_path = {
    'database': 'data/database.csv',
    'abstract': 'data/abstract/',
    'css': 'data/poster/css/poster.css',
}
default_tba = {
    'date': 'TBA',
    'begin_time': '',
    'end_time': '',
    'place': 'TBA',
    'speaker': 'TBA',
    'affiliation': '',
    'title': 'TBA',
    'abstract': 'TBA',
}

new_seminar_name = 'New Seminar'
new_path = {
    'database': 'new.csv',
    'abstract': 'new/',
    'css': 'new.css',
}
new_tba = {
    'date': 'New TBA date',
    'begin_time': 'New TBA begin_time',
    'end_time': 'New TBA end_time',
    'place': 'New TBA place',
    'speaker': 'New TBA speaker',
    'affiliation': 'New TBA affiliation',
    'title': 'New TBA title',
    'abstract': 'New TBA abstract',
}

params_default = [
    ('path', default_path),
    ('seminar_name', default_seminar_name),
    ('tba', default_tba),
]

params_new = [
    ('path', new_path),
    ('seminar_name', new_seminar_name),
    ('tba', new_tba),
]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('attr, value', params_default)
def test_default(attr, value):
    assert getattr(config, attr) == value


@pytest.mark.parametrize('attr, value', params_new)
def test_setup(attr, value):
    config.setup(tests_path / 'data/config.yml')
    assert getattr(config, attr) == value
