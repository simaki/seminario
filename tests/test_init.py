import yaml
import pathlib
import pytest
import datetime
from typing import Optional

from seminario import Seminar


# def isinstance_maybe(obj, typing):
#     return (obj is None) or isinstance(obj, typing)

# def valid_data():
#     cases = list(pathlib.Path('./cases/valid/').glob('*.yml'))
#     cases.sort()
#     for case in cases:
#         with open(case) as f:
#             yield yaml.load(f, Loader=yaml.FullLoader)

# def invalid_data():
#     cases = list(pathlib.Path('./cases/invalid/').glob('*.yml'))
#     cases.sort()
#     for case in cases:
#         with open(case) as f:
#             yield yaml.load(f, Loader=yaml.FullLoader)

# @pytest.mark.parametrize('valid_data', valid_data())

# def test_typing(valid_data):
#     """
#     Test if Seminar.__init__ automatically convert typing.
#     """
#     seminar = Seminar(valid_data)
#     key_typing = [
#         ('date', datetime.date),
#         ('begin_time', datetime.time),
#         ('end_time', datetime.time),
#         ('place', str),
#         ('speaker', str),
#         ('affiliation', str),
#         ('title', str),
#         ('abstract_file', pathlib.PosixPath),
#         ('slide_file', pathlib.PosixPath),
#     ]
#     for key, typing in key_typing:
#         assert isinstance_maybe(seminar.data[key], typing)

# @pytest.mark.parametrize('invalid_data', invalid_data())

# def test_valueerror(invalid_data):
#     with pytest.raises(ValueError):
#         seminar = Seminar(invalid_data)

# def test_fillna():
#     seminar = Seminar(data={})
#     expected = {
#         'name': None,
#         'date': None,
#         'begin_time': None,
#         'end_time': None,
#         'place': None,
#         'speaker': None,
#         'affiliation': None,
#         'title': None,
#         'abstract_file': None,
#         'slide_file': None,
#     }
#     assert seminar.data == expected
