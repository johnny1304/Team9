from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask( __name__ )
app.config['SECRET_KEY'] = 'Authorised Personnel Only.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'database directory' #set the database directory
Bootstrap( app )
db = SQLAlchemy( app )
login_manager = LoginManager()
login_manager.init_app( app )
login_manager.login_view = 'login'

class User( UserMixin, db.Model ):
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
	#prefix? radio button?
	#age?

@app.route('/')
def index():
	return render_template("index.html") #directs to the index.html

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm() #create login form here

	if form.validate_on_submit(): #if login form is submitted then
		user = User() #check if the user is in the database
		#if the check password function terminates and returns True, then
		if check_password_hash(user.password, form.password.data):
			#logs in the user using flask login_user() function and
			#pass the remember_me boolean parameter from the form
			login_user(user, remember=form.remember.data)
			#redirect the user to the dashboard after logging in
			return redirect(url_for('dashboard'))
		else:
			return #error stating the password is incorrect
	else:
		return #error stating the user doesn't exist
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm() #create register form here

	if form.validate_on_submit(): #if register form is submitted then
		#hash the password
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		#create a new user for the database
		new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, 
			email=form.email.data, password=hashed_password)
		#add the new user to the database
		db.session.add(new_user)
		#commit the changes to the database
		db.session.commit()

		return #a page that acknowledges the user has been created
	return render_template('signup.html', form=form) # return the signup html page

@app.route('/dashboard')
@login_required
def dashboard():
	#return the dashboard html file with the user passed to it
	return render_template('dashboard.html', user=current_user)

#@app.route('/edit')
#@login_required
	

#@app.route('/resetpassword')
#@login_required


@app.route('/logout')
@login_required
def logout():
	logout_user() #logs the user out
	return redirect(url_for('index')) #or return a log out page

if __name__ == "__main__":
	app.run(debug=True)