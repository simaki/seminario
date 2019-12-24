import seminario


CSV_DATABASE = './data/database.csv'
SEMINAR_NAME = 'Seminar'
DIR_ABSTRACT = './data/abstract/'


def main():
    seminario.interactive.main(
        csv_database=CSV_DATABASE,
        seminar_name=SEMINAR_NAME,
        dir_abstract=DIR_ABSTRACT,
    )


if __name__ == '__main__':
    main()
