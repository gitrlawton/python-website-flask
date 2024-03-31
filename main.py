from flask import Flask
from flask import redirect, url_for
from flask import render_template, request
from flask import session
# Used to create time-based, permanent sessions.
from datetime import timedelta
# Allows us to use message flashing (notifying the user the result of an action.)
from flask import flash

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# All the session data is encrypted, so we need to use a secret key to decrypt it.
app.secret_key = "hello"
# users is the name of the table we will be referencing.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session data is temporary storage on the server by default, meaning if you close
# your browser, it will be deleted. There is such a thing as permanent sessions.
# This sets the amount of time to keep permanent session data.
app.permanent_session_lifetime = timedelta(days=3)
# Intiialize our database as db.
db = SQLAlchemy(app)

# Database model.
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    # What we need to create a new user: name and email.
    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    # Grab all of the objects in the users table and pass them to view.html.
    return render_template("view.html", values=users.query.all())

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
        # Query and grab information from the database, using filter_by to 
        # search the database according to the 'name' property.
        # If a user with the name of the user exists in the database, it will
        # return the first one.  otherwise, found_user will be 'None'.
        found_user = users.query.filter_by(name=user).first()
        # If found_user is not None...
        if found_user:
            # Store the user's email in the session under the key 'email'.
            session["email"] = found_user.email
        # Otherwiser, user doesn't exist already (it is a new user.)
        else:
            # Create a new user with the user constructor.  Pass it the user
            # and an empty string for its email.
            usr = users(user, "")
            # Add and commit changes to database.
            db.session.add(usr)
            db.session.commit()
            
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

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    # Getting the user information from the session.
    # Check to see if there is a user stored in the session.
    if "user" in session:
        # If so, initialize a variable with the value stored in the session.
        user = session["user"]
        # Check if there was a POST request to the page (which in this case means 
        # the user typed an email address into the input box and clicked submit.)
        if request.method == "POST":
            # Extract the value for email from the form submission.
            email = request.form["email"]
            # Save the email to a key in the session data.
            session["email"] = email
            # Grab the user's name from the table of users.
            found_user = users.query.filter_by(name=user).first()
            # Set the email associated with the user to the email address they
            # just submitted via POST request.
            found_user.email = email
            # Commit the update to the database.
            db.session.commit()
            
            flash("Email was saved.")
        # Otherwise..
        else:
            # Check if there is an email stored in the session already.
            if "email" in session:
                email = session["email"]   
        # Render the user.html page and pass it our variable 'email'. 
        # Note: email will either be an email address, or None if no email
        # was found in session and it was a GET request.        
        return render_template("user.html", email=email)
    # Otherwise...
    else:
        # Let them know they are not logged in.
        flash("You are not logged in.")
        # Make them visit the login page.
        return redirect(url_for("login"))
    
# Function to handle user logging out.
@app.route("/logout")
def logout():
    # If user was logged in...
    if "user" in session:
        user = session["user"]
        # Flash a message to let user know they logged out.  The second arg, 
        # "info", is a categorization for the message.
        flash("You have been logged out", "info")
        
    # Remove the session data for the user.
    session.pop("user", None)
    session.pop("email", None)
    # Redirect to login page.
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Creates the database.  Make sure it only runs once.  Then, comment it out.
    #db.create_all()
    app.run(debug=True)