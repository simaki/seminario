import re

import pandas as pd

from seminario.seminar import Seminar
from seminario.poster import PosterMaker
from ._io import IOSeminarData

from .config import config


def add():
    """Add a new seminar to the database and overwrite."""
    database = pd.read_csv(
        config.path.database,
        index_col=0, parse_dates=['date', 'begin_time', 'end_time']
    )

    seminar = Seminar(IOSeminarData().read_data())

    database = pd.concat([database, pd.DataFrame(seminar, index=[0])])
    database.reset_index(drop=True)
    database.to_csv(config.path.database)

    print(database.tail())
    print('\nAdded a seminar to database.')


def update():
    """Update a seminar in the database and overwrite."""
    database = pd.read_csv(
        config.path.database,
        index_col=0, parse_dates=['date', 'begin_time', 'end_time']
    )

    index = IOSeminarData().choose_index(database)
    seminar = Seminar(database.data.iloc[index, :].to_dict())
    seminar = Seminar(IOSeminarData().update_data(seminar))

    database.iloc[index, :] = pd.DataFrame(seminar).iloc[0, :]
    database.to_csv(config.path.database)

    print('\nUpdated database.')


def poster():
    """Make a poster of a seminar in the database."""
    database = pd.read_csv(
        config.path.database,
        index_col=0, parse_dates=['date', 'begin_time', 'end_time']
    )

    index = IOSeminarData().choose_index(database)
    seminar = Seminar(database.data.iloc[index].to_dict())

    path = 'poster.pdf'
    PosterMaker().to_pdf(seminar, path=path)

    print(f'\nMade a poster: {path}.')


def quit():
    pass


f = {
    'A': add,
    'U': update,
    'P': poster,
    'Q': quit,
}


def main(seminar_name, csv_database, dir_abstract, css):
    print(f'''
    {seminar_name}
    {'=' * len(seminar_name)}

    (A) Add seminar
    (E) Edit seminar
    (P) Make poster
    (Q) Quit
    ''')

    done = False
    while not done:
        answer = input('- Choose : ')
        if re.match('[AEPQaepq]', answer):
            f[answer[0].upper()]()
            done = True
        else:
            print('Invalid input : ', answer)


if __name__ == '__main__':
    main()
