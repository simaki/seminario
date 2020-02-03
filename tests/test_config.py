import pytest


from seminario.config import config


def test_path():
    config.path == {
        'database': 'data/database.csv',
        'abstract': 'data/abstract/',
        'css': 'data/poster/css/poster.css',
    }

def test_seminar():
    config.seminar == {
        'name': 'Seminar',
    }

def test_tba():
    config.tba == {
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

