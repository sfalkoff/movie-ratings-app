from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

#TODO: write appropriate __repr__ functions for each class

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)

class Movie(Base):
    __tablename__="movies"
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(400), nullable = True)
    #This last column has string release years, may want to change into datetime later, may not even need
    release_year = Column(String(4), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)


def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
