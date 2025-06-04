import datetime
import sqlite3

# stage 1 -  store and retrieve saved movies
#         - only one table, one default user - title, release_date, watched
# stage 2 - new table - multiple users and films they have watched
# stage 3 - 3 tables - movie table, users table, watched table


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY, 
    title TEXT,
    release_timestamp REAL
    );"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    ); """

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)    
    ); """

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES (?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
INSERT_WATCHED_MOVIES = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"
UPDATE_WATCHED_MOVIE = "UPDATE movies SET watched = 1 WHERE title = ?;"
SEARCH_MOVIE = "SELECT * FROM movies WHERE title LIKE ?;"
SEARCH_USERS = "SELECT * FROM users WHERE username LIKE ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
# orig SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE user_username = ?;"
SELECT_WATCHED_MOVIES = """SELECT m.*
                            FROM watched w
                            JOIN movies m 
                            ON m.id = w.movie_id
                            where w.user_username=?;
                        """

connection = sqlite3.connect("data.db")  # created adn saved by sqlite3 into the current folder


def create_tables():
    with connection:
        connection.execute("PRAGMA foreign_keys = ON")  # SQLite requires you to explicitly enable foreign key constraint enforcement
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)


def add_user(username):
    with connection:
        connection.execute(INSERT_USER, (username,))


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def search_movie(search_term):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
        return cursor.fetchall()


def find_user(search_term):
    with connection:
        cursor = connection.cursor()
        # cursor.execute(SEARCH_USERS, (f"%{search_term}%",))
        cursor.execute(SEARCH_USERS, (f"{search_term}",))
        return cursor.fetchall()


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(user_username, movie_id):
    try:
        with connection:
            connection.execute(INSERT_WATCHED_MOVIES, (user_username, movie_id))
    except sqlite3.IntegrityError as e:
        print(f"Error: cannot watch movie. Reason {e}.")
        print(f"Make sure that user and movie exist before trying again.")


def get_watched_movies(user_username):
    # todo - cannot distinguish if the user has no watched movies or the user was not found in the db
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (user_username,))
        return cursor.fetchall()


def users():
    with connection:
        cursor= connection.cursor()
        cursor.execute(SELECT_ALL_USERS)
        return cursor.fetchall()
