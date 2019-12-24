import yaml
import pathlib
import pytest
import datetime
from typing import Optional

from seminario import Seminar


def isinstance_maybe(obj, typing):
    return (obj is None) or isinstance(obj, typing)

def casedata():
    cases = list(pathlib.Path('./cases/').glob('*.yml'))
    cases.sort()
    for case in cases:
        with open(case) as f:
            yield yaml.load(f, Loader=yaml.FullLoader)

@pytest.mark.parametrize('data', casedata())

# ----------

def test_typing(data):
    """
    Test if Seminar.__init__ automatically convert typing.
    """
    seminar = Seminar(data)
    key_typing = [
        ('date', datetime.date),
        ('begin_time', datetime.time),
        ('end_time', datetime.time),
        ('place', str),
        ('speaker', str),
        ('affiliation', str),
        ('title', str),
        ('abstract_file', pathlib.PosixPath),
        ('slide_file', pathlib.PosixPath),
    ]
    for key, typing in key_typing:
        assert isinstance_maybe(seminar.data[key], typing)



