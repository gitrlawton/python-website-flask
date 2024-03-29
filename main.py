from flask import Flask
from flask import redirect, url_for
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    # Check if themethod used was POST.
    if request.method == "POST":
        # If so, data was sent.  Extract the user's name from the form data.
        user = request.form["nm"]
        # Redirect page to the user route, passing it the user's name.
        return redirect(url_for("user", usr=user))
    else:
        # Otherwise, it was a GET request so stay on login page.
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)