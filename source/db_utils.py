import sqlite3


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


def create_database_and_table_if_not_exists():
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(CREATE_TABLE_STATEMENT)
        db.commit()
        return


def insert_score(name: str, score: int):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(INSERT_STATEMENT, [name, score])
        db.commit()
        return


def get_high_scores():
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute(SELECT_STATEMENT)
        rows = cursor.fetchall()
        return rows
