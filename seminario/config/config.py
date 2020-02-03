import yaml


lib_path = Path(dirname(__file__))


with open(lib_path / 'tba.yml') as f:
    tba = Bunch(yaml.load(f, Loader=yaml.FullLoader))

with open(lib_path / 'path.yml') as f:
    path = Bunch(yaml.load(f, Loader=yaml.FullLoader))

with open(lib_path / 'seminar.yml') as f:
    seminar = Bunch(yaml.load(f, Loader=yaml.FullLoader))
