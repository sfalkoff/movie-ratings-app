from flask import Flask, render_template, redirect, request
import model
app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.User.query.all()
    return render_template("user_list.html", users = user_list)

if __name__ == "__main__":
    app.run(debug = True)