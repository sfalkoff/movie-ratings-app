from flask import Flask, g, render_template, redirect, request, flash
from flask import session as flask_session
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.before_request
def before_request():
    if 'email' in flask_session:
        g.user = flask_session['email']
    else:
        g.user = 'and welcome!'

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/users")
def userlist():
    user_list = model.User.query.limit(5).all()
    return render_template("user_list.html", users = user_list)

@app.route("/movies/<int:id>")
def movie_details(id):
    #database query for user's ratings
    movie = model.Movie.query.get(id)
    movie.name, movie.release_year, movie.imdb_url

    # IF has rating, show rating, allow edits
    if 'email' in flask_session:
        user = model.User.query.filter_by(email =flask_session['email']).one()
        user_id = user.id
        my_rating = model.Rating.query.filter(model.Rating.movie_id == id, model.Rating.user_id == user_id).first()
        print my_rating
        print my_rating.rating
        # if my_rating != None:
        #     #let me edit my rating
        # else:
        #     #let me create a rating

    return render_template("movie_ratings.html", name = movie.name, year = movie.release_year, imdb = movie.imdb_url)


@app.route("/ratings/<int:id>")
def ratings(id):
    #database query for user's ratings
    user = model.User.query.get(id)
    user_ratings = user.ratings
    ur_dict = {}

    #make for loop iterate over list of movie id's in user_ratings
    for item in range(len(user_ratings)):
        title = user_ratings[item].movie.name
        ur_dict[title] = user_ratings[item].rating

    return render_template("user_ratings.html", ur_dict = ur_dict)

@app.route("/movies")
def movie_list():
    movie_list = model.Movie.query.limit(5).all()
    return render_template("movie_list.html", movie_list = movie_list)

@app.route("/login", methods =["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods =["POST"])
def process_login():
    email = request.form['email']
    password = request.form['password']    

    user = model.User.query.filter(model.User.email==email).first()
 
    if user != None:
        if user.email == email and user.password == password:
            flask_session['email'] = email
            flash("Hello! Login successful.")
            print flask_session
            return redirect("/")
        else:
            flash("Incorrect password! Try again.")
            print flask_session
            return redirect("/login")

    else: 
        flash("You aren't in our database, want to sign up?")
        return redirect("/signup")

@app.route("/logout", methods=["GET"])
def log_out():
    flask_session.clear()
    flash("You are successfully logged out!")
    return redirect("/")


@app.route("/signup", methods=["GET"])
def signup():
    #presents a form template that gets user info
    return render_template("signup.html")
    
@app.route("/signup", methods=["POST"])
def process_signup():
    #FIXME on signup.html form for validation
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    zipcode = request.form["zipcode"]

    new_user = model.User(email = email, password = password, age = age, zipcode = zipcode)

    model.session.add(new_user)
    model.session.commit()

    flash("Welcome! You're all signed up.")
    return redirect("/")
    # return render_template("test.html", email = email, password = password, age = age, zipcode = zipcode)

if __name__ == "__main__":
    app.run(debug = True)