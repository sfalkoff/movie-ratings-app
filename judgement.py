from flask import Flask, render_template, redirect, request, flash
from flask import session as flask_session
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/users")
def userlist():
    user_list = model.User.query.limit(5).all()
    return render_template("user_list.html", users = user_list)

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
        print user_ratings[item].movie
        
    # pass dict to jinja to do own forloop to make a list
    print ur_dict
    return render_template("user_ratings.html", ur_dict = ur_dict)

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