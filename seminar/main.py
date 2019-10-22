import seminario


seminario.setup(
    database='./data/database.csv',
    dir_abstract='./data/abstract/',
    dir_slide='./data/slide/',
    dir_poster='./data/poster/',
    poster_css='./data/poster/css/poster.css',
)


def main():
    seminario.interactive.main()


if __name__ == '__main__':
    main()
