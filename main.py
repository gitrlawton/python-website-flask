from flask import Flask
from flask import redirect, url_for
from flask import render_template, request
from flask import session
# Used to create time-based, permanent sessions.
from datetime import timedelta
# Allows us to use message flashing (notifying the user the result of an action.)
from flask import flash

app = Flask(__name__)
# All the session data is encrypted, so we need to use a secret key to decrypt it.
app.secret_key = "hello"

# Session data is temporary storage on the server by default, meaning if you close
# your browser, it will be deleted. There is such a thing as permanent sessions.
# This sets the amount of time to keep permanent session data.
app.permanent_session_lifetime = timedelta(days=3)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    # Check if the method used was POST.  If so...
    if request.method == "POST":
        # Establish our session as permanent, adhering to the lifetime
        # set above.
        session.permanent = True
        # Since the method was POST, data was sent.  Extract the user's name 
        # from the form data.
        user = request.form["nm"]
        # Store the user data in our session, under the key "user".
        # Note: Sessions store data in a dictionary.
        session["user"] = user
        # Flash message to let them know they logged in.
        flash("Login successful.")
        # Redirect page to the user route, passing it the user's name.
        return redirect(url_for("user"))
    # Otherwise...
    else:
        # If the user is already logged in...
        if "user" in session:
            # Let them know they're already logged in.
            flash("Already logged in.")
            # Take them to the user page.
            return redirect(url_for("user"))
        # Otherwise, show them the login page.
        else:
            return render_template("login.html")

@app.route("/user")
def user():
    # Getting the user information from the session.
    # Check to see if there is a user stored in the session.
    if "user" in session:
        # If so, initialize a variable with the value stored in the session.
        user = session["user"]
        return render_template("user.html", user=user)
    # Otherwise...
    else:
        # Let them know they are not logged in.
        flash("You are not logged in.")
        # Make them visit the login page.
        return redirect(url_for("login"))
    
# Function to handle user logging out.
@app.route("logout")
def logout():
    # If user was logged in...
    if "user" in session:
        user = session["user"]
        # Flash a message to let user know they logged out.  The second arg, 
        # "info", is a categorization for the message.
        flash("You have been logged out", "info")
        
    # Remove the session data for the user.
    session.pop("user", None)
    # Redirect to login page.
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)