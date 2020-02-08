# import pytest
# from os.path import dirname
# from pathlib import Path
# import yaml

# from seminario.cli.stdin import StdIn

# tests_path = Path(dirname(__file__))


# with open(tests_path / 'cases/input/date.yml') as f:
#     cases_date = yaml.load(f, Loader=yaml.FullLoader)

# with open(tests_path / 'cases/input/time.yml') as f:
#     cases_time = yaml.load(f, Loader=yaml.FullLoader)

# with open(tests_path / 'cases/input/abstract.yml') as f:
#     cases_abstract = yaml.load(f, Loader=yaml.FullLoader)

# with open(tests_path / 'cases/input/slide.yml') as f:
#     cases_slides = yaml.load(f, Loader=yaml.FullLoader)


# params_date_valid = cases_date['valid']
# params_date_invalid = cases_date['invalid']

# params_time_valid = cases_time['valid']
# params_time_invalid = cases_time['invalid']

# params_abstract_valid = cases_abstract['valid']
# params_abstract_invalid = cases_abstract['invalid']

# params_slide_valid = cases_slides['valid']
# params_slide_invalid = cases_slides['invalid']


# # --------------------------------------------------------------------------------


# @pytest.mark.parametrize('date', params_date_valid)
# def test_date_valid(date):
#     stdin = StdIn()
#     assert stdin._check('date', date) == date


# @pytest.mark.parametrize('date', params_date_invalid)
# def test_date_invalid(date):
#     stdin = StdIn()
#     with pytest.raises(ValueError):
#         stdin._check('date', date)


# @pytest.mark.parametrize('time', params_time_valid)
# def test_time_valid(time):
#     stdin = StdIn()
#     assert stdin._check('begin_time', time) == time


# @pytest.mark.parametrize('time', params_time_invalid)
# def test_time_invalid(time):
#     stdin = StdIn()
#     with pytest.raises(ValueError):
#         stdin._check('begin_time', time)


# @pytest.mark.parametrize('abstract', params_abstract_valid)
# def test_abstract_valid(abstract):
#     stdin = StdIn()
#     assert stdin._check('abstract_file', abstract) == abstract


# @pytest.mark.parametrize('abstract', params_abstract_invalid)
# def test_abstract_invalid(abstract):
#     stdin = StdIn()
#     with pytest.raises(ValueError):
#         stdin._check('abstract_file', abstract)


# @pytest.mark.parametrize('slide', params_slide_valid)
# def test_slide_valid(slide):
#     stdin = StdIn()
#     assert stdin._check('slide_file', slide) == slide


# @pytest.mark.parametrize('slide', params_slide_invalid)
# def test_slide_invalid(slide):
#     stdin = StdIn()
#     with pytest.raises(ValueError):
#         stdin._check('slide_file', slide)
