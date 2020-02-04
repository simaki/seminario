import pytest


from seminario.cli.stdin import StdIn


params_date_valid = [
    '2000/01/01',
    '2000-01-01',
]
params_date_invalid = [
    '200-01-01',
    '2000-01-1',
    '2000-1-01',
    'hoge-fu-ga',
]

params_time_valid = [
    '12:00',
    '00:59',
]
params_time_invalid = [
    '1:00',
    '12:0',
    'ho:ge',
]

params_abst_valid = [
    'alice.txt',
]
params_abst_invalid = [
    'alice.rtf',
    '.txt',
    'alice.txt.rtf',
]

params_slide_valid = [
    'alice.pdf',
]
params_slide_invalid = [
    'alice.rtf',
    '.pdf',
    'alice.pdf.rtf',
]


# --------------------------------------------------------------------------------


@pytest.mark.parametrize('date', params_date_valid)
def test_date_valid(date):
    stdin = StdIn()
    assert stdin._check('date', date) == date


@pytest.mark.parametrize('date', params_date_invalid)
def test_date_invalid(date):
    stdin = StdIn()
    with pytest.raises(ValueError):
        stdin._check('date', date)


@pytest.mark.parametrize('time', params_time_valid)
def test_time_valid(time):
    stdin = StdIn()
    assert stdin._check('begin_time', time) == time


@pytest.mark.parametrize('time', params_time_invalid)
def test_time_invalid(time):
    stdin = StdIn()
    with pytest.raises(ValueError):
        stdin._check('begin_time', time)


@pytest.mark.parametrize('abst', params_abst_valid)
def test_abst_valid(abst):
    stdin = StdIn()
    assert stdin._check('abstract_file', abst) == abst


@pytest.mark.parametrize('abst', params_abst_invalid)
def test_abst_invalid(abst):
    stdin = StdIn()
    with pytest.raises(ValueError):
        stdin._check('abstract_file', abst)


@pytest.mark.parametrize('slide', params_slide_valid)
def test_slide_valid(slide):
    stdin = StdIn()
    assert stdin._check('slide_file', slide) == slide


@pytest.mark.parametrize('slide', params_slide_invalid)
def test_slide_invalid(slide):
    stdin = StdIn()
    with pytest.raises(ValueError):
        stdin._check('slide_file', slide)
