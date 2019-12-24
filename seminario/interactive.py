import re

from .seminar import Seminar
from .database import Database
from .poster import PosterGenerator
from ._io import IOSeminarData


def add(seminar_name, csv_database, dir_abstract):
    """Add a new seminar to the database and overwrite."""
    database = Database.read_csv(csv_database)

    data = IOSeminarData().read_data().update({'name': seminar_name})
    seminar = Seminar(data)

    database.add(seminar)
    database.to_csv(csv_database)

    print(database.data.tail())
    print('\nAdded a seminar to database.')


def update(seminar_name, csv_database, dir_abstract):
    """Update a seminar in the database and overwrite."""
    database = Database.read_csv(csv_database)

    index = IOSeminarData().choose_index(database)
    seminar = Seminar(database.data.iloc[index].to_dict())

    data = IOSeminarData().update_data(seminar)
    seminar.update(data)

    database.update(index, seminar)
    database.to_csv(csv_database)

    print('\nUpdated database.')


def poster(seminar_name, csv_database, dir_abstract, css):
    """Make a poster of a seminar in the database."""
    database = Database.read_csv(csv_database)

    index = IOSeminarData().choose_index(database)
    seminar = Seminar(database.data.iloc[index].to_dict())

    path = 'poster.pdf'
    PosterGenerator(css=css).to_pdf(seminar, path=path)

    print('\nMade a poster: {path}.')


def quit():
    pass


f = {
    'A': add,
    'U': update,
    'P': poster,
    'Q': quit,
}


def main(seminar_name, csv_database, dir_abstract):
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
