import pandas as pd

import seminario
from .stdin import StdIn


class InteractiveAPI:
    """
    Interactive API.

    Parameters
    ----------
    - config : path-like
        If None, use `config.path.database`.
    """
    def __init__(self, config=None):
        if config:
            seminario.config.setup(config)

    def main(self):
        line = '=' * len(seminario.config.seminar_name)
        print((
            f'\n{seminario.config.seminar_name}\n{line}\n'
            '(A) Add seminar\n'
            '(E) Edit seminar\n'
            '(P) Make poster\n'
            '(Q) Quit\n'
        ))

        operation = input('* Choose operation : ')

        if operation == 'A':
            self._add()
        elif operation == 'E':
            self._edit()
        elif operation == 'P':
            self._poster()
        elif operation == 'Q':
            self._quit()
        else:
            raise ValueError(f'Invalid input: {operation}')

    @property
    def database(self):
        return pd.read_csv(seminario.config.path.database, index_col=0)

    def _add(self):
        print('\n')
        data = StdIn().read_all()
        new_seminar = seminario.Seminar(**data)

        new_database = pd.concat([
            self.database,
            pd.DataFrame(new_seminar, index=[0]),
        ], axis=0)

        new_database = new_database.reset_index(drop=True)
        new_database.to_csv(seminario.config.path.database)

        print(new_database.tail())
        print('\nSuccessfully added a seminar to database.')

    def _edit(self):
        print('\n')
        raise NotImplementedError('Editing is not yet implemented. Sorry!')

    def _poster(self):
        print('\n')
        print(self.database.tail())

        print('\n')
        index = int(input('* Choose index to make a poster : '))

        seminar = seminario.Seminar(**self.database.iloc[index, :].to_dict())
        path = 'poster.pdf'
        seminario.PosterMaker().make_poster(seminar, path=path)

        print(f'Created a poster : {path}.')

    def _quit(self):
        pass
