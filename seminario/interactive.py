import re
import seminario


def add():
    """Add a new seminar to the database and overwrite."""
    smdf = seminario.SeminarDataFrame.read_database()
    smdf = smdf.add(interactive=True)
    smdf.to_database()
    print(smdf.tail())
    print('\nAdded a seminar.')


def edit():
    """Edit a seminar in the database and overwrite."""
    smdf = seminario.SeminarDataFrame.read_database()
    smdf.edit(interactive=True)
    print('\nEdited a seminar.')


def poster():
    """Make a poster of a seminar in the database."""
    smdf = seminario.SeminarDataFrame.read_database()
    smdf.make_poster(interactive=True)
    print('\nMade a poster.')


def quit():
    pass


f = {
    'A': add,
    'E': edit,
    'P': poster,
    'Q': quit,
}


def main():
    name = seminario.config._Config.name
    print('\n{}\n{}'.format(name, '=' * len(name)))

    print((
        '(A) Add seminar\n'
        '(E) Edit seminar\n'
        '(P) Make Poster\n'
        '(Q) Quit\n'
    ))

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
