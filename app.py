from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Authorised Personnel Only.'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://seintu:0mYkNrVI0avq@mysql.netsoc.co/seintu_project'  # set the database directory
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

#setup for proposal call form
app.config["MYSQL_HOST"] = "mysql.netsoc.co"
app.config["MYSQL_USER"] = "seintu"
app.config["MYSQL_PASSWORD"] = "0mYkNrVI0avq"
app.config["MYSQL_DB"] = "seintu_project"
mysql = MySQL(app)
mysql.init_app(app)

class proposalForm(FlaskForm):
    start_date = DateField('Start Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    funding_amount = IntegerField('Funding Amount', validators=[InputRequired()], render_kw={"placeholder": "Amount"})
    funding_body = StringField('Funding Body', validators=[InputRequired()], render_kw={"placeholder": "Funding Body"})
    funding_programme = StringField('Funding Programme', validators=[InputRequired()], render_kw={"placeholder": "Funding Programme"})
    status = StringField('Status', validators=[InputRequired()], render_kw={"placeholder": "Active/Inactive"})
    primary_attribution = StringField('Primary Attribution', validators=[InputRequired()], render_kw={"placeholder": "Primary Attribution"})
    submit = SubmitField('Submit')

class Funding(db.Model):
    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date, nullable=False)
    FundingAmount = db.Column(db.Integer, nullable=False)

    FundingProgramme = db.Column(db.String(255), nullable=False)
    Stats = db.Column(db.String(255), nullable=False)
    PrimaryAttribution = db.Column(db.String(255), nullable=False, primary_key=True)
    ORCID =db.Column(db.String(255), nullable=False)

    def __init__(self, Start, End, Amount, Programme, status, PrimaryAttribution, ORCID):
        self.StartDate = Start
        self.EndDate = End
        self.FundingAmount = Amount

        self.FundingProgramme = Programme
        self.Stats = status
        self.PrimaryAttribution = PrimaryAttribution
        self.ORCID = ORCID

    def __repr__(self):
        return f"User('{self.StartDate}', '{self.FundingProgramme}', '{self.FundingAmount}')"

# standard set up for the Flask app

class User(UserMixin, db.Model):
    # this is the user login class that corresponds to the database
    __tablename__ = 'Researcher'  # the table name in the database is called Researcher
    # the following variables correspond to the columns in the Researcher table
    orcid = db.Column('orcid', db.Integer, primary_key=True, unique=True)
    first_name = db.Column('FirstName', db.String(20))
    last_name = db.Column('LastName', db.String(20))
    email = db.Column('email', db.String(50), unique=True)
    password = db.Column('password', db.String(80))
    job = db.Column('job', db.String(255))
    prefix = db.Column('prefix', db.String(20))
    suffix = db.Column('suffix', db.String(20))
    phone = db.Column('phone', db.Integer)
    phone_extension = db.Column('PhoneExtension', db.Integer)

    def __init__(self, orcid, first_name, last_name, email, password, job, prefix, suffix, phone, phone_extension):
        # this initialises the class and maps the variables to the table (done by flask automatically)
        self.orcid = orcid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.job = job
        self.prefix = prefix
        self.suffix = suffix
        self.phone = phone
        self.phone_extension = phone_extension

    def get_id(self):
        # this overrides the method get_id() so that it returns the orcid instead of the default id attribute in UserMixIn
        return self.orcid


# Below are the form classes that inherit the FlaskForm class.
# You can set the requirements for each attribute here instead of doing it in the html file
class LoginForm(FlaskForm):
    # this is the class for the login form in the sign_in.html
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
	#this is the class for the register form in the sign_up.html
	orcid = IntegerField('ORCID:', validators=[InputRequired()])
	first_name = StringField('First Name:', validators=[InputRequired(), Length(max=20)])
	last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=20)])
	email = StringField('Email:', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
	password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)])
	job = StringField('Job: ', validators=[InputRequired(), Length(max=255)])
	prefix = StringField('Prefix: ', validators=[InputRequired(), Length(max=20)])
	suffix = StringField('Suffix: ', validators=[InputRequired(), Length(max=20)])
	phone = IntegerField('Phone: ')
	phone_extension = IntegerField('Phone Extension: ')


@login_manager.user_loader
def load_user(user_id):
    # this is a function that callsback the user by the user_id
    return User.query.get(int(user_id))

def mail(content="", email="", password=""):
    #function provides default content message, sender's email, and password but accepts
    #them as parameters if given
    #for now it sends an email to all researchers(i hope) not sure how im supposed to narrow it down yet
    cur = mysql.get_db().cursor()
    cur.execute("SELECT email FROM researchers")
    rv = cur.fetchall()
	
    if not content:
        content = "default text"
    if not email:
        email = "default email address"
    if not password:
        password = "default password"
	
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo() #not a typo do not fix thanks
    mail.starttls()
    mail.login(email,password)
    for email in rv:
	    mail.sendmail('sender(me)', 'receiver', content)
    mail.close()

@app.route('/')
@app.route('/home')
def index():
    # this route returns the home.html file
    return render_template("/home.html")  # directs to the index.html


@app.route('/sign_in', methods=['GET', 'POST'])
def signin():
    # this is the login in route
    form = LoginForm()  # create login form here

    if form.validate_on_submit():  # if login form is submitted then
        user = User.query.filter_by(email=form.email.data).first()  # get user from the database
        if not user or not check_password_hash(user.password, form.password.data):
            # if user doesn't exist or the password is incorrect
            flash('Please check your login details and try again!')  # show an error message
            return redirect(url_for('signin'))

        # else logs in the user
        login_user(user, remember=form.remember.data)
        # and redirect to the index page which will be the profile page once its done
        return redirect(url_for('index'))
    return render_template('sign_in.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()  # create register form here
    if request.method == 'POST':
        if form.is_submitted():
            print("submitted")

        if form.validate():
            print("valid")
    if form.validate_on_submit():
        print("here")# if register form is submitted then
        # hash the password
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # create a new user for the database
        user = User.query.filter_by(email=form.email.data).first()
        exist_orcid = User.query.filter_by(orcid=form.orcid.data).first()

        if not exist_orcid and not user:
            new_user = User(orcid=form.orcid.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, job=form.job.data, prefix=form.prefix.data, suffix=form.suffix.data,
                        phone=form.phone.data, phone_extension=form.phone_extension.data, password=hashed_password)
            # add the new user to the database
            db.session.add(new_user)
            # commit the changes to the database
            db.session.commit()
            return redirect(url_for('signin'))  # a page that acknowledges the user has been created

        if user:
            flash('This email has already been used', category="email")
        if exist_orcid:
            flash('This orcid has already been registered', category="orcid")
        
        return redirect(url_for('signup'))
    return render_template('sign_up.html', form=form, logged=False)  # return the signup html page


@app.route('/dashboard')
@login_required
def dashboard():
    # return the dashboard html file with the user passed to it
    return render_template('dashboard.html', user=current_user)


# @app.route('/edit')
# @login_required


# @app.route('/resetpassword')

@app.route('/proposal_call', methods=['GET', 'POST'])
@login_required
def proposal_call():
    #Creates proposal form
    form = proposalForm(request.form)
    print(form.errors)
    #checks if form is submitted by post
    if request.method == 'POST':
        if form.is_submitted():
            print("submitted")

        if form.validate():
            print("valid")

        print(form.errors)
        #if input validates pushes to db
        if form.validate_on_submit():
            flash("Successfully logged")
            Start = form.start_date.data
            print(Start)
            End = form.end_date.data
            Amount = form.funding_amount.data
            FundingBody = form.funding_body.data
            Programme = form.funding_programme.data
            status = form.status.data
            PrimaryAttribution = form.primary_attribution.data
            ORCID = "22222"

            conn = mysql.connect
            cur = conn.cursor()
            # execute a query
            cur.execute("""INSERT INTO Funding(StartDate, EndDate, AmountFunding, FundingBody, FundingProgramme, Stats, PrimaryAttribution, ORCID)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",(Start, End, Amount, FundingBody, Programme, status, PrimaryAttribution, ORCID))
            # rv contains the result of the execute
            conn.commit()
            cur.close()
            conn.close()
            #links to form creation
            return render_template('create_submission_form.html')
        return render_template('proposal_call.html', form=form)
    else:
        return render_template('proposal_call.html', form=form)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/sign_in?next=' + request.path)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # logs the user out
    return redirect(url_for('index'))  # or return a log out page


if __name__ == "__main__":
    app.run(debug=True)
