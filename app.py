import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_mail import Message, Mail
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime


# Create a Mail instance.
mail = Mail()
# Create a Flask instance.
app = Flask(__name__)
# Add a secret key.
app.config["SECRET_KEY"] = "MY super secret key"
# Connect to a database.
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
# Get rid of SQLALCHEMY_TRACK_MODIFICATIONS warning.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set up the mail server.
app.config["MAIL_SERVER"] = "smtp.gmail.com"
# Set up a mail port.
app.config["MAIL_PORT"] = 465
# Encript data using SSL.
app.config["MAIL_USE_SSL"] = True
# Set up where to send the e-mail.
app.config["MAIL_USERNAME"] = os.environ.get("GMAIL")
# E-mail password.
app.config["MAIL_PASSWORD"] = os.environ.get("GMAIL_PW")
# Initialize mail.
mail.init_app(app)
# Create db Instance.
db = SQLAlchemy(app)


# Create the login manager.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Create Users table.
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(200))
    age = db.Column(db.Integer())
    location = db.Column(db.String())
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
    full_name = StringField("Full Name", validators=[InputRequired()])
    age = StringField("Your age", validators=[InputRequired()])
    location = StringField("Country", validators=[InputRequired()])
    username = StringField("Username(Nickname) - You will need this to log in", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid E-mail!")])
    date_added = str(datetime.now()).split(".")[0]
    signup = SubmitField("Register")


# Create a UserUpdate form.
class UserEdit(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    age = StringField("Your age", validators=[InputRequired()])
    location = StringField("Country", validators=[InputRequired()])
    username = StringField("Username(Nickname)",
                           validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid E-mail!")])
    edit = SubmitField("Update Profile")
    edit = SubmitField("Delete Profile")



# Create Products table.
class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    category = db.Column(db.String(200))
    origin = db.Column(db.String(200))
    price = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date_added = db.Column(db.String())



# Create AddProduct form.
class AddProduct(FlaskForm):
    product_name = StringField("Product Name", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    category = StringField("Category", validators=[InputRequired()])
    origin = StringField("Made In", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    image = StringField("Image source", validators=[InputRequired()])
    date_added = str(datetime.now()).split(".")[0]
    submit = SubmitField("Add Product")



# Create EditProducts form.
class EditProduct(FlaskForm):
    product_name = StringField("Product Name", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    category = StringField("Category", validators=[InputRequired()])
    origin = StringField("Made In", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    image = StringField("Image source", validators=[InputRequired()])
    edit = SubmitField("Update Product")
    edit = SubmitField("Delete Product")


# Create a Contact Us form.
class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[InputRequired()])
    email = StringField("Your E-mail", validators=[InputRequired(), Email(message="Invalid e-mail address!")])
    subject = StringField("Subject")
    message = TextAreaField("Your message")
    submit = SubmitField("Send message")

# Creating a global variable to make it easier to maintain admins.
admins = [1]

# Create index route.
@app.route("/")
def index():
    return render_template("index.html")

# Create admin route.
@app.route("/admin")
@login_required
def admin():
    all_users = Users.query.order_by(Users.date_added)
    if current_user.id in admins:
        return render_template("admin.html",
                               all_users=all_users)
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
        else:
            flash(f"Invalid username or password.")
    return render_template("login.html",
                           form=form)

# Create a sign up route.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        mail = Users.query.filter_by(email=form.email.data).first()
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        if user:
            flash(f"Username '{form.username.data}' already exists.")
        if mail:
            flash(f"E-mail address '{form.email.data}' is already asociated to another user.")
        else:
            new_user = Users(full_name=form.full_name.data,
                             age=form.age.data,
                             location=form.location.data,
                             username=form.username.data,
                             email=form.email.data,
                             password=hashed_password,
                             date_added=form.date_added)

            db.session.add(new_user)
            db.session.commit()
            flash(f"User '{form.username.data}' has been successfully created. Go to the login page.")
    return render_template("signup.html",
                           form=form)

# Create a login manager function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create a dashboard route.
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UserEdit()
    id = current_user.id
    to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        if request.form["edit"] == "Update Profile":
            to_update.full_name = request.form["full_name"]
            to_update.age = request.form["age"]
            to_update.location = request.form["location"]
            to_update.username = request.form["username"]
            to_update.email = request.form["email"]
            try:
                db.session.commit()
                flash("User profile updated successfully!")
                return render_template("dashboard.html",
                                       current_user=current_user,
                                       to_update=to_update,
                                       admins=admins,
                                       form=form)
            except:
                flash("Oops! Something went wrong! Try again!")
                return render_template("dashboard.html",
                                       current_user=current_user,
                                       to_update=to_update,
                                       admins=admins,
                                       form=form)
        if request.form["edit"] == "Delete Profile":
            try:
                db.session.delete(to_update)
                db.session.commit()
                return redirect(url_for("index"))
            except:
                flash("Oops! Something went wrong. Try again.")
    return render_template("dashboard.html",
                           current_user=current_user,
                           to_update=to_update,
                           admins=admins,
                           form=form)


@app.route("/admin_user_edit/<int:id>", methods = ["GET", "POST"])
@login_required
def admin_user_edit(id):
    form = UserEdit()
    all_users = Users.query.order_by(Users.date_added)
    to_update = Users.query.get_or_404(id)
    if current_user.id in admins:
        if request.method == "POST":
            if request.form["edit"] == "Update Profile":
                to_update.full_name = request.form["full_name"]
                to_update.age = request.form["age"]
                to_update.location = request.form["location"]
                to_update.username = request.form["username"]
                to_update.email = request.form["email"]
                try:
                    db.session.commit()
                    flash("User profile updated successfully!")
                    return render_template("admin_user_edit.html",
                                           current_user=current_user,
                                           to_update=to_update,
                                           all_users=all_users,
                                           id=id,
                                           form=form)
                except:
                    flash("Oops! Something went wrong! Try again!")
                    return render_template("admin_user_edit.html",
                                           current_user=current_user,
                                           to_update=to_update,
                                           all_users=all_users,
                                           id=id,
                                           form=form)
            if request.form["edit"] == "Delete Profile":
                try:
                    db.session.delete(to_update)
                    db.session.commit()
                    return redirect(url_for("admin"))
                except:
                    flash("Oops! Something went wrong. Try again.")
        return render_template("admin_user_edit.html",
                               current_user=current_user,
                               to_update=to_update,
                               all_users=all_users,
                               id=id,
                               form=form)
    else:
        flash("You are not authorized to see this page.")
        return redirect("index")


@app.route("/products", methods=["GET", "POST"])
@login_required
def admin_products():
    all_products = Products.query.order_by(Products.date_added)
    if current_user.id in admins:
        return render_template("admin_products.html",
                               all_products=all_products)
    else:
        flash("You are not authorized to see this page.")
        return redirect("index")



@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    form = AddProduct()
    if current_user.id in admins:
        if form.validate_on_submit():
            new_product = Products(product_name=form.product_name.data,
                                   description=form.description.data,
                                   category=form.category.data,
                                   origin=form.origin.data,
                                   price=form.price.data,
                                   image=form.image.data,
                                   date_added=form.date_added)
            db.session.add(new_product)
            db.session.commit()
            flash(f"Product '{form.product_name.data}' has been successfully added.")

        else:
            return render_template("add_product.html",
                        form=form)

        return render_template("add_product.html",
                               form=form)
    else:
        flash("You are not authorized to see this page. Only admins can add products.")
        return redirect(url_for("dashboard"))

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    form = EditProduct()
    all_products = Products.query.order_by(Products.date_added)
    to_edit = Products.query.get_or_404(id)
    if current_user.id in admins:
        if request.method == "POST":
            if request.form["edit"] == "Update Product":
                to_edit.product_name = request.form["product_name"]
                to_edit.description = request.form["description"]
                to_edit.category = request.form["category"]
                to_edit.origin = request.form["origin"]
                to_edit.price = request.form["price"]
                to_edit.image = request.form["image"]
                try:
                    db.session.commit()
                    flash("Product updated successfully!")
                    return render_template("edit_product.html",
                                           to_edit=to_edit,
                                           all_products=all_products,
                                           id=id,
                                           form=form)
                except:
                    flash("Oops! Something went wrong. Try again!")
                    return render_template("admin_products.html",
                                           to_edit=to_edit,
                                           all_products=all_products,
                                           id=id,
                                           form=form)
            if request.form["edit"] == "Delete Product":
                try:
                    db.session.delete(to_edit)
                    db.session.commit()
                    flash("Product deleted successfully!")
                    return redirect(url_for("admin_products"))
                except:
                    flash("Oops! Something went wrong. Try again!")
        return render_template("edit_product.html",
                               to_edit=to_edit,
                               all_products=all_products,
                               id=id,
                               form=form)
    else:
        flash("You are not authorized to see this page. Only admins can edit products.")
        return redirect(url_for("dashboard"))


@app.route("/user_products")
@login_required
def user_products():
    all_products = Products.query.filter(Products.id)
    return render_template("user_products.html",
                               all_products=all_products)



@app.route("/product_details/<int:id>", methods=["GET", "POST"])
@login_required
def product_details(id):
    all_products = Products.query.filter(Products.id)
    to_display = Products.query.get_or_404(id)
    return render_template("product_details.html",
                           all_products=all_products,
                           to_display=to_display)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    form = ContactForm()
    if request.method == "POST":
        msg = Message(form.subject.data, sender="Market Online", recipients=["adicotuna26@gmail.com"])
        msg.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
        flash("Message sent successfully!")
        return render_template("contact.html",
                               form=form)
    elif request.method == "GET":
        return render_template("contact.html",
                               form=form)




if __name__ == "__main__":
    app.run(debug=True)