import unittest
import shutil
import seminario


class TestInteractive(unittest.TestCase):

    def setUp(self):
        shutil.copy('./data/database.csv', './data/database_.csv')
        seminario.setup(
            database='./data/database_.csv',
            dir_abstract='./data/abstract/',
            dir_slide='./data/slide/',
            dir_poster='./data/poster/',
            poster_css='./data/poster/css/poster.css',
        )

    def test_interactive(self):
        seminario.interactive.main()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
