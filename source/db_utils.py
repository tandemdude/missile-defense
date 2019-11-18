import sqlite3
import typing


CREATE_TABLE_STATEMENT = """
CREATE TABLE IF NOT EXISTS scores(
	name text NOT NULL,
	score integer NOT NULL
);
"""

INSERT_STATEMENT = """
INSERT INTO scores(name, score) 
VALUES(?, ?);
"""

SELECT_STATEMENT = """
SELECT name, score FROM scores
ORDER BY score DESC LIMIT 10;
"""

DB_PATH = "highscores.db"


def create_database_and_table_if_not_exists() -> None:
    """
    Procedure to create a SQLite database file and
    the necessary table for scores to be stored

    :return: None
    """
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(CREATE_TABLE_STATEMENT)
        db.commit()


def insert_score(name: str, score: int) -> None:
    """
    Procedure to insert a new record into the scores
    database using a prepared statement

    :param name: The :class:`str` name to be stored
    :param score: The :class:`int` score to be stored
    :return: None
    """
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(INSERT_STATEMENT, [name, score])
        db.commit()


def get_high_scores() -> typing.Tuple[typing.Tuple[str, int]]:
    """
    Function to get the top 10 scores from the database
    in the correct order

    :return: :class:`tuple`[:class:`tuple`[:class:`str`, :class:`int]] of name, score pairs
    """
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(SELECT_STATEMENT)
        rows = cursor.fetchall()
        return rows
