import model
import csv
from datetime import datetime

def load_users(session):
    src_file = open("seed_data/u.user")

    for line in src_file:
        line = line.strip()
        id, age, gender, position, zipcode = line.split("|")
        # make a user instance w relevant above data
        new_user = model.User(age = age, zipcode = zipcode)
        new_user.id = id
        # add new instance to session
        session.add(new_user)

    session.commit()


def load_movies(session):
    with open("seed_data/u.item", 'rb') as src_file:
        reader = csv.reader(src_file, delimiter="|")
        
        for row in reader:
            id = row[0]
            name_str = row[1]

            # decodes latin-1 back into unicode
            name_str = name_str.decode("latin-1")

            # only add movies with title and associated info to db
            if name_str != "unknown":
                # remove year from movie name title
                name = name_str[0:-7]
                str_released_at = row[2]

                # change string to datetime object
                released_at = datetime.strptime(str_released_at, "%d-%b-%Y")
                imdb_url = row[4] 

                #instantiate movie object
                movie = model.Movie(name = name, released_at = released_at, imdb_url=imdb_url)
                movie.id = id
    
                session.add(movie)

        session.commit()

def load_ratings(session):
    with open("seed_data/u.data", 'rb') as src_file:
        reader = csv.reader(src_file, delimiter="\t")
        
        for row in reader:
            user_id, movie_id, rating, timestamp = row
            user_rating = model.Rating(user_id = user_id, movie_id = movie_id, rating = rating)
            session.add(user_rating)

        session.commit()
               

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)


if __name__ == "__main__":
    s = model.connect()
    main(s)
