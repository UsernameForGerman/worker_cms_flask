import typing as tp

import app
import models


def get_authors() -> tp.List[models.Author]:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        raw_authors = cursor.execute('SELECT * FROM author')
        return [models.Author(*raw_author) for raw_author in raw_authors]


def get_author_by_id(id: int) -> tp.Dict[str, tp.Union[models.Author, models.Death, tp.List[tp.Union[models.Country, models.Work]]]]:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        authors = cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.birth_date,
            d.id,
            d.death,
            c.id,
            c.name,
            w.id,
            w.release_date,
            w.title,
            w.type
        FROM author a
        LEFT JOIN death d
            ON d.id = a.id
        INNER JOIN country_to_author ctw
            ON ctw.author_id = a.id
        INNER JOIN country c
            ON c.id = ctw.country_id
        LEFT JOIN author_to_work atw
            ON atw.author_id = a.id
        LEFT JOIN work w
            ON w.id = atw.work_id
        WHERE a.id = ?
        ORDER BY w.type;
        """, [id]).fetchall()
        if not authors:
            raise app.exceptions.NotFound()
        countries, works = [], []
        for author in authors:
            country = models.Country(author[5], author[6])
            if country not in countries:
                countries.append(country)
            work = models.Work(author[7], author[8], author[9], author[10]) if author[7] is not None else None
            if work and work not in works:
                works.append(work)
        return {
            'author': models.Author(authors[0][0], authors[0][1], authors[0][2]),
            'death': models.Death(authors[0][3], authors[0][4]) if authors[0][3] is not None else None,
            'countries': countries,
            'works': works
        }


def get_works() -> tp.List[models.Work]:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        raw_works = cursor.execute('SELECT * FROM work')
        return [models.Work(*raw_work) for raw_work in raw_works]


def get_work_by_id(id: int) -> tp.Dict[str, tp.Union[models.Work, tp.List[tp.Union[models.Country, models.Author]]]]:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        works = cursor.execute("""
        SELECT 
            w.id, 
            w.release_date,
            w.title,
            w.type,
            c.id,
            c.name,
            a.id,
            a.name,
            a.birth_date
        FROM work w
        INNER JOIN country_to_work ctw
            ON ctw.work_id = w.id
        INNER JOIN country c
            ON ctw.country_id = c.id
        INNER JOIN author_to_work atw
            ON atw.work_id = w.id
        INNER JOIN author a
            ON atw.author_id = a.id
        WHERE w.id = ?;
        """, [id]).fetchall()
        if not works:
            raise app.exceptions.NotFound()
        countries, authors = [], []
        for work in works:
            country = models.Country(work[4], work[5])
            if country not in countries:
                countries.append(country)
            author = models.Author(work[6], work[7], work[8]) if work[6] is not None else None
            if author and author not in authors:
                authors.append(author)
        return {
            'work': models.Work(
                works[0][0], works[0][1], works[0][2], works[0][3]
            ),
            'countries': countries,
            'authors': authors
        }


def generate_new_id_for_model(model: tp.Type[tp.Union[models.Author, models.Death, models.Work, models.Country, models.AuthorToWork, models.CountryToWork, models.CountryToAuthor]]) -> int:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        id = cursor.execute('SELECT id FROM {tablename} ORDER BY id DESC LIMIT 1;'.format(tablename=model.__tablename__)).fetchone()
        return id[0] + 1


def insert_author(author: models.Author, death: tp.Optional[models.Death], countries: tp.List[str], works: tp.List[str]):
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO author (id, name, birth_date)
            VALUES (?, ?, ?);
            """, [author.id, author.name, author.birth_date]
        )
        if death:
            cursor.execute(
                """
                INSERT INTO death (id, death)
                VALUES (?, ?)
                """, [death.id, death.death]
            )
        cursor.executemany(
            """
            INSERT INTO country_to_author(country_id, author_id)
            VALUES (?, ?)
            """,
            [(country_id, author.id) for country_id in countries]
        )
        if works:
            cursor.executemany(
                """
                INSERT INTO author_to_work(author_id, work_id)
                VALUES (?, ?)
                """,
                [(author.id, work_id) for work_id in works]
            )


def insert_work(work: models.Work, countries: tp.List[str], authors: tp.List[str]):
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO work (id, title, release_date, type)
            VALUES (?, ?, ?, ?);
            """, [work.id, work.title, work.release_date, work.type]
        )
        cursor.executemany(
            """
            INSERT INTO country_to_work(country_id, work_id)
            VALUES (?, ?)
            """,
            [(country_id, work.id) for country_id in countries]
        )
        if authors:
            cursor.executemany(
                """
                INSERT INTO author_to_work(author_id, work_id)
                VALUES (?, ?)
                """,
                [(author_id, work.id) for author_id in authors]
            )


def get_countries() -> tp.List[models.Country]:
    with app.sqlite3.connect(app.DBNAME) as conn:
        cursor = conn.cursor()
        return [models.Country(*country) for country in cursor.execute(
            """
            SELECT * FROM country;
            """
        )]
