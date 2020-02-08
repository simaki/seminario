from os.path import dirname
from pathlib import Path

from cli.api import InteractiveAPI


here = Path(dirname(__file__))


if __name__ == '__main__':
    config = here / 'data/config.yml'
    InteractiveAPI(config=config).main()



