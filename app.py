from typing import List
import datetime
import database

menu = """Please select one of the following options:
 1) Add new movie.
 2) View upcoming movies.
 3) View all movies.
 4) Watch a movie.
 5) View watched movies.
 6) Add a new user.
 7) Search for a movie.
 8) Exit.
 
 Your selection: """

welcome = """ 
--------------------------------------
      Welcome to the watchlist app
-------------------------------------- 
"""

print(welcome)
database.create_tables()


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def _show_users(show_users_tag):
    users = database.users()
    if show_users_tag:
        if users:
            print(f"--- registred users  ---")
            for user in users:
                print(user[0])
            print("--\n")
        else:
            print(f"No registred users.")
    else:
        return [user[0] for user in users]


def _find_user():
    """ Is case insensitive """
    search_term = input("Enter the partial user name: ")
    users = database.find_user(search_term)
    if users:
        print(f"Following user(s) match:")
        for user in users:
            print(f"- {user[0]}")
    else:
        print("No such user.")


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)
    # corresponding code in db when adding the movie manually:
    # INSERT INTO movies (title, release_timestamp)
    # VALUES ('Inception', strftime('%s', '2010-07-16'));


def prompt_watch_movie():
    username = input("Enter name of the user: ")
    # cannot distinguish if the user has no watched movies or the user was not found in the db
    if username in _show_users(0):
        movie_id = input("Enter ID of the movie you have watched: ")
        # movie_title = input("Enter title of the movie you have watched: ")
        # todo - user will insert movie title, not id
        database.watch_movie(username, movie_id)
    else:
        print(f"The provided user '{username}' is not registred.")


def print_movie_list(heading: str, movies: List) -> None:
    print(f"--- {heading} ---")
    for _id, title, release_date in movies:
        movie_date = datetime.date.fromtimestamp(release_date)
        human_date = movie_date.strftime("%d.%m.%Y")
        print(f"{_id}: {title} ({human_date})")
    print("--\n")


def prompt_search_movies():
    search_term = input("Enter the partial movie title: ")
    movies = database.search_movie(search_term)
    print(movies)
    if movies:
        print_movie_list("Found movies", movies)
    else:
        print("No movie found.")


def prompt_show_watched_movies():
    user = input("Enter name of the user: ")  # TODO make it case insensitive
    # TODO - no check for duplicates in the watched table
    # cannot distinguish if the user has no watched movies or the user was not found in the db
    if user in _show_users(0):
        movies = database.get_watched_movies(user)
        if movies:
            print_movie_list(f"{user} watched following movies ", movies)
        else:
            print(f"{user} has no watched movies.")
    else:
        print(f"The provided user '{user}' is not registred.")


# walrus operator := combining assignment and use in a single step
while (user_input := input(menu)) != "8":
    print(f"You have chosen {user_input}.")
    if user_input == "1":
        # Add new movie.
        prompt_add_movie()
    elif user_input == "2":
        #  View upcoming movies.
        movies = database.get_movies(True)
        if movies:
            print_movie_list("Upcoming movies", movies)
        else:
            print("No upcoming movies.")
    elif user_input == "3":
        # View all movies.
        movies = database.get_movies()
        print_movie_list("All movies in db", movies)
    elif user_input == "4":
        # Watch a movie.
        prompt_watch_movie()
    elif user_input == "5":
        # View watched movies for a particular user.
        prompt_show_watched_movies()
    elif user_input == "6":
        # Add a new user.
        prompt_add_user()
    elif user_input == "7":
        #  7) Search for a movie.
        prompt_search_movies()
    elif user_input == "u":
        # show users
        _show_users()
    elif user_input == "f":
        # find users
        _find_user()
    else:
        print("Invalid option. Please choose again!")
