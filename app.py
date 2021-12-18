import sqlite3

from flask import Flask
from flask_bootstrap import Bootstrap
from werkzeug import exceptions


app = Flask(__name__)
app.url_map.strict_slashes = False
Bootstrap(app)
DBNAME = 'main.db'


def prepare_db():
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    statements = [
        """
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER UNIQUE NOT NULL PRIMARY KEY,
            name TEXT,
            birth_date TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS death(
            id INTEGER UNIQUE NOT NULL PRIMARY KEY,
            death DATE,
            FOREIGN KEY (id) REFERENCES author(id) ON DELETE CASCADE
            ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS country(
            id INTEGER UNIQUE NOT NULL PRIMARY KEY,
            name TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS work(
            id INTEGER UNIQUE NOT NULL PRIMARY KEY,
            release_date TEXT,
            title TEXT,
            type TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS country_to_author(
            country_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS country_to_work(
            country_id INTEGER NOT NULL,
            work_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE,
            FOREIGN KEY (work_id) REFERENCES work(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS author_to_work(
            author_id INTEGER NOT NULL,
            work_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE,
            FOREIGN KEY (work_id) REFERENCES work(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS country_to_author_country_id_idx 
        ON country_to_author(country_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS country_to_author_author_id_idx
        ON country_to_author(author_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS country_to_work_country_id_idx
        ON country_to_work(country_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS country_to_work_work_id_idx
        ON country_to_work(work_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS author_to_work_author_id_idx
        ON author_to_work(author_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS author_to_work_work_id_idx
        ON author_to_work(work_id);
        """
    ]
    for statement in statements:
        cursor.execute(statement)


if __name__ == "__main__":

    # Need to make sure Flask knows about its views before we run
    # the app, so we import them. We could do it earlier, but there's
    # a risk that we may run into circular dependencies, so I do it at the
    # last minute here.

    from views import *

    prepare_db()
    app.app.run(debug=True, host='0.0.0.0', port=5030)  # 0.0.0.0 означает «все адреса IPv4 на локальном компьютере».
