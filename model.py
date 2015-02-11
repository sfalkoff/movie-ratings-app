from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

ENGINE = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable = True)

    def __repr__(self):
        return "<User: id=%r email=%s pass=%s age=%d zip=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)

class Movie(Base):
    __tablename__="movies"
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(400), nullable = True)
    #This last column has string release years, may want to change into datetime later, may not even need
    release_year = Column(Integer, nullable = True)

    def __repr__(self):
        return "<Movie: id=%r name=%s release_year=%d>" % (self.id, self.name, self.release_year)


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable = True)

    movie = relationship('Movie', backref=backref('ratings', order_by=id))

    user = relationship("User", backref=backref('ratings', order_by=id))

    def __repr__(self):
        return "<Rating: id=%r movie_id=%d user_id=%d rating=%d>" % (self.id, self.movie_id, self.user_id, self.rating)

def connect():
    pass
### End class declarations

def main():
    """In case we need this for something"""
    pass


if __name__ == "__main__":
    main()
