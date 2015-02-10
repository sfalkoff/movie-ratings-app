import model
import csv

def load_users(session):
    # use u.user: 1|24|M|technician|85711
    src_file = open("seed_data/u.user")

    for line in src_file:
        line = line.strip()
        id, age, gender, position, zipcode = line.split("|")
        # make a user instance w relevant above data
        new_user = model.User(age = age, zipcode = zipcode)
        new_user.id = id
        # add new instance to session
        session.add(new_user)

    #commit
    session.commit()


def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
