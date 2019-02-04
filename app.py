from flask import Flask, render_template, redirect, url_for, request, flash
from flaskext import mysql
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
import pymysql as db_er


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Authorised Personnel Only.'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://seintu:0mYkNrVI0avq@mysql.netsoc.co/seintu_project'  # set the database directory
app.config["MYSQL_HOST"] = "mysql.netsoc.co"
app.config["MYSQL_USER"] = "seintu"
app.config["MYSQL_PASSWORD"] = "0mYkNrVI0avq"
app.config["MYSQL_DB"] = "seintu_project"
mysql = MySQL()
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mysql.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name:', validators=[InputRequired(), Length(max=20)])
    last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email:', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)])


# prefix? radio button?
# age?

class proposalForm(FlaskForm):
    start_date = DateField('Start Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    funding_amount = IntegerField('Funding Amount', validators=[InputRequired()], render_kw={"placeholder": "Amount"})
    funding_body = StringField('Funding Body', validators=[InputRequired()], render_kw={"placeholder": "Funding Body"})
    funding_programme = StringField('Funding Programme', validators=[InputRequired()], render_kw={"placeholder": "Funding Programme"})
    status = StringField('Status', validators=[InputRequired()], render_kw={"placeholder": "Active/Inactive"})
    primary_attribution = StringField('Primary Attribution', validators=[InputRequired()], render_kw={"placeholder": "Primary Attribution"})
    submit = SubmitField('Submit')




@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")  # directs to the index.html


@app.route('/sign_in', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # create login form here

    if form.validate_on_submit():  # if login form is submitted then
        user = User()  # check if the user is in the database
        # if the check password function terminates and returns True, then
        if check_password_hash(user.password, form.password.data):
            # logs in the user using flask login_user() function and
            # pass the remember_me boolean parameter from the form
            login_user(user, remember=form.remember.data)
            # redirect the user to the dashboard after logging in
            return redirect(url_for('dashboard'))
        else:
            return  # error stating the password is incorrect
    else:
        return render_template('sign_in.html', form=form)
    return render_template('sign_in.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()  # create register form here

    if form.validate_on_submit():  # if register form is submitted then
        # hash the password
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # create a new user for the database
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, password=hashed_password)
        # add the new user to the database
        db.session.add(new_user)
        # commit the changes to the database
        db.session.commit()

        return  # a page that acknowledges the user has been created
    return render_template('sign_up.html', form=form)  # return the signup html page


@app.route('/dashboard')
@login_required
def dashboard():
    # return the dashboard html file with the user passed to it
    return render_template('dashboard.html', user=current_user)


# @app.route('/edit')
# @login_required


# @app.route('/resetpassword')
# @login_required

# Proposal call form submission and reroute
@app.route('/proposal_call', methods=['GET', 'POST'])
def proposal_call():
    form = proposalForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        if form.is_submitted():
            print("submitted")

        if form.validate():
            print("valid")

        print(form.errors)

        if form.validate_on_submit():
            flash("Successfully logged")
            Start = form.start_date.data
            print(Start)
            End = form.end_date.data
            Amount = form.funding_amount.data
            Body = form.funding_body.data
            Programme = form.funding_programme.data
            status = form.status.data
            PrimaryAttribution = form.primary_attribution.data
            ORCID = "22222"
            #prop = proposalDB(Start,End,Amount,Body,Programme,status,PrimaryAttribution,ORCID)
            # make a connection
            #db.session.add(prop)

            cur = mysql.connection.cursor()
            # execute a query
            cur.execute("""INSERT INTO Funding (StartDate, EndDate, AmountFunding, FundingBody, FundingProgramme, Stats, PrimaryAttribution, ORCID)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""%(Start, End, Amount, Body, Programme, status, PrimaryAttribution, ORCID))
            # rv contains the result of the execute
            rv = cur.fetchall()
            return str(rv)


        return render_template('proposal_call.html', form=form)
    else:
        return render_template('proposal_call.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # logs the user out
    return redirect(url_for('index'))  # or return a log out page


if __name__ == "__main__":
    app.run(debug=True)