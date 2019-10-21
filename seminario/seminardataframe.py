import datetime
import pandas as pd

from seminario.config import _Config
from seminario.seminar import Seminar


class SeminarDataFrame(pd.core.frame.DataFrame):
    """
    Dataframe with the data of seminars.

    Inheriting ``pandas.DataFrame``.

    Each ``index`` specifies each seminar.
    The ``columns`` must have the following items:
        - 'date'
        - 'begin time'
        - 'end time'
        - 'place'
        - 'speaker'
        - 'affiliation
        - 'title'
        - 'abstract file'
        - 'slide file'
    """

    def __init__(self, data=None, **kwargs):
        """Initializes self."""
        if data is not None:
            super(SeminarDataFrame, self).__init__(data, **kwargs)
            self.replace({pd.np.nan: None}, inplace=True)
        else:
            kwargs['columns'] = list(Seminar()._dict.keys())
            super(SeminarDataFrame, self).__init__(data={}, **kwargs)

    @classmethod
    def read_database(cls, database=None):
        """
        Read a csv file into ``SeminarDataFrame``.

        Parameters
        ----------
        - database : str
            Path of the seminar dataframe.
            If None, ``_Config.database``.

        Returns
        -------
        SeminarDataFrame

        Example
        -------

        >>> seminario.setup(database='./data/database.csv')
        >>> smdf = seminario.read_database()
        >>> smdf
                 date begin time end time place        speaker  ...
        0  2019-01-01      12:00    13:00  101A  Alice Speaker  ...
        1  2019-02-02      12:30    13:30  102B     Bob Talker  ...
                   title abstract file slide file
        0   Apple Effect     alice.txt  alice.pdf
        1  Banana Effect       bob.txt    bob.pdf
        """
        def _to_time(s):
            return datetime.datetime.strptime(s, '%H:%M').time()

        database = database or _Config.database
        if database is None:
            raise ValueError('Database is neither set nor specified.')
        try:
            df = pd.read_csv(database, index_col=0, parse_dates=['date'])
            # df['date'] = df['date'].map(_to_date)
            df['begin time'] = df['begin time'].map(_to_time)
            df['end time'] = df['end time'].map(_to_time)

        except FileNotFoundError as e:
            print(e)
        return SeminarDataFrame(df)

    def to_database(self, database=None):
        """
        Write self to a csv file (database).

        Parameters
        ----------
        - database : str, path object or file-like object
            Path to write.
        """
        def _to_HHMM(s):
            if s is None:
                return ''
            else:
                return s.strftime('%H:%M')

        self_ = self
        self_['begin time'] = self_['begin time'].map(_to_HHMM)
        self_['end time'] = self_['end time'].map(_to_HHMM)

        database = database or _Config.database
        if database is None:
            raise ValueError('The database is neither set nor specified.')
        else:
            self.to_csv(database)

    def add(
        self,
        seminar: Seminar = None,
        inplace=False,
        interactive=False
    ):
        """
        Add a new ``Seminar`` to self.

        Parameters
        ----------
        - seminar : Seminar
            ``Seminar`` to add.
        - inplace : bool, default False
            If True, add inplace and return None.
        - interactive : bool, default False
            If True, add interactively.
        """
        if interactive:
            seminar = Seminar(interactive=True)

        if inplace:
            i = self.index[-1] + 1 if list(self.index) else 0
            self.loc[i] = seminar.to_Series()
        else:
            return self.append(seminar.to_DataFrame(),
                               ignore_index=True, sort=False)

    def edit(
        self,
        data={},
        index=None,
        inplace=False,
        interactive=False,
    ):
        """
        Edit a ``Seminar`` in self.

        Parameters
        ----------
        - data: dict
            New data of the seminar.
        - index: int
            Index of the seminar to edit.
        - inplace : bool, default False
            If True, edit inplace and return None.
        - interactive : bool, default False
            If True, edit interactively.
        """
        seminar = Seminar(self.iloc[index, :])
        seminar_new = seminar.edit(data,
                                   inplace=False,
                                   interactive=interactive)
        if inplace:
            self.loc[index] = seminar_new.to_Series()
        else:
            self_new = self.copy()
            self_new.loc[index] = seminar_new.to_Series()
            return self_new

    def make_poster(
        self,
        index=None,
        path=None,
        css=None,
        interactive=False,
    ):
        """
        Make a poster of ``seminar`` in self.

        Parameters
        ----------
        - index : int
            Index of the ``Seminar`` to make a poster.
        - path : str, path object or file-like object
            Path of the poster.
        - css : str, path object or file-like object
            Path of the css file of the poster.
        - interactive : bool
            If True, choose index interactively.
        """
        if interactive:
            index = self._choose_index()
        s = Seminar(data=self.loc[index, :])
        s.make_poster(path=path, css=css)

    def _choose_index(self):  # TODO
        """
        Choose an index of self interactively.

        Example
        -------

        >>> index = sdf._choose_index()
                date ...
        0 2019-04-11 ...
        1 2019-05-12 ...
        2 2019-06-13 ...
        3 2019-07-13 ...
        4 2019-08-14 ...
        - Enter index:
        >>> 1
        >>> s = sdf.loc[index, :]
        >>> seminar.Seminar(data=s)
        date        : 2019-05-12
        begin time  : ...
        ...
        """
        num_show = 5
        self_show = self.copy()
        while len(self_show.index):
            print(self_show.tail(num_show))
            i = input('- Enter index : ') or None
            i = int(i) if i is not None else None
            if i in self_show.index:
                return i
            self_show = self_show.iloc[:-num_show]
