from re import fullmatch


class StdIn:
    """
    StdIn.
    """
    keys = (
        'date',
        'begin_time',
        'end_time',
        'place',
        'speaker',
        'affiliation',
        'title',
        'abstract_file',
        'slide_file',
    )

    suggestion = {
        'date': ' (YYYY-MM-DD)',
        'begin_time': ' (HH:MM)',
        'end_time': ' (HH:MM)',
        'place': '',
        'speaker': '',
        'affiliation': '',
        'title': '',
        'abstract_file': ' (*.txt)',
        'slide_file': ' (*.pdf)',
    }

    re = {
        'date': r'\d{4}[-/]\d{2}[-/]\d{2}',
        'begin_time': r'\d{2}:\d{2}',
        'end_time': r'\d{2}:\d{2}',
        'place': r'.+',
        'speaker': r'.+',
        'affiliation': r'.+',
        'title': r'.+',
        'abstract_file': r'.+\.txt',
        'slide_file': r'.+\.pdf',
    }

    # def read(self, key):
    #     """
    #     Read standard input.

    #     Returns
    #     -------
    #     value : str or None
    #     """
    #     while True:
    #         try:
    #             value = input(f'Input {key}{self.suggestion[key]} : ')
    #             value = self._check(value)
    #         except ValueError as e:
    #             print(e)
    #         else:
    #             return value

    # def readall(self):
    #     """
    #     Read standard input of all keys.

    #     Returns
    #     -------
    #     values : dict
    #     """
    #     return {
    #         key: self.read(key) for key in self.keys
    #     }

    def _check(self, key, value):
        """
        Check if value is a valid input for key.

        Returns
        -------
        value
            If value is empty or value matches with regex.

        Raises
        ------
        ValueError
            If value is not empty and does not match with regex.
        """
        if not value:
            return value
        if fullmatch(self.re[key], value):
            return value
        raise ValueError(f'Invalid input: {value}')
