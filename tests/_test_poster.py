import unittest
import seminario

from context import (
    dict_seminar_A,
    dict_seminar_B,
    dict_seminar_n,
)


class TestPoster(unittest.TestCase):

    def setUp(self):
        seminario.setup(
            dir_abstract='./data/abstract/',
            dir_poster='./data/poster/',
            poster_css='./data/poster/css/poster.css',
        )

    def test_poster(self):
        seminar_A = seminario.Seminar(dict_seminar_A)
        seminar_B = seminario.Seminar(dict_seminar_B)
        seminar_n = seminario.Seminar(dict_seminar_n)

        seminar_A.make_poster()
        seminar_B.make_poster()
        seminar_n.make_poster()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
