from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime


# Create a Flask instance.
app = Flask(__name__)
# Add a secret key.
app.config["SECRET_KEY"] = "MY super secret key"
# Connect to a database.
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
# Get rid of SQLALCHEMY_TRACK_MODIFICATIONS warning.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create db Instance.
db = SQLAlchemy(app)


# Create the login manager.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Create a Users class.
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(), unique=True)
    date_added = db.Column(db.String())


# Create Login Form.
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log In")


# Create Registration Form.
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid E-mail!")])
    date_added = str(datetime.now()).split(".")[0]
    signup = SubmitField("Register")



# Create index route.
@app.route("/")
def index():
    return render_template("index.html")

# Create admin route.
@app.route("/admin")
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry only admins can access admin page.")
        return redirect((url_for("dashboard")))

# Create login route.
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("Logged in successfully!")
                return redirect(url_for('dashboard'))
        flash(f"Invalid username or password.")
        # return "<h1>" + form.username.data + " " + form.password.data + "</h>"
    return render_template("login.html",
                           form=form)

# Create a sign up route.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data,
                         email=form.email.data,
                         password=hashed_password,
                         date_added=form.date_added)
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{form.username.data}' has been successfully created.")
        # return "<h1>"+ form.username.data + " " + form.password.data + " " + form.email.data + "</h>"

    return render_template("signup.html",
                           form=form)

# Create a login manager function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create a dashboard route.
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",
                           name=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)