import os
from pathlib import Path
import secrets
import uuid
from PIL import Image
from flask import Flask, render_template, redirect, url_for, flash, request,send_file,send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateField, SelectField, SubmitField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email, Length, length, DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_dropzone import Dropzone
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Authorised Personnel Only.'  # set the database directory
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/calvi/OneDrive/Documents/CS3305/Team9/test.db'
#app.config[
#    'SQLALCHEMY_DATABASE_URI'] = 'mysql://seintu:0mYkNrVI0avq@mysql.netsoc.co/seintu_project2'  # set the database directory
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

SQLALCHEMY_DATABASE_URI = "mysql://Johnnyos1304:netsoc101@Johnnyos1304.mysql.pythonanywhere-services.com/Johnnyos1304$project"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#setup for proposal call form
app.config["MYSQL_HOST"] = "Johnnyos1304.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "Johnnyos1304"
app.config["MYSQL_PASSWORD"] = "netsoc101"
app.config["MYSQL_DB"] = "Johnnyos1304$project"
mysql = MySQL(app)
mysql.init_app(app)



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
    type = db.Column('Type', db.String(20))
    education = db.relationship('Education', backref='Researcher')
    employment = db.relationship('Employment', backref='Researcher')
    societies = db.relationship('Societies', backref='Researcher')
    awards = db.relationship('Awards', backref='Researcher')
    funding = db.relationship('Funding', backref='Researcher')
    team_members = db.relationship('TeamMembers', backref='Researcher')
    impacts = db.relationship('Impacts', backref='Researcher')
    inno_and_comm = db.relationship('InnovationAndCommercialisation', backref='Researcher')
    publications = db.relationship('Publications', backref='Researcher')
    presentations = db.relationship('Presentations', backref='Researcher')
    collab = db.relationship('Collaborations', backref='Researcher')
    organised_events = db.relationship('OrganisedEvents', backref='Researcher')
    edu_and_public_engagement = db.relationship('EducationAndPublicEngagement', backref='Researcher')
    submission = db.relationship('Submissions', backref='Researcher')
    ExternalReview = db.relationship('ExternalReview',backref='Researcher')
    reports = db.relationship('Report', backref='Researcher')

    def __init__(self, orcid, first_name, last_name, email, password, job, prefix, suffix, phone, phone_extension, type):
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
        self.type = type

    def get_orcid(self):
        return self.orcid

    def get_id(self):
        # this overrides the method get_id() so that it returns the orcid instead of the default id attribute in UserMixIn
        return self.orcid

class Proposal(db.Model):
    __tablename__ = "Proposal"
    Deadline = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(100),nullable=False)
    TextOfCall = db.Column(db.String(1000), nullable=False)
    TargetAudience = db.Column(db.String(500), nullable=False)
    EligibilityCriteria = db.Column(db.String(1000), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    ReportingGuidelines = db.Column(db.String(1000), nullable=False)
    TimeFrame = db.Column(db.String(200), nullable=False)
    picture = db.Column(db.String(200),nullable=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    def __init__(self, Deadline, title, TextOfCall, TargetAudience, EligibilityCriteria, Duration, ReportingGuidelines, TimeFrame):
        self.Deadline = Deadline
        self.title = title
        self.TextOfCall = TextOfCall
        self.TargetAudience = TargetAudience
        self.EligibilityCriteria = EligibilityCriteria
        self.Duration = Duration
        self.ReportingGuidelines = ReportingGuidelines
        self.TimeFrame = TimeFrame

    def __repr__(self):
        return f"User('{self.Deadline}', '{self.TargetAudience}', '{self.TimeFrame}')"

class Submissions(db.Model):
    __tablename__='Submission'
    propid = db.Column(db.Integer,nullable=False)
    subid = db.Column(db.Integer,nullable=False, primary_key=True)
    title = db.Column(db.Text,nullable=False)
    duration = db.Column(db.Integer,nullable=False)
    NRP = db.Column(db.String(200),nullable=False)
    legal = db.Column(db.Text,nullable=False)
    ethicalAnimal = db.Column(db.Text,nullable=False)
    ethicalHuman = db.Column(db.Text,nullable=False)
    location = db.Column(db.Text,nullable=False)
    coapplicants = db.Column(db.Text,nullable=True)
    collaborators = db.Column(db.Text,nullable=True)
    scientific = db.Column(db.Text,nullable=False)
    lay = db.Column(db.Text,nullable=False)
    declaration = db.Column(db.Boolean,nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('Researcher.orcid') ,nullable=False)
    draft = db.Column(db.Boolean, nullable=False, default=True)
    proposalPDF = db.Column(db.String(255),nullable=False)
    status = db.Column(db.String(255), default="pending")
    reports = db.relationship('Report', backref="Submission")
    team = db.relationship('Team', backref="Submission")
    funding = db.relationship('Funding', backref="Submission")

    def __init__(self,propid,title,duration,NRP,legal,ethicalAnimal,ethicalHuman,location,coapplicants,collaborators,scientific,lay,declaration,user,proposalPDF):
        self.title=title
        self.propid=propid
        self.duration=duration
        self.NRP=NRP
        self.legal=legal
        self.ethicalAnimal=ethicalAnimal
        self.ethicalHuman=ethicalHuman
        self.location=location
        self.coapplicants=coapplicants
        self.collaborators=collaborators
        self.scientific=scientific
        self.lay=lay
        self.declaration=declaration
        self.user=user
        self.proposalPDF=proposalPDF
        self.draft=True


    def setDraftFalse(self):
        self.draft=False


class Funding(db.Model):
    __tablename__ = 'Funding'

    StartDate = db.Column(db.Date, nullable=False)
    EndDate = db.Column(db.Date, nullable=False)
    AmountFunding = db.Column(db.Integer, nullable=False)
    FundingBody = db.Column(db.String(255))
    FundingProgramme = db.Column(db.String(255), nullable=False)
    Stats = db.Column(db.String(255), nullable=False)
    PrimaryAttribution = db.Column(db.String(255), nullable=False)
    orcid = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'), nullable=False)
    subid = db.Column(db.Integer, db.ForeignKey('Submission.subid'), nullable=False)
    ID=db.Column(db.Integer, nullable=False, primary_key=True)

    def __init__(self,subid,StartDate, EndDate, AmountFunding, FundingBody, FundingProgramme, Stats, PrimaryAttribution, orcid):
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.AmountFunding = AmountFunding
        self.FundingBody = FundingBody
        self.FundingProgramme = FundingProgramme
        self.Stats = Stats
        self.PrimaryAttribution = PrimaryAttribution
        self.orcid = orcid
        self.subid=subid

    def __repr__(self):
        return f"User('{self.StartDate}', '{self.FundingProgramme}', '{self.AmountFunding}')"


class ExternalReview(db.Model):
    __tablename__="ExternalReview"
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    Submission=db.Column(db.Integer,db.ForeignKey('Submission.subid'),nullable=False)
    reviewer=db.Column(db.Integer,db.ForeignKey('Researcher.orcid'),nullable=False)
    Complete=db.Column(db.Boolean,default=False,nullable=False)
    review=db.Column(db.String(255),nullable=False)

    def __init__(self,Submission,reviewer,Complete,review):
        self.Submission=Submission
        self.reviewer=reviewer
        self.Complete=Complete
        self.review=review

class ExternalPendingReviews(db.Model):
    __tablename__="ExternalPendingReviews"
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    Submission = db.Column(db.Integer, db.ForeignKey('Submission.subid'), nullable=False)
    reviewer = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'), nullable=False)
    Complete = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self,Submission,reviewer,Complete):
        self.Submission=Submission
        self.reviewer=reviewer
        self.Complete=Complete


class Education(db.Model):
    __tablename__ = "Education"
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column('Degree', db.String(255))
    field = db.Column('Field', db.String(255))
    institution = db.Column('Institution', db.String(255))
    location = db.Column('Location', db.String(255))
    year = db.Column('Year', db.Integer)
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Employment(db.Model):
    __tablename__ = "Employment"
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column('Company', db.String(255))
    location = db.Column('Location', db.String(255))
    years = db.Column('Years', db.Integer)
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Societies(db.Model):
    __tablename__ = "Societies"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column('StartDate', db.Date)
    end_date = db.Column('EndDate', db.Date)
    society = db.Column('Society', db.String(255))
    membership = db.Column('Membership', db.String(255))
    status = db.Column('Status', db.String(20))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Awards(db.Model):
    __tablename__ = "Awards"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    award_body = db.Column('AwardingBody', db.String(255))
    details = db.Column('Details', db.String(255))
    team_member = db.Column('TeamMember', db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Team(db.Model):
    __tablename__ = "Team"
    team_id = db.Column("TeamID", db.Integer, primary_key=True)
    team_leader = db.Column("TeamLeader", db.Integer, db.ForeignKey('Researcher.orcid'))
    #change to sub id
    subid = db.Column("SubmissionID", db.Integer, db.ForeignKey('Submission.subid'))

class TeamMembers(db.Model):
    __tablename__ = "TeamMembers"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column("StartDate", db.Date)
    departure_date = db.Column("DepartureDate", db.Date)
    name = db.Column("Name", db.String(255))
    position = db.Column("position", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))
    team_id = db.Column(db.Integer, db.ForeignKey('Team.TeamID'))
    #subid = db.Column(db.Integer, nullable="False")

class Impacts(db.Model):
    __tablename__ = "Impacts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column("Title", db.String(255))
    category = db.Column("Category", db.String(255))
    primary_beneficiary = db.Column("PrimaryBeneficiary", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class InnovationAndCommercialisation(db.Model):
    __tablename__ = "InnovationAndCommercialisation"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column("Year", db.Integer)
    type = db.Column("Type", db.String(255))
    title = db.Column("Title", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255), nullable=False)
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Publications(db.Model):
    __tablename__ = "Publications"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column("Year", db.Integer)
    type = db.Column("Type", db.String(255))
    title = db.Column("Title", db.String(255))
    name = db.Column("Name", db.String(255))
    status = db.Column("Status", db.String(255))
    doi = db.Column("DOI", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Presentations(db.Model):
    __tablename__ = "Presentations"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column("Year", db.Integer)
    title = db.Column("Title", db.String(255))
    type = db.Column("Type", db.String(255))
    conference = db.Column("Conference", db.String(255))
    invited_seminar = db.Column("InvitedSeminar", db.String(255))
    keynote = db.Column("Keynote", db.String(255))
    organising_body = db.Column("OrganisingBody", db.String(255))
    location = db.Column("Location", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Collaborations(db.Model):
    __tablename__ = "Collaborations"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column("StartDate", db.Date)
    end_date = db.Column("EndDate", db.Date)
    institution = db.Column("Institution", db.String(255))
    department = db.Column("Department", db.String(255))
    location = db.Column("Location", db.String(255))
    name_collaborator = db.Column("NameCollaborator", db.String(255))
    primary_goal = db.Column("PrimaryGoal", db.String(255))
    frequency_of_interaction = db.Column("FrequencyOfInteraction", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    academic = db.Column("Academic", db.Boolean)
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class OrganisedEvents(db.Model):
    __tablename__ = "OrganisedEvents"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column("StartDate", db.Date)
    end_date = db.Column("EndDate", db.Date)
    title = db.Column("Title", db.String(255))
    type = db.Column("Type", db.String(255))
    role = db.Column("Role", db.String(255))
    location = db.Column("Location", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class EducationAndPublicEngagement(db.Model):
    __tablename__ = "EducationAndPublicEngagement"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(255))
    start_date = db.Column("StartDate", db.Date)
    end_date = db.Column("EndDate", db.Date)
    activity = db.Column("Activity", db.String(255))
    topic = db.Column("Topic", db.String(255))
    target_area = db.Column("TargetArea", db.String(255))
    primary_attribution = db.Column("PrimaryAttribution", db.String(255))
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))

class Report(db.Model):
    __tablename__ = "Report"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    pdf = db.Column(db.String(255))
    type = db.Column(db.String(255), nullable=False)
    ORCID = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'))
    subid = db.Column(db.Integer, db.ForeignKey('Submission.subid'), nullable="False")

# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------


# Below are the form classes that inherit the FlaskForm class.
# You can set the requirements for each attribute here instead of doing it in the html file
class LoginForm(FlaskForm):
    # this is the class for the login form in the sign_in.html
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    forgot = StringField("Forgot your password")

class ForgotForm(FlaskForm):
    email  = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email"),Length(max=50)])
    reEmail = StringField("Re-type Email", validators=[InputRequired(), Email(message="Invalid Email"),Length(max=50)])
    submit = SubmitField('Reset Password')


class ResetForm(FlaskForm):
    new = PasswordField("New Password", validators=[InputRequired(), Length(min=8,max=80), EqualTo('repeat', message='Passwords must match')])
    repeat = PasswordField("Re-type Password", validators=[InputRequired(), Length(min=8,max=80)])
    submit = SubmitField('Reset Password')

class UpdateInfoForm(FlaskForm):


    #this is the class for the register form in the sign_up.html
    first_name = StringField('First Name:'  , validators=[InputRequired(), Length(max=20)])
    last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email:', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    job = StringField('Job: ', validators=[InputRequired(), Length(max=255)])
    prefix = StringField('Prefix: ', validators=[InputRequired(), Length(max=20)])
    suffix = StringField('Suffix: ', validators=[InputRequired(), Length(max=20)])
    phone = IntegerField('Phone: ')
    phone_extension = IntegerField('Phone Extension: ')
    submit = SubmitField('Edit')


class RegisterForm(FlaskForm):
    #this is the class for the register form in the sign_up.html
    orcid = IntegerField('ORCID:', validators=[InputRequired()])
    first_name = StringField('First Name:', validators=[InputRequired(), Length(max=20)])
    last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email:', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')
    job = StringField('Job: ', validators=[InputRequired(), Length(max=255)])
    prefix = StringField('Prefix: ', validators=[InputRequired(), Length(max=20)])
    suffix = StringField('Suffix: ', validators=[InputRequired(), Length(max=20)])
    phone = IntegerField('Phone: ')
    phone_extension = IntegerField('Phone Extension: ')

class ManageForm(FlaskForm):
    researcher = SelectField("User")
    role = SelectField('Role: ', choices=[('Researcher','Researcher'),('Reviewer','Reviewer'),("Admin","Admin")])
    submit = SubmitField('Apply')


#form for form creations
class formCreationForm(FlaskForm):
    start_date = DateField('Start Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    funding_amount = IntegerField('Funding Amount', validators=[InputRequired()], render_kw={"placeholder": "Amount"})
    funding_body = StringField('Funding Body', validators=[InputRequired()], render_kw={"placeholder": "Funding Body"})
    funding_programme = StringField('Funding Programme', validators=[InputRequired()], render_kw={"placeholder": "Funding Programme"})
    status = StringField('Status', validators=[InputRequired()], render_kw={"placeholder": "Active/Inactive"})
    primary_attribution = StringField('Primary Attribution', validators=[InputRequired()], render_kw={"placeholder": "Primary Attribution"})
    submit = SubmitField('Submit')

class UpdateEducationForm(FlaskForm):
    idd = "edu"
    id = StringField('ID:', validators=[ Length(max=50)])
    degree = StringField('Degree:', validators=[ Length(max=50)])
    institution = StringField('Institution:', validators=[ Length(max=50)])
    location = StringField('Locations:', validators=[Length(max=50)])
    year = IntegerField('Year ' )
    field = StringField('Field:', validators=[ Length(max=50)])
    submit_edu = SubmitField('Edit Education')
    remove_edu = SubmitField('Remove')

class AddFundingForm(FlaskForm):
    start_date = DateField('Start Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    amount_funding = IntegerField('Amount Funding', )
    funding_body = StringField('Funding Body', validators=[ Length(max=50)] )
    funding_programme = StringField('Funding Programme ', validators=[ Length(max=50)])
    stats = StringField('Stats', validators=[ Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[ Length(max=50)])
    submit = SubmitField('Add')

class AddTeamForm(FlaskForm):
    team_id = StringField('Team ID' ,  validators=[ Length(max=50)] )
    team_leader = StringField('Team Leader' , validators=[ Length(max=50)] )
    proposal_id = StringField('Proposal ID' , validators=[ Length(max=50)] )
    submit = SubmitField('Add')

class AddEducationForm(FlaskForm):
    degree = StringField('Degree:', validators=[ Length(max=50)])
    institution = StringField('Institution:', validators=[ Length(max=50)])
    location = StringField('Locations:', validators=[Length(max=50)])
    year = IntegerField('Year ' )
    field = StringField('Field:', validators=[ Length(max=50)])
    submit = SubmitField('Add Education')

class AddPublications(FlaskForm):
    year = IntegerField("Year")
    type = StringField("Type", validators=[Length(max=50)])
    title = StringField("Title", validators=[Length(max=50)])
    name = StringField("Name", validators=[Length(max=50)])
    status = StringField("Status", validators=[Length(max=50)])
    doi = StringField("DOI",validators=[Length(max=50)])
    primary_attribution = StringField("PrimaryAttribution", validators=[Length(max=50)])
    submit = SubmitField('Add Publications')


class AddEmploymentForm(FlaskForm):
    company = StringField('Company:', validators=[ Length(max=50)])
    location = StringField('Location:', validators=[ Length(max=50)])
    years = IntegerField('Years:')
    submit = SubmitField('Add')

class UpdatePublications(FlaskForm):
    id = StringField("ID:" ,validators=[ Length(max=50)])
    year = IntegerField("Year")
    type = StringField("Type", validators=[Length(max=50)])
    title = StringField("Title", validators=[Length(max=50)])
    name = StringField("Name", validators=[Length(max=50)])
    status = StringField("Status", validators=[Length(max=50)])
    doi = StringField("DOI",validators=[Length(max=50)])
    primary_attribution = StringField("PrimaryAttribution", validators=[Length(max=50)])
    submit_pub = SubmitField('Edit Publications')
    remove_pub = SubmitField('Remove')

class UpdateEmploymentForm(FlaskForm):
    id = StringField('ID:', validators=[ Length(max=50)])
    company = StringField('Company:', validators=[ Length(max=50)])
    location = StringField('Location:', validators=[ Length(max=50)])
    years = IntegerField('Years:')
    submit_emp = SubmitField('Edit Employment')
    remove_emp = SubmitField('Remove')

class UpdateEducationAndPublicEngagement(FlaskForm):
    id = StringField('ID' ,validators=[ Length(max=50)])
    name = StringField('Name', validators=[Length(max=50)])
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    activity = StringField('Activity', validators=[Length(max=50)])
    topic = StringField('Topic', validators=[Length(max=50)])
    target_area = StringField('Target Area', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit_edup= SubmitField('Edit')
    remove_edup = SubmitField('Remove')


class UpdateFundingForm(FlaskForm):
    id = StringField('ID:', validators=[ Length(max=50)])
    start_date = DateField('Start Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    amount_funding = IntegerField('Amount Funding', )
    funding_body = StringField('Funding Body', validators=[ Length(max=50)] )
    funding_programme = StringField('Funding Programme ', validators=[ Length(max=50)])
    stats = StringField('Status', validators=[ Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[ Length(max=50)])
    submit_fund = SubmitField('Edit Funding')
    remove_fund = SubmitField('Remove')

class UpdateOrganisedEvents(FlaskForm):
    id = StringField('ID:', validators=[ Length(max=50)])
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    title = StringField('Title', validators=[Length(max=50)])
    type = StringField('Type', validators=[Length(max=50)])
    role = StringField('Role', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit_org = SubmitField('Edit')
    remove_org = SubmitField('Remove')

class UpdateImpactsForm(FlaskForm):
    id = StringField('ID:', validators=[Length(max=50)])
    title = StringField('Title: ', validators=[Length(max=50)])
    category = StringField('Category: ', validators=[Length(max=50)])
    primary_beneficiary = StringField('Primary Beneficiary: ', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution:', validators=[Length(max=50)])
    submit_imp = SubmitField('Edit')
    remove_imp = SubmitField('Remove')

class UpdatePresentations(FlaskForm):
    id = StringField('ID:', validators=[Length(max=50)])
    year = IntegerField('Year', )
    title = StringField('Title', validators=[Length(max=50)])
    type = StringField('Type', validators=[Length(max=50)])
    conference = StringField('Conference', validators=[Length(max=50)])
    invited_seminar = StringField('Invited Seminar', validators=[Length(max=50)])
    keynote = StringField('Keynote', validators=[Length(max=50)])
    organising_body = StringField('Organising Body', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution:' , validators=[Length(max=50)])
    submit_pres = SubmitField('Edit')
    remove_pres = SubmitField('Remove')

class UpdateCollaborations(FlaskForm):
    id = StringField('ID:', validators=[Length(max=50)])
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date =DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    institution = StringField('Institution', validators=[Length(max=50)])
    department = StringField('Department', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    name_collaborator = StringField('Name Colloaborator', validators=[Length(max=50)])
    primary_goal = StringField('Primary Goal',validators=[Length(max=50)] )
    frequency_of_interaction = StringField('Frequency Of Interaction', validators=[Length(max=50)])
    primary_attribution =  StringField('Primary Attribution:' , validators=[Length(max=50)])
    academic = BooleanField('Academic')
    submit_collab = SubmitField('Edit')
    remove_collab = SubmitField('Edit')

class UpdateSocietiesForm(FlaskForm):
    idd = "socc"
    id = StringField('ID:', validators=[ Length(max=50)])
    start_date = DateField('Start Date',render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date',render_kw={"placeholder": "YYYY-MM-DD"})
    society = StringField('Society:', validators=[ Length(max=50)])
    membership = StringField('Membership:',validators=[ Length(max=50)])
    status = StringField('Status:',validators=[ Length(max=20)])
    submit_soc = SubmitField('Edit Societies')
    remove_soc = SubmitField('Remove')

class UpdateInnovation(FlaskForm):
    id = StringField('ID',  validators=[ Length(max=50)])
    year = IntegerField('Year:' )
    type = StringField('Type', validators=[Length(max=50)])
    title = StringField('Title', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit_inn = SubmitField('Edit')
    remove_inn = SubmitField('Remove')



class UpdateAwardsForm(FlaskForm):
    id = StringField('ID:', validators=[ Length(max=50)])
    year = IntegerField('Year:')
    award_body = StringField('Awarding Body:', validators=[ Length(max=50)])
    details = StringField('Detail:', validators=[Length(max=50)])
    team_member = StringField('Team Member ', validators=[Length(max=50)])
    submit_awrd = SubmitField('Edit Awards')
    remove_awrd = SubmitField('Remove')

class AddSocietiesForm(FlaskForm):
    start_date = DateField('Start Date',render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date',render_kw={"placeholder": "YYYY-MM-DD"})
    society = StringField('Society:', validators=[ Length(max=50)])
    membership = StringField('Membership:',validators=[ Length(max=50)])
    status = StringField('Status:',validators=[ Length(max=20)])
    submit = SubmitField('Add Society')


class AddPresentations(FlaskForm):
    year = IntegerField('Year', )
    title = StringField('Title', validators=[Length(max=50)])
    type = StringField('Type', validators=[Length(max=50)])
    conference = StringField('Conference', validators=[Length(max=50)])
    invited_seminar = StringField('Invited Seminar', validators=[Length(max=50)])
    keynote = StringField('Keynote', validators=[Length(max=50)])
    organising_body = StringField('Organising Body', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution:' , validators=[Length(max=50)])
    submit = SubmitField('Add Presentation')

class AddCollaborations(FlaskForm):
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date =DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    institution = StringField('Institution', validators=[Length(max=50)])
    department = StringField('Department', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    name_collaborator = StringField('Name Colloaborator', validators=[Length(max=50)])
    primary_goal = StringField('Primary Goal',validators=[Length(max=50)] )
    frequency_of_interaction = StringField('Frequency Of Interaction', validators=[Length(max=50)])
    primary_attribution =  StringField('Primary Attribution:' , validators=[Length(max=50)])
    academic = BooleanField('Academic')
    submit = SubmitField('Add Collaborations')

class AddOrganisedEvents(FlaskForm):
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    title = StringField('Title', validators=[Length(max=50)])
    type = StringField('Type', validators=[Length(max=50)])
    role = StringField('Role', validators=[Length(max=50)])
    location = StringField('Location', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit = SubmitField('Add Organised Event')

class AddEducationAndPublicEngagement(FlaskForm):
    name = StringField('Name', validators=[Length(max=50)])
    start_date = DateField('Start Date', render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', render_kw={"placeholder": "YYYY-MM-DD"})
    activity = StringField('Activity', validators=[Length(max=50)])
    topic = StringField('Topic', validators=[Length(max=50)])
    target_area = StringField('Target Area', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit = SubmitField('Add Education and Public Engagement')


class AddAwardsForm(FlaskForm):

	year = IntegerField('Year:')
	award_body = StringField('Awarding Body:', validators=[ Length(max=50)])
	details = StringField('Detail:', validators=[Length(max=50)])
	team_member = StringField('Team Member ', validators=[Length(max=50)])
	submit = SubmitField('Add Awards')
class AddInnovation(FlaskForm):
    year = IntegerField('Year:' )
    type = StringField('Type', validators=[Length(max=50)])
    title = StringField('Title', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution', validators=[Length(max=50)])
    submit = SubmitField('Add Innovation')

class AddTeamMembersForm(FlaskForm):

    start_date = DateField('Start Date',render_kw={"placeholder": "YYYY-MM-DD"})
    departure_date = DateField('Departure Date',render_kw={"placeholder": "YYYY-MM-DD"})
    name = StringField('Name:', validators=[ Length(max=50)])
    position = StringField('Position:',validators=[ Length(max=50)])
    primary_attribution = StringField('Primary Attribution:',validators=[ Length(max=20)])
    team_id = IntegerField('TeamID')
    orcid = IntegerField('ORCID:' )
    submit = SubmitField('Add Team Members')

class AddImpactsForm(FlaskForm):
    title = StringField('Title: ', validators=[Length(max=50)])
    category = StringField('Category: ', validators=[Length(max=50)])
    primary_beneficiary = StringField('Primary Beneficiary: ', validators=[Length(max=50)])
    primary_attribution = StringField('Primary Attribution:', validators=[Length(max=50)])
    submit = SubmitField('Add Impacts')

class ExternalReviewForm(FlaskForm):

    pdfReview=FileField('PDF of Review',validators=[InputRequired()])
    submit = SubmitField('submit')

class ReportForm(FlaskForm):
    title = StringField('Title: ', validators=[Length(max=50), InputRequired()])
    pdf = FileField('PDF: ', validators=[InputRequired()])
    submit = SubmitField('Add')

#form for submission
class Submission_Form(FlaskForm):
    propid = StringField('propid')
    title = StringField('Title', validators=[InputRequired()],render_kw={"placeholder": "Title"})
    duration = IntegerField('Duration', validators=[InputRequired()],render_kw={"placeholder": "Duration in months"})
    NRP = SelectField(u'NRP', choices=[('areaA','Priority Area A - Future Networks & Communications'),
                                       ('areaB', 'Priority Area B - Data Analytics, Management, Securitu & Privacy'),
                                       ('areaC', 'Priority Area C - Digital Platforms, Content & Applications'),
                                       ('areaD', 'Priority Area D - Connected Health and Independent Living'),
                                       ('areaE', 'Priority Area E - Medical Devices'),
                                       ('areaF', 'Priority Area F - Diagnostics'),
                                       ('areaG', 'Priority Area G - Therapeutics : Synthesis, Formulation, Processing and Drug Delivery'),
                                       ('areaH', 'Priority Area H - Food for Health'),
                                       ('areaI', 'Priority Area I - Sustainable Food Production'),
                                       ('areaJ', 'Priority Area J - Marine Renewable Energy'),
                                       ('areaK', 'Priority Area K - Smart Grids & Smart Cities'),
                                       ('areaL', 'Priority Area L - Manufacturing Competitiveness'),
                                       ('areaM', 'Priority Area M - Processing Technologies and Novel Materials'),
                                       ('areaN', 'Priority Area N - Innovation in Services and Buisness Processses'),
                                       ('Software', 'Software'),
                                       ('Others', 'Others')
                                       ])
    legal_remit = TextAreaField("Please describe how your proposal is aligned with SFI's legal remit (max 250 words)"
                                ,validators=[InputRequired(), length(max=1250) ],render_kw={"placeholder": "Legal remit"}
                                )
    ethical_animal =  TextAreaField("A statement indicating whether the research involves the use of animals"
                                ,validators=[InputRequired()],render_kw={"placeholder": "Animal ethics statement"}
                                )
    ethical_human = TextAreaField("A statement indicating whether the research involves human participants, human biological material, or identifiable data"
                                   , validators=[InputRequired()], render_kw={"placeholder": "Human ethics statement"}
                                   )
    location = TextAreaField("A statement of the applicant’s location (country) at the time of submission"
                             , validators=[InputRequired()], render_kw={"placeholder": "Location statement"})
    co_applicants = TextAreaField("A list of co-applicants if applicable",render_kw={"placeholder": "List of co-applicants eg: '- name' "})
    collaborators = TextAreaField("Alist of collaborators, if applicable. Information about collaborators should include:( -Name -Organization -Email )"
                                  ,render_kw={"placeholder":"-name\n-organisation\n-Email;"})
    scientific_abstract = TextAreaField("Scientific Abstract( max 200 words )",
                                        validators=[InputRequired(), length(max=1000)], render_kw={"placeholder":"Scientific Abstract"} )
    lay_abstract = TextAreaField("Lay Abstract( max 100 words )",
                                        validators=[InputRequired(), length(max=500)], render_kw={"placeholder":"Lay Abstract"})
    proposalPDF = FileField("PDF of proposal" ,validators=[InputRequired()])
    declaration = BooleanField('Agree?', validators=[DataRequired(), ])
    submit = SubmitField('Submit')

    validate = SubmitField('Validate form')

    draft = SubmitField('Save Draft')

    def setPropId(self, propid):
        self.propid=propid


class proposalForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()],render_kw={"placeholder": "Title"})
    deadline = DateField('Deadline', validators=[InputRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    text_of_call = TextAreaField('Text of Call', validators=[InputRequired()], render_kw={"placeholder": "Text of call"})
    target_audience = StringField('Target Audience', validators=[InputRequired()], render_kw={"placeholder": "Target Audience"})
    eligibility_criteria = TextAreaField('Eligibility Criteria', validators=[InputRequired()], render_kw={"placeholder": "Eligibility Criteria"})
    duration = IntegerField('Duration', validators=[InputRequired()], render_kw={"placeholder": "Duration in Months"})
    reporting_guidelines = TextAreaField('Reporting Guidlines', validators=[InputRequired()], render_kw={"placeholder": "Reporting Guidelines"})
    time_frame = StringField('Time frame', validators=[InputRequired()], render_kw={"placeholder": "Time Frame"})
    picture = FileField('Upload Proposal Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class sendExternalReview(FlaskForm):
    ORCID=IntegerField('ORCID',validators=[InputRequired()],render_kw={"placeholder": "ORCID"})
    Decline=SubmitField('Decline application')
    submit=SubmitField('Send for review')
    complete=SubmitField('External Reviews Sent: Mark as under Review')

class ConfirmationForm(FlaskForm):
    Sub=StringField("Submission id")
    Approve=SubmitField("Approve Application")
    Decline=SubmitField("Decline Application")

    def setSub(self,sub):
        self.Sub=sub


# -------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
class ExternalReviewForm(FlaskForm):

    pdfReview=FileField('PDF of Review',validators=[InputRequired()])
    submit = SubmitField('submit')


def admin_setup(orcid):
    user=User.query.filter_by(orcid=orcid).first()
    user.type="Admin"
    db.session.commit()


class AddTeamMemberForm(FlaskForm):
    start_date = DateField("Start Date : ", validators=[InputRequired()], render_kw={"placeholder" : "YYYY-MM-DD"})
    departure_date = DateField("Departure Date : ", validators=[InputRequired()], render_kw={"placeholder" : "YYYY-MM-DD"})
    position = StringField("Position : ", validators=[InputRequired(), length(max=255)], render_kw={"placeholder" : "Position of the team member"})
    ORCID = IntegerField("ORCID : ", validators=[InputRequired()], render_kw={"placeholder" : "ORCID of the researcher to add to your team"})
    submit = SubmitField("Add")

class CreateTeamForm(FlaskForm):
    create = SubmitField("Click here to create a team!")

class DeleteTeamMemberForm(FlaskForm):
    delete = SubmitField("Remove")

class EditTeamMemberForm(FlaskForm):
    start_date = DateField("Start Date : ")
    departure_date = DateField("Departure Date : ")
    position = StringField("Position : ")
    primary_attribution = StringField("Primary Attribution : ")
    submit = SubmitField("Edit")


@login_manager.user_loader
def load_user(user_id):
    # this is a function that callsback the user by the user_id
    return User.query.get(int(user_id))


def mail(receiver, content="", email="", password="", subject=""):
    #function provides default content message, sender's email, and password but accepts
    #them as parameters if given
    #for now it sends an email to all researchers(i hope) not sure how im supposed to narrow it down yet
    #cur = mysql.get_db().cursor()
    #cur.execute("SELECT email FROM researchers")
    #rv = cur.fetchall()
    print(content)
    if not content:
        content = "Account made confirmation message"
    if not email:
        email = "team9sendermail@gmail.com"
    if not password:
        password = "default password"
        password = "team9admin"
    if not subject:
        subject="Account confirmation email"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['To'] = receiver
    msg['From'] = email
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email, password)
    #for email in rv:
    mail.sendmail(email,receiver,msg.as_string())
    mail.close()

@app.route('/')
@app.route('/home')
def index():

    #if current_user.is_authenticated:
    #    updateType = User.query.filter_by(orcid=current_user.orcid).first()
    #    updateType.type = "Admin"
    #    db.session.commit()
        # this route returns the home.html file
    #conn = mysql.connect
    #cur = conn.cursor()
    #cur.execute("DROP TABLE Submission;")
    #conn.commit()
    #cur.close()
    #conn.close()
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
        if user.type == "Admin":
            return redirect(url_for('dashboard')) #returns the admin page
        # and redirect to the index page which will be the profile page once its done
        return redirect(url_for('dashboard'))
    return render_template('sign_in.html', form=form)

@app.route('/forgot', methods=["Get",'Post'])
def forgot():
    form = ForgotForm()
    if form.submit.data:
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            send = "Follow this url to reset your password: https://johnnyos1304.pythonanywhere.com/reset?l=%s"%(email)
            subject = "Reset Password"
            mail(receiver=form.email.data,content=send,subject=subject)
            return redirect(url_for('link'))
        else:
            message="Please enter valid form data"
            return render_template('forgot.html', form=form)
    return render_template('forgot.html', form=form)

@app.route('/link', methods=["Get","Post"])
def link():
    message="Please check your email and follow the instructions."
    return render_template("link.html",messages=message)

@app.route("/reset", methods=["Get","Post"])
def reset():
    form = ResetForm()
    if request.method == "POST":
        if form.submit.data:
            print("here")
            hashed_password = generate_password_hash(form.new.data, method='sha256')
            email = request.args.get("l")
            user = User.query.filter_by(email=email).first()
            if user!=None:
                print("here2")
                user.password=hashed_password
                db.session.commit()
            return redirect(url_for("signin"))
    else:
        email = request.args.get("l")
        return render_template("reset.html",l=email,form=form)




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
                        phone=form.phone.data, phone_extension=form.phone_extension.data, password=hashed_password, type="Researcher")
            # add the new user to the database
            db.session.add(new_user)
            # commit the changes to the database
            db.session.commit()
            # send confirmation email
            mail(form.email.data)
            return redirect(url_for('signin'))  # a page that acknowledges the user has been created

        if user:
            flash('This email has already been used', category="email")
        if exist_orcid:
            flash('This orcid has already been registered', category="orcid")
        return redirect(url_for('signup'))
    return render_template('sign_up.html', form=form)  # return the signup html page



@app.route('/dashboard')
@login_required
def dashboard():
    # return the dashboard html file with the user passed to it
    profile = getProfileInfo()
    applications = Submissions.query.filter_by(user=current_user.orcid).all()
    reports = current_user.reports
    scientific_reports = []
    financial_reports = []
    for each in reports:
        if each.type == "Scientific":
            scientific_reports.append(each)
        elif each.type == "Financial":
            financial_reports.append(each)

    return render_template('dashboard.html', user=current_user, applications=applications, s_reports=scientific_reports, f_reports=financial_reports, info=profile)

@app.route('/scientific_reports', methods=["GET", "POST"] )
@login_required
def scientific_reports():
    id = request.args.get("id")
    print(id)
    form = ReportForm()
    reports = current_user.reports
    s_reports = []
    for each in reports:
        if each.type == "Scientific":
            s_reports.append(each)
    if request.method == "POST":
        print(form.title.data)
        print(form.pdf.data)
        if form.is_submitted():
            print("submitted")
        if form.validate():
            print("validated")
    if form.validate_on_submit():
        file = request.files['pdf']
        if file.filename=="":
            flash('No selected file')
            return redirect(url_for(scientific_reports))
        if file:
            filename = secure_filename(file.filename)
            file.save('/home/Johnnyos1304/Team9/uploads/'+filename)
            #file.save('uploads/'+filename)
            filenamesecret = uuid.uuid4().hex
            print("file saved")
        newReport = Report(title=form.title.data, type="Scientific", pdf=filenamesecret, ORCID=current_user.orcid, subid=id)
        db.session.add(newReport)
        db.session.commit()
        return redirect(url_for('scientific_reports'))
    return render_template("scientific_reports.html", reports=s_reports, form=form, id=id)
# @app.route('/edit')
# @login_required
'''if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))'''

@app.route('/financial_reports', methods=["GET", "POST"])
@login_required
def financial_reports():
    id = request.args.get("id")
    form = ReportForm()
    reports = current_user.reports
    f_reports = []
    for each in reports:
        if each.type == "Financial":
            f_reports.append(each)
    if request.method == "POST":
        print(form.title.data)
        print(form.pdf.data)
        if form.is_submitted():
            print("submitted")
        if form.validate():
            print("validated")
    if form.validate_on_submit():
        file = request.files['pdf']
        if file.filename=="":
            flash('No selected file')
            return redirect(url_for(finanical_reports))
        if file:
            filename = secure_filename(file.filename)
            file.save('/home/Johnnyos1304/Team9/uploads/'+filename)
            #file.save('uploads/'+filename)
            filenamesecret = uuid.uuid4().hex
            print("file saved")

        newReport = Report(title=form.title.data, type="Financial", pdf=filenamesecret, ORCID=current_user.orcid, subid=id)
        db.session.add(newReport)
        db.session.commit()
        return redirect(url_for('financial_reports'))
    return render_template("financial_reports.html", reports=f_reports, form=form)

@app.route('/current_applications')
@login_required
def current_applications():
    posts = []
    entries=Submissions.query.filter_by(user=current_user.orcid).all()
    for i in entries:
        post={}
        post["status"]=i.status
        post["title"]=i.title
        posts.append(post)
    return render_template("current_applications.html",posts=posts)

@app.route('/completed reviews_list')
@login_required
def completed_reviews_list():
    completed = Submissions.query.filter_by(status="Approval Pending").all()
    subs=[]
    for i in completed:
        sub={}
        sub["title"] = i.title
        sub["id"]=i.subid
        sub["status"]=i.status
        subs.append(sub)
    return render_template("completed_reviews_list.html",sub=subs)


@app.route('/completed_reviews',methods=['GET','POST'])
@login_required
def completed_review():
    #complete display of submission,review of submission and approval button
    id=request.args.get("id")
    rev = {}
    sub = {}
    prop = {}
        #display submission data
    if id!=None:
        i = Submissions.query.filter_by(subid=id).first()
        props = Proposal.query.filter_by(id=i.propid).first()
        prop["subid"] = props.id
        prop["deadline"] = props.Deadline
        prop["text"] = props.TextOfCall
        prop["audience"] = props.TargetAudience
        prop["eligibility"] = props.EligibilityCriteria
        prop["duration"] = props.Duration
        prop["guidelines"] = props.ReportingGuidelines
        prop["timeframe"] = props.TimeFrame
        prop["title"] = props.title

        sub["title"] = i.title
        sub["duration"] = i.duration
        sub["NRP"] = i.NRP
        sub["legal"] = i.legal
        sub["ethicalAnimal"] = i.ethicalAnimal
        sub["ethicalHuman"] = i.ethicalHuman
        sub["location"] = i.location
        sub["coapplicants"] = i.coapplicants
        sub["collaborators"] = i.collaborators
        sub["scientific"] = i.scientific
        sub["lay"] = i.lay
        sub["file"] = i.proposalPDF

        review=ExternalReview.query.filter_by(Submission=i.subid).first()

        rev["file"]=review.review
        rev["reviewer"]=review.reviewer


    form=ConfirmationForm()
    form.setSub(i)
    if form.Decline.data:
        print("declined")
        form.Sub.status="declined"
        db.session.commit()
        return redirect(url_for("dashboard"))
    if form.Approve.data:
        form.Sub.status="Approved"
        #create a new funding thingy
        #create a new team data thingy
        #
        db.session.commit()
        return redirect(url_for("funding", id=id))
    return render_template("completed_reviews.html",form=form,sub=sub,rev=rev,prop=prop)

class FundingForm(FlaskForm):
    start_date = DateField("Start Date : ")
    end_date = DateField("End Date : ")
    amount_funding = IntegerField("Amount Funding : ")
    funding_body = TextAreaField("Funding Body : ")
    funding_programme = TextAreaField("Funding Programme : ")
    stats = StringField("Stats : ")
    primary_attribution = StringField("Primary Attribution : ")
    submit = SubmitField("Submit")

@app.route('/funding', methods=["GET", "POST"])
@login_required
def funding():
    id = request.args.get("id")
    submission = Submissions.query.filter_by(subid=id).first()
    orcid = submission.user
    print(submission)
    fundingform = FundingForm()
    funding = Funding.query.filter_by(subid=id).first()
    if fundingform.submit.data and fundingform.validate():
        new_funding = Funding(StartDate=fundingform.start_date.data, EndDate=fundingform.end_date.data,
            AmountFunding=fundingform.amount_funding.data, FundingBody=fundingform.funding_body.data, 
            FundingProgramme=fundingform.funding_programme.data,Stats=fundingform.stats.data, 
            PrimaryAttribution=fundingform.primary_attribution.data, orcid=orcid, subid=id)
        db.session.add(new_funding)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template("funding.html", id=id, fundingform=fundingform, submission=submission, funding=funding)

@app.route('/admin_external_review')
@login_required
def admin_external_review():
    posts = []
    entries = Submissions.query.filter_by(status="pending").all()
    for i in entries:
        post = {}
        post["status"] = i.status
        post["title"] = i.title
        post["id"] = i.subid
        posts.append(post)
    return render_template("admin_external_review.html", posts=posts)

@app.route('/admin_send_review',methods=['GET', 'POST'])
@login_required
def admin_send_review():
    form=sendExternalReview()
    post=request.args.get("id")
    sub={}
    prop={}
    i = Submissions.query.filter_by(subid=f"{post}").first()
    props=Proposal.query.filter_by(id=i.propid).first()
    prop["subid"] = props.id
    prop["deadline"] = props.Deadline
    prop["text"] = props.TextOfCall
    prop["audience"] = props.TargetAudience
    prop["eligibility"] = props.EligibilityCriteria
    prop["duration"] = props.Duration
    prop["guidelines"] = props.ReportingGuidelines
    prop["timeframe"] = props.TimeFrame
    prop["title"] = props.title

    sub["title"]=i.title
    sub["duration"]=i.duration
    sub["NRP"]=i.NRP
    sub["legal"]=i.legal
    sub["ethicalAnimal"]=i.ethicalAnimal
    sub["ethicalHuman"]=i.ethicalHuman
    sub["location"]=i.location
    sub["coapplicants"]=i.coapplicants
    sub["collaborators"]=i.collaborators
    sub["scientific"]=i.scientific
    sub["lay"]=i.lay
    sub["file"]=i.proposalPDF

    if form.Decline.data:
        i.status="declined"
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("admin_external_review"))

    elif form.complete.data:
        #change submission to external review when done button is pressed
        i.status="review"
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("dashboard"))
        reviewer = User.query.filter_by(orcid = form.ORCID.data).first()
        email = reviewer.email
        mail(email, "Review request made, check your profile")

    elif form.ORCID.data!=None:
        print("here")
        #database push external review link to user
        new_external_review=ExternalPendingReviews(post,form.ORCID.data,False)
        db.session.add(new_external_review)
        db.session.commit()
        flash("sent for external review")
    return render_template("admin_send_review.html",sub=sub,prop=prop,form=form)

@app.route('/reviewer_pending_list')
@login_required
def reviewer_pending_list():
    posts = []
    entries = ExternalPendingReviews.query.filter_by(reviewer=current_user.orcid).all()
    #change this DB request to look for reveiews appropropriate to the current_user.orcid
    for i in entries:
        sub=Submissions.query.filter_by(subid=i.Submission).first()
        post = {}
        post["status"] = sub.status
        post["title"] = sub.title
        post["id"] = sub.subid
        post["file"]=sub.proposalPDF
        posts.append(post)
    return render_template("reviewer_pending_list.html", posts=posts)


@app.route('/create_submission_form')
@login_required
def create_submission_page():
    # return the dashboard html file with the user passed to it
    posts=[]
    #conn = mysql.connect
    #cur = conn.cursor()
    # execute a query
    proposals = Proposal.query.all()
    #cur.execute("""
    #            SELECT *
    #            FROM Proposal;
    #            """)
    #for i in cur.fetchall():
    for each in proposals:
        post={}
        post["id"] = each.id
        post["deadline"] = each.Deadline
        post["text"] = each.TextOfCall
        post["audience"] = each.TargetAudience
        post["eligibility"] = each.EligibilityCriteria
        post["duration"] = each.Duration
        post["guidelines"] = each.ReportingGuidelines
        post["timeframe"] = each.TimeFrame
        posts.append(post)
    #conn.commit()

    #cur.close()
    #conn.close()
    return render_template('create_submission_form.html', user=current_user, posts=posts)
# @app.route('/resetpassword')

@app.route('/proposals', methods=['GET' , 'POST'])
@login_required
def proposals():
    #posts = []
    proposals = Proposal.query.all()
    #conn = mysql.connect
    #cur = conn.cursor()
    # execute a query

    """cur.execute(""
                 SELECT *
                 FROM Proposal;
                 "")"""
    #for post in proposals:
    #for i in cur.fetchall():
        #post = {}
        #print(i)
        #post["id"] = i[9]
        #post["deadline"] = i[0]
        #post["text"] = i[2]
        #post["audience"] = i[3]
        #post["eligibility"] = i[4]
        #post["duration"] = i[5]
        #post["guidelines"] = i[6]
        #post["timeframe"] = i[7]
        #post["title"] = i[1]
        #posts.append(post)
    #conn.commit()

    #cur.close()
    #conn.close()
    return render_template('proposals.html', user=current_user, posts=proposals)

@app.route('/submissions',methods=['GET' , 'POST'])
@login_required
def submissions():
    #fix request shit
    sub={}
    form=Submission_Form()
    post=request.args.get("id")
    form.setPropId(post)
    submissions = Submissions.query.filter_by(propid=post, user=current_user.orcid).first()
    #conn = mysql.connect
    #cur = conn.cursor()
    previousFile=None



    """cur.execute(f""
                             SELECT *
                             FROM Submission
                             WHERE propid = {post} AND user='{current_user.orcid}';
                             ")"""
    #for i in cur.fetchall():
    #    if i[15]==0:
    #        return render_template("submitted.html")
    #    form.propid=i[0]
    #    form.title.data=i[2]
    #    form.duration.data=i[3]
    #    form.NRP.data=i[4]
    #    form.legal_remit.data=i[5]
    #    form.ethical_animal.data=i[6]
    #    form.ethical_human.data=i[7]
    #    form.location.data=i[8]
    #    form.co_applicants.data=i[9]
    #    form.collaborators.data=i[10]
    #    form.scientific_abstract.data=i[11]
    #    form.lay_abstract.data=i[12]
    #    form.declaration.data=i[13]
    #    previousFile=i[16]



    #cur.close()
    #conn.close()


    if form.validate_on_submit():
        if form.validate.data:
            flash("Input Successfully Validated")
        elif form.draft.data:
            print(previousFile)
            filenamesecret = previousFile
            if form.proposalPDF.data!=None:
                filenamesecret = uuid.uuid4().hex
                if filenamesecret != previousFile:
                    form.proposalPDF.data.save('/home/Johnnyos1304/Team9/uploads/' + filenamesecret)
                else:
                    while True:
                        filecheck=Path(f"/home/Johnnyos1304/Team9/uploads/{filenamesecret}")
                        if filecheck.is_file():
                            filenamesecret = uuid.uuid4().hex
                        else:
                            break
                    form.proposalPDF.data.save('/home/Johnnyos1304/Team9/uploads/' + filenamesecret)
                    print(filenamesecret + "1")

                if previousFile != None:
                    os.remove(f"/home/Johnnyos1304/Team9/uploads/{previousFile}")

            existing_submission = Submissions.query.filter_by(propid=form.propid, user=current_user.orcid).first()
            print(existing_submission)
            if existing_submission:
                existing_submission.propid = form.propid
                existing_submission.title = form.title.data
                existing_submission.duration = form.duration.data
                existing_submission.NRP = form.NRP.data
                existing_submission.legal = form.legal_remit.data
                existing_submission.ethicalAnimal = form.ethical_animal.data
                existing_submission.ethicalHuman = form.ethical_human.data
                existing_submission.location = form.location.data
                existing_submission.coapplicants = form.co_applicants.data
                existing_submission.collaborators = form.collaborators.data
                existing_submission.scientific = form.scientific_abstract.data
                existing_submission.lay = form.lay_abstract.data
                existing_submission.declaration = form.declaration.data
                existing_submission.proposalPDF = filenamesecret
                existing_submission.draft = 0
                print(existing_submission.legal, " ", form.legal_remit.data)
                db.session.commit()
                return redirect(url_for("submissions", id=form.propid, sub=sub,submissions=submissions))


            new_submission=Submissions(propid=form.propid,title=form.title.data, duration=form.duration.data,
                                       NRP=form.NRP.data,legal=form.legal_remit.data,
                                       ethicalAnimal=form.ethical_animal.data,
                                       ethicalHuman=form.ethical_human.data,
                                       location=form.location.data,
                                       coapplicants=form.co_applicants.data,
                                       collaborators=form.collaborators.data,
                                       scientific=form.scientific_abstract.data,
                                       lay=form.lay_abstract.data,
                                       declaration=form.declaration.data,
                                       user=f"{current_user.orcid}",
                                       proposalPDF=f"{filenamesecret}"
                                       )
            db.session.add(new_submission)
            db.session.commit()
            flash("successfully Saved Draft")
            return redirect(url_for("submissions",id=form.propid,sub=sub,submissions=submissions))
        elif form.submit.data:
            filenamesecret = previousFile
            if form.proposalPDF.data!=None:
                filenamesecret = uuid.uuid4().hex
                if filenamesecret != previousFile:
                    while True:
                        filecheck=Path(f"/home/Johnnyos1304/Team9/uploads/{filenamesecret}")
                        if filecheck.is_file():
                            filenamesecret = uuid.uuid4().hex
                        else:
                            break
                    form.proposalPDF.data.save('/home/Johnnyos1304/Team9/uploads/' + filenamesecret)
                    if previousFile != None:
                        os.remove(f"/home/Johnnyos1304/Team9/uploads/{previousFile}")

            existing_submission = Submissions.query.filter_by(propid=form.propid, user=current_user.orcid).first()
            if existing_submission:
                existing_submission.propid = form.propid
                existing_submission.title = form.title.data
                existing_submission.duration = form.duration.data
                existing_submission.NRP = form.NRP.data
                existing_submission.legal = form.legal_remit.data
                existing_submission.ethicalAnimal = form.ethical_animal.data
                existing_submission.ethicalHuman = form.ethical_human.data
                existing_submission.location = form.location.data
                existing_submission.coapplicants = form.co_applicants.data
                existing_submission.collaborators = form.collaborators.data
                existing_submission.scientific = form.scientific_abstract.data
                existing_submission.lay = form.lay_abstract.data
                existing_submission.declaration = form.declaration.data
                existing_submission.proposalPDF = filenamesecret
                existing_submission.draft = 0
                db.session.commit()
                return redirect(url_for("submitted"))

            new_submission = Submissions(propid=form.propid, title=form.title.data, duration=form.duration.data,
                                         NRP=form.NRP.data, legal=form.legal_remit.data,
                                         ethicalAnimal=form.ethical_animal.data,
                                         ethicalHuman=form.ethical_human.data,
                                         location=form.location.data,
                                         coapplicants=form.co_applicants.data,
                                         collaborators=form.collaborators.data,
                                         scientific=form.scientific_abstract.data,
                                         lay=form.lay_abstract.data,
                                         declaration=form.declaration.data,
                                         user=f"{current_user.orcid}",
                                         proposalPDF=f"{filenamesecret}"
                                         )
            new_submission.setDraftFalse()
            db.session.add(new_submission)
            db.session.commit()
            flash("successfully submitted")
            return redirect(url_for("submissions", id=form.propid, sub=sub, submissions=submissions))



    i=Proposal.query.filter_by(id=f"{post}").first()
    sub["id"] = i.id
    sub["deadline"] = i.Deadline
    sub["text"] = i.TextOfCall
    sub["audience"] = i.TargetAudience
    sub["eligibility"] = i.EligibilityCriteria
    sub["duration"] = i.Duration
    sub["guidelines"] = i.ReportingGuidelines
    sub["timeframe"] = i.TimeFrame
    sub["title"] = i.title

    return render_template('submissions.html', user=current_user, sub=sub,form=form, submissions=submissions)

#needs to be fixed cant save image
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/propoosal_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/download')
@login_required
def download():
    filename=request.args.get("file")
    dir="uploads"
    return send_from_directory(dir,filename,as_attachment=True)

@app.route('/external_review',methods=['GET','POST'])
@login_required
def external_review():
    form = ExternalReviewForm()
    file=request.args.get("file")
    review=request.args.get("pdfReview")
    if form.pdfReview.data!=None:
        print("here")
        filenamesecret = uuid.uuid4().hex
        form.pdfReview.data.save('/home/Johnnyos1304/Team9/uploads/' + filenamesecret)
        #form.pdfReview.data.save('uploads/' + filenamesecret)
        sub=Submissions.query.filter_by(proposalPDF=file).first()
        new_review = ExternalReview(sub.subid,current_user.orcid,True,filenamesecret)
        sub.status="Approval Pending"
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("dashboard"))

    if file==None and review==None:
        return redirect(url_for("index"))
    return render_template('external_review.html',file=file,form=form)

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
            #if form.picture.data:         #image processing
             #   print("here ttt")
              #  picture_file = save_picture(form.picture.data)
               # Image.open(picture_file)
            deadline = form.deadline.data
            textofcall = form.text_of_call.data
            targetaudience = form.target_audience.data
            eligibilitycriteria = form.eligibility_criteria.data
            duration = form.duration.data
            reportingguidelines = form.reporting_guidelines.data
            timeframe = form.time_frame.data
            title = form.title.data

            new_proposal = Proposal(Deadline=deadline, title=title, TextOfCall=textofcall,TargetAudience=targetaudience,
                EligibilityCriteria=eligibilitycriteria, Duration=duration, ReportingGuidelines=reportingguidelines, TimeFrame=timeframe)
            #conn = mysql.connect
            #cur = conn.cursor()
            # execute a query
            #cur.execute(""INSERT INTO Proposal(Deadline,Title, TextOfCall, TargetAudience, EligibilityCriteria, Duration, ReportingGuidelines, TimeFrame)
            ##            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",(deadline,title, textofcall, targetaudience, eligibilitycriteria, duration, reportingguidelines, timeframe))
            # rv contains the result of the execute
            #conn.commit()
            #cur.close()
            #conn.close()
            db.session.add(new_proposal)
            db.session.commit()
            #links to form creation
            print("here")
            return redirect(url_for('dashboard'))
        return render_template('proposal_call.html', form=form)
    else:
        return render_template('proposal_call.html', form=form)


@app.route('/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info():
    update_general = UpdateInfoForm(request.form)
    update_education = UpdateEducationForm(request.form)
    update_societies = UpdateSocietiesForm(request.form)
    update_employment = UpdateEmploymentForm(request.form)
    update_awards = UpdateAwardsForm(request.form)
    update_funding = UpdateFundingForm(request.form)
    update_org = UpdateOrganisedEvents(request.form)
    update_pub = UpdatePublications(request.form)
    update_imp = UpdateImpactsForm(request.form)
    update_edup = UpdateEducationAndPublicEngagement(request.form)
    update_pres = UpdatePresentations(request.form)
    update_collab = UpdateCollaborations(request.form)
    update_inn = UpdateInnovation(request.form)
    user = current_user
    print(user.societies)

    if request.method == 'POST':

        #print(update_general.errors)
        #if input validates pushes to db
        #
        if update_general.validate_on_submit() :


            update_user = User.query.filter_by(orcid=current_user.orcid).first()

            update_user.first_name = update_general.first_name.data
            update_user.last_name = update_general.last_name.data
            update_user.email = update_general.email.data
            update_user.job = update_general.job.data
            update_user.prefix = update_general.prefix.data
            update_user.suffix = update_general.suffix.data
            update_user.phone = update_general.phone.data
            update_user.phone_extension = update_general.phone_extension.data

            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE Researcher SET FirstName='{first_name}', LastName='{last_name}', Job='{job}', Prefix='{prefix}', Suffix='{suffix}',
            #        Phone={phone}, PhoneExtension={phone_extension}, Email='{email}' WHERE ORCID ={current_user.orcid};  """)
            ##conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))



       # Edit societies
        elif update_societies.validate_on_submit() and "submit_soc" in request.form:

            updates = Societies.query.filter_by(ORCID=current_user.orcid).all()
            id1 = update_societies.id.data

            for each in updates:
                if each.id == id1:
                    each.start_date = update_societies.start_date.data
                    each.end_date = update_societies.end_date.data
                    each.society = update_societies.society.data
                    each.membership = update_societies.membership.data
                    each.status = update_societies.status.data

            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE Societies SET StartDate= '{start_date}', EndDate='{end_date}', Society = '{society}', Membership = '{membership}',
            #Status = '{status}' WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('societiesInfo'))
        # Remove societies
        elif update_societies.validate_on_submit() and "remove_soc" in request.form:
            print("here")

            id1 = update_societies.id.data
            society = Societies.query.filter_by(id=id1).first()

            db.session.delete(society)
            db.session.commit()


            #conn = mysql.connect
            #cur= conn.cursor()
            ## execute a query
            #cur.execute(f"""DELETE FROM Societies WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('edit_info'))
        # Edit Education
        elif update_education.validate_on_submit() and "submit_edu" in request.form:
            degree = update_education.degree.data
            institution = update_education.institution.data
            location = update_education.location.data
            year = update_education.year.data
            field = update_education.field.data
            id = update_education.id.data


            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""UPDATE Education SET Degree = '{degree}', Institution = '{institution}', Location= '{location}',
             Year= {year}, Field = '{field}' WHERE ID ={id};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('educationInfo'))
        #Remove Edu
        elif update_education.validate_on_submit() and "remove_edu" in request.form:
            print("here")

            id1 = update_education.id.data

            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Education WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('edit_info'))

        #Edit Employment
        elif update_employment.validate_on_submit() and "submit_emp" in request.form:

            employment = Employment.query.filter_by(ORCID=current_user.orcid).all()
            id2 = update_employment.id.data

            for each in employment:
                if each.id == id2:
                    each.company = update_employment.company.data
                    each.location = update_employment.location.data
                    each.years = update_employment.years.data
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE Employment SET Company = '{company}',  Location= '{location}',
            # Years= {years}  WHERE ID ={id2};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('employmentInfo'))
        #Remove Employment
        elif update_employment.validate_on_submit() and "remove_emp" in request.form:
            print("here")

            id1 = update_employment.id.data

            employment = Employment.query.filter_by(id=id1).first()

            db.session.delete(employment)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Employment WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('edit_info'))

        #Edit Awards
        elif update_awards.validate_on_submit() and "submit_awrd" in request.form:
            id3 = update_awards.id.data
            awards = Awards.query.filter_by(id=id3).first()
            awards.year = update_awards.year.data
            awards.award_body = update_awards.award_body.data
            awards.details = update_awards.details.data
            awards.team_member = update_awards.team_member.data

            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE Awards SET Year = {year}, AwardingBody = '{award_body}', Details = '{details}',
            #TeamMember = '{team_member}' WHERE ID ={id3};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('awardsInfo'))
        #Remove Awards
        elif update_awards.validate_on_submit() and "remove_awrd" in request.form:
            print("here")

            id1 = update_awards.id.data

            award = Awards.query.filter_by(id=id1).first()
            db.session.delete(award)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Awards WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('edit_info'))
        elif update_org.validate_on_submit() and "submit_org" in request.form:
            id1 = update_org.id.data
            org = OrganisedEvents.query.filter_by(id=id1).first()
            org.start_date = update_org.start_date.data
            org.end_date = update_org.end_date.data
            org.title = update_org.title.data
            org.type = update_org.type.data
            org.role = update_org.type.data
            org.location = update_org.location.data
            org.primary_attribution = update_org.primary_attribution.data
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE OrganisedEvents SET StartDate = '{start_date}', EndDate = '{end_date}', Title='{title}', Type = '{type}',
            #Role = '{role}', Location = '{location}', PrimaryAttribution = {primary_attribution} WHERE ID = {id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('organised_events_info'))
        elif update_org.validate_on_submit() and "remove_org" in request.form:
            print("here")
            id1 = update_org.id.data
            org = OrganisedEvents.query.filter_by(id=id1).first()

            db.session.delete(org)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM OrganisedEvents WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('edit_info'))

        elif update_funding.validate_on_submit() and "submit_fund" in request.form:
            id1 = update_funding.id.data
            funding = Funding.query.filter_by(id=id1).first()
            funding.start_date = update_funding.start_date.data
            funding.end_date = update_funding.end_date.data
            funding.amount_funding = update_funding.amount_funding.data
            funding.funding_body= update_funding.funding_body.data
            funding.funding_programme = update_funding.funding_programme.data
            funding.stats = update_funding.stats.data
            funding.primary_attribution = update_funding.primary_attribution.data
            #conn = mysql.connect
            #funds = Funding.query.filter_by(ID = id1).first
            #funds.start_date = start_date
            #funds.end_date = end_date
            #funds.amount_funding = amount_funding
            #funds.funding_body = funding_body
            #funds.funding_programme = funding_body
            #funds.stats = stats
            #funds.primary_attribution = primary_attribution
            db.session.commit()
            return redirect(url_for('profile'))
        #Remove Awards
        elif update_funding.validate_on_submit() and "remove_fund" in request.form:
            print("here")

            id1 = update_funding.id.data

            funding = Funding.query.filter_by(id=id1).first()

            db.session.delete(funding)
            db.session.commit()

            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Funding WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_pub.validate_on_submit() and "submit_pub" in request.form:
            id2 = update_pub.id.data
            pub = Publications.query.filter_by(id=id2).first()
            pub.year = update_pub.year.data
            pub.type = update_pub.type.data
            pub.title = update_pub.title.data
            pub.name = update_pub.name.data
            pub.status = update_pub.status.data
            pub.doi = update_pub.doi.data
            pub.primary_attribution = update_pub.primary_attribution.data

            db.session.commit()
            #conn = mysql.connect()
            #cur = conn.cursor()
            #cur.execute(f"""UPDATE Publications SET Year = {year}, Type = '{type}', Title= '{title}',
            # Name = '{name}', Status = '{status}', DOI = '{doi}' WHERE ID = {id2} """)
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_pub.validate_on_submit() and "remove_pub" in request.form:
            print("here")
            id1 = update_pub.id.data
            pub = Publications.query.filter_by(id=id1).first()

            db.session.delete(pub)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Publications WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_imp.validate_on_submit() and "submit_imp" in request.form:
            id2 = update_imp.id.data
            imp = Impacts.query.filter_by(id=id2).first()
            imp.title = update_imp.title.data
            imp.category = update_imp.category.data
            imp.primary_beneficiary = update_imp.primary_beneficiary.data
            imp.primary_attribution = update_imp.primary_attribution.data

            db.session.commit()
            #conn = mysql.connect()
            #cur = conn.cursor()
            #cur.execute(f"""UPDATE Impacts SET Title = '{title}', Category = '{category}' , PrimaryBeneficiary = '{primary_beneficiary}',
            #PrimaryAttribution = '{primary_attribution}' WHERE ID = {id2} """)
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_imp.validate_on_submit() and "remove_imp" in request.form:
            print("here")
            id1 = update_imp.id.data
            imp = Impacts.query.filter_by(id=id1).first()

            db.session.delete(imp)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Impact WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_edup.validate_on_submit() and "submit_edup" in request.form:
            id1 = update_edup.id.data
            edup = EducationAndPublicEngagement.query.filter_by(id=id1).first()
            edup.name = update_edup.name.data
            edupstart_date = update_edup.start_date.data
            edup.end_date = update_edup.end_date.data
            edup.activity = update_edup,activity.data
            edup.topic = update_edup.topic.data
            edup.target_area = update_edup.target_area.data
            edup.primary_attribution = update_edup.primary_attribution.data

            db.session.commit()
            #conn = mysql.connect()
            #cur = conn.cursor()
            #cur.execute(f"""UPDATE EducationAndPublicEngagement SET Name = '{name}', StartDate = '{start_date}', EndDate = '{end_date}',
            #Activity = '{activity}', Topic = '{topic}', TargetArea = '{target_area}', PrimaryAttribution='{primary_attribution}' WHERE ID = {id1} """)
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_edup.validate_on_submit() and "remove_edup" in request.form:
            print("here")
            id1 = update_edup.id.data
            edup = EducationAndPublicEngagement.query.filter_by(id=id1).first()

            db.session.delete(edup)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM EducationAndPublicEngagemen WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_pres.validate_on_submit() and "submit_pres" in request.form:
            id1 = update_pres.id.data
            pres = Presentations.query.filter_by(id=id1).first()
            pres.year = update_pres.year.data
            pres.title = update_pres.title.data
            pres.type = update_pres.type.data
            pres.conference = update_pres.conference.data
            pres.invited_seminar = update_pres.invited_seminar.data
            pres.keynote = update_pres.keynote.data
            pres.organising_body = update_pres.organising_body.data
            pres.location = update_pres.location.data

            db.session.commit()
            #conn = mysql.connect()
            #cur = conn.cursor()
            #cur.execute(f"""UPDATE Presentations SET Year = {year}, Title = '{title}', Type = '{type}', Conference='{conference}',
            # InvitedSeminar='{invited_seminar}', Keynote = '{keynote}', OrganisedBody = '{organising_body}', Location = '{location}' WHERE ID = {id1} """)
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_pres.validate_on_submit() and "remove_pres" in request.form:
            print("here")
            id1 = update_pres.id.data
            pres = Presentations.query.filter_by(id=id1).first()

            db.session.delete(pres)
            db.session.commit()
            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""DELETE FROM Presentations WHERE ID ={id1};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))
        elif update_collab.validate_on_submit and "submit_collab" in request.form:
            id1 = update_collab.id.data
            start_date = update_collab.start_date.data
            end_date = update_collab.end_date.data
            department = update_collab.end_date.data
            location =  update_collab.end_date.data
            name_collaborator = update_collab.name_collaborator.data
            primary_goal = update_collab.primary_goal.data
            frequency_of_interaction = update_collab.frequency_of_interaction.data
            primary_attribution = update_collab.primary_attribution.data
            academic = update_collab.academic.data
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(f"""UPDATE Collaboratiions Set StartDate = '{start_date}', EndDate = '{end_date}', Department = '{department}', Location='{location}',
            NameCollaborator = '{name_collaborator}', PrimaryGoal = '{primary_goal}', FrquencyOfInteraction = '{frequency_of_interaction}',
             PrimaryAttribution='{primary_attribution}', Academic = {academic} WHERE ID = {id1} """)
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        elif update_pres.validate_on_submit and "remove_collab" in request.form:
            print("here")
            id1 = update_collab.id.data
            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Collaborations WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        elif update_inn.validate_on_submit and "submit_inn" in request.form:
            id1 = update_inn.id.form
            year = update_inn.year.form
            type = update_inn.type.form
            title = update_inn.title.form
            primary_attribution = update_inn.primary_attribution._form
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(f"""UPDATE Innovations Set Year = {year}, Type = '{type}', Title = '{title}', PrimaryAttribution = '{primary_attribution}'
             WHERE ID = {id1} """)
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        elif update_inn.validate_on_submit and "remove_inn" in request.form:
            print("here")
            id1 = update_inn.id.data
            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Innovations WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))



    return render_template('edit_info.html', form1=update_general, form2=update_education , form3=update_societies, form4 = update_employment,
    form5 = update_awards,form6 = update_funding ,form7= update_org, form8=update_pub, form9=update_imp ,form10 = update_edup,
     form11 = update_pres,  form12 = update_collab , form13 = update_inn ,user=user)




@app.route('/generalInfo', methods=['GET', 'POST'])
@login_required
def generalInfo():
    #Creates proposal form
    form = UpdateInfoForm(request.form)

    #checks if form is submitted by post
    if request.method == 'POST':

        print(form.errors)
        #if input validates pushes to db
        if form.validate_on_submit():

            #if form.picture.data:         #image processing
             #   print("here ttt")
              #  picture_file = save_picture(form.picture.data)
               # Image.open(picture_file)
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.job = form.job.data
            current_user.prefix = form.prefix.data
            current_user.suffix = form.suffix.data
            current_user.phone = form.phone.data
            current_user.phone_extension = form.phone_extension.data

            db.session.commit()

            #conn = mysql.connect
            #cur= conn.cursor()
            # execute a query
            #cur.execute(f"""UPDATE Researcher SET FirstName='{first_name}', LastName='{last_name}', Job='{job}', Prefix='{prefix}', Suffix='{suffix}',
            #        Phone={phone}, PhoneExtension={phone_extension}, Email='{email}' WHERE ORCID ={current_user.orcid};  """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('profile'))

    return render_template('generalInfo.html', form=form)

@app.route('/innovation_info', methods=['GET', 'POST'])
@login_required
def innovation_info():
    form = AddInnovation(request.form)
    innovation = InnovationAndCommercialisation.query.all()
    print(innovation)

    if request.method == 'POST':
        if form.validate_on_submit():
            year = form.year.data
            type = form.type.data
            title = form.title.data
            primary_attribution = form.primary_attribution.data

            inno = InnovationAndCommercialisation(year=year, type=type, title=title,primary_attribution=primary_attribution,ORCID=current_user.orcid)
            db.session.add(inno)
            db.session.commit()
            #conn = mysql.connect
            #cur = conn.cursor()
            #cur.execute(f"""INSERT Into InnovationAndCommercialisation (Year, Type, Title, PrimaryAttribution, ORCID) VALUES ('{year}','{type}','{title}',
            #'{primary_attribution}', {current_user.orcid}) """)
            #conn.commit()
            #cur.close()
            #conn.close()
            return redirect(url_for('innovation_info'))
        return render_template('innovation_info.html', form = form)
    innovation_list = current_user.inno_and_comm
    print(innovation_list)
    return render_template('innovation_info.html', form=form, list = innovation_list)

@app.route('/presentations_info', methods=['GET','POST'])
@login_required
def presentations_info():
    form = AddPresentations(request.form)
    presentations = Presentations.query.all()
    print(presentations)

    if request.method == 'POST':
        if form.validate_on_submit():
            year = form.year.data
            title = form.title.data
            type = form.type.data
            conference = form.conference.data
            invited_seminar = form.invited_seminar.data
            keynote = form.keynote.data
            organising_body = form.organising_body.data
            location = form.location.data
            primary_attribution = form.primary_attribution.data
            conn = mysql.connect
            cur = conn.cursor()
            cur.execute(f""" INSERT Into Presentations (Year, Title, Type, Conference, InvitedSeminar, Keynote, OrganisingBody,
            Location, PrimaryAttribution, ORCID) VALUES ({year}, '{title}','{type}', '{conference}', '{invited_seminar}' , '{keynote}', '{organising_body}',
            '{location}', '{primary_attribution}', {current_user.orcid});""")
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('presentations_info.html', form=form)
    presentations_list = current_user.presentations
    return render_template('presentations_info.html', form=form, list=presentations_list)

@app.route('/collaborations_info', methods=['GET','POST'])
@login_required
def collaborations_info():
    form = AddCollaborations(request.form)
    collaborations = Collaborations.query.all()
    print(collaborations)

    if request.method == 'POST':
        if form.validate_on_submit():
            start_date = form.start_date.data
            end_date = form.end_date.data
            institution = form.institution.data
            department = form.department.data
            location = form.location.data
            name_collaborator = form.name_collaborator.data
            primary_goal = form.primary_goal.data
            frequency_of_interaction =  form.frequency_of_interaction.data
            primary_attribution =  form.primary_attribution.data
            academic = form.academic.data
            conn = mysql.connect
            cur = conn.cursor()
            cur.execute(f""" INSERT Into Collaborations (StartDate, EndDate, Institution, Department, Location, NameCollaborator,
            PrimaryGoal,FrequencyOfInteraction, PrimaryAttribution,Academic, ORCID) VALUES ('{start_date}','{end_date}','{institution}'
            ,'{department}','{location}','{name_collaborator}','{primary_goal}','{frequency_of_interaction}',
            '{primary_attribution}',{academic},{current_user.orcid});""")
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('collaborations_info.html',form=form)
    collaborations_list = current_user.collab
    return render_template('collaborations_info.html', form=form, list= collaborations_list)


@app.route('/funding_info', methods=['GET', 'POST'])
@login_required
def funding_info():
    form = AddFundingForm(request.form)
    funding = Funding.query.all()
    print(funding)

    if request.method == 'POST':
        if form.validate_on_submit():
            start_date = form.start_date.data
            end_date = form.end_date.data
            amount_funding = form.amount_funding.data
            funding_body = form.funding_body.data
            funding_programme = form.funding_programme.data
            stats = form.stats.data
            primary_attribution = form.primary_attribution.data
            conn = mysql.connect
            cur = conn.cursor()
            cur.execute(f""" INSERT Into Funding (StartDate, EndDate, AmountFunding,FundingBody,FundingProgramme,
            Stats, PrimaryAttribution, ORCID) VALUES ('{start_date}','{end_date}', {amount_funding},
            '{funding_body}','{funding_programme}', '{stats}', '{primary_attribution}', {current_user.orcid});""")
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('funding_info.html', form=form)

    funding_list = current_user.funding
    print(funding_list)
    return render_template('funding_info.html', form=form, list = funding_list)

@app.route('/publications_info', methods=['GET','POST'])
@login_required
def publications_info():
    form = AddPublications(request.form)
    publications = Publications.query.all()
    if request.method =='POST':
        if form.validate_on_submit():

            year = form.year.data
            type = form.type.data
            title = form.title.data
            name = form.name.data
            status = form.status.data
            doi = form.doi.data
            primary_attribution = form.primary_attribution.data
            conn = mysql.connect
            cur= conn.cursor()
                        # execute a query
            cur.execute(f"""INSERT INTO Publications (Year, Type, Title, Name, Status, DOI, PrimaryAttribution,ORCID)
            VALUES ({year},'{type}','{title}','{name}','{status}','{doi}','{primary_attribution}',{current_user.orcid});  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))

        return render_template('publications_info.html', form=form) # list=impacts_list
    else:
        publications_list = current_user.publications
        return render_template('publications_info.html', form=form, list=publications_list)






@app.route('/educationInfo', methods=['GET', 'POST'])
@login_required
def educationInfo():
    #Creates proposal form

    form= AddEducationForm(request.form)
    education_list = current_user.education

    if request.method == 'POST':
            #if input validates pushes to db
        if form.validate_on_submit():

                #if form.picture.data:         #image processing
                #   print("here ttt")
                #  picture_file = save_picture(form.picture.data)
                # Image.open(picture_file)
            degree = form.degree.data
            institution= form.institution.data
            location= form.location.data
            year = form.year.data
            field = form.field.data
            print(degree)
            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO Education (Degree,Institution,
            Location, Year, Field, ORCID) VALUES ('{degree}','{institution}','{location}',{year},'{field}',{current_user.orcid});  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('educationInfo'))


    return render_template('educationInfo.html', form=form, list=education_list)

@app.route('/employmentInfo', methods=['GET', 'POST'])
@login_required
def employmentInfo():
    #Creates proposal form
    form = AddEmploymentForm(request.form)
    employment_list = current_user.employment
    if request.method == 'POST':

        print(form.errors)
            #if input validates pushes to db
        if form.validate_on_submit():

                #if form.picture.data:         #image processing
                #   print("here ttt")
                #  picture_file = save_picture(form.picture.data)
                # Image.open(picture_file)
            company = form.company.data
            location= form.location.data
            years = form.years.data


            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO Employment (Company,Location,Years, ORCID) VALUES ('{company}',
            '{location}',{years},{current_user.orcid});  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('employmentInfo'))



    return render_template('employmentInfo.html', form=form, list=employment_list)


@app.route('/societiesInfo', methods=['GET', 'POST'])
@login_required
def societiesInfo():
    #Creates proposal form
    form = AddSocietiesForm(request.form)
    societies_list = current_user.societies
    if request.method == 'POST':

        print(form.errors)
            #if input validates pushes to db
        if form.validate_on_submit():

                #if form.picture.data:         #image processing
                #   print("here ttt")
                #  picture_file = save_picture(form.picture.data)
                # Image.open(picture_file)
            start_date = form.start_date.data
            end_date = form.end_date.data
            society = form.society.data
            membership = form.membership.data
            status = form.status.data


            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO Societies (StartDate, EndDate, Society, Membership, Status, ORCID) VALUES ('{start_date}',
            '{end_date}','{society}','{membership}','{status}',{current_user.orcid});  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('societiesInfo'))



    return render_template('societiesInfo.html', form=form, list=societies_list)

@app.route('/organised_events', methods=['GET', 'POST'])
@login_required
def organised_events():
    #Creates proposal form
    form = AddOrganisedEvents(request.form)
    organised_events = OrganisedEvents.query.all()
    if request.method == 'POST':

        print(form.errors)
            #if input validates pushes to db
        if form.validate_on_submit():

                #if form.picture.data:         #image processing
                #   print("here ttt")
                #  picture_file = save_picture(form.picture.data)
                # Image.open(picture_file)
            start_date = form.start_date.data
            end_date = form.end_date.data
            title = form.title.data
            type = form.type.data
            role = form.role.data
            location = form.location.data
            primary_attribution = form.primary_attribution.data

            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO OrganisedEvents (StartDate, EndDate, Title, Type, Role, Location, PrimaryAttribution, ORCID) VALUES ('{start_date}',
            '{end_date}','{title}','{type}','{role}','{location}', '{primary_attribution}','{current_user.orcid}');  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('organised_events.html', form=form)

    organised_events_list = current_user.organised_events
    print(organised_events_list)
    return render_template('organised_events.html', form=form, list=organised_events_list)


@app.route('/education_and_public_engagement', methods=['GET', 'POST'])
@login_required
def education_and_public_engagement():
    #Creates proposal form
    form = AddEducationAndPublicEngagement(request.form)
    education_and_public_engagement = EducationAndPublicEngagement.query.all()
    if request.method == 'POST':

        print(form.errors)
            #if input validates pushes to db
        if form.validate_on_submit():

                #if form.picture.data:         #image processing
                #   print("here ttt")
                #  picture_file = save_picture(form.picture.data)
                # Image.open(picture_file)
            name = form.name.data
            start_date = form.start_date.data
            end_date = form.end_date.data
            activity=  form.activity.data
            topic = form.topic.data
            target_area = form.target_area.data
            primary_attribution = form.primary_attribution.data

            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO EducationAndPublicEngagement (Name, StartDate, EndDate, Activity, Topic, TargetArea, PrimaryAttribution, ORCID) VALUES ('{name}','{start_date}','{end_date}','{activity}','{topic}','{target_area}', '{primary_attribution}','{current_user.orcid}');  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('education_and_public_engagement.html', form=form)

    education_and_public_engagement_list = current_user.edu_and_public_engagement
    print(education_and_public_engagement_list)
    return render_template('education_and_public_engagement.html', form=form, list=education_and_public_engagement_list)

@app.route('/awardsInfo', methods=['GET', 'POST'])
@login_required
def awardsInfo():

    form = AddAwardsForm(request.form)
    awards_list= current_user.awards

    if request.method == 'POST':

        print(form.errors)
            #if input validates pushes to db
        if form.validate_on_submit():


            year= form.year.data
            award_body= form.award_body.data
            details= form.details.data
            team_member = form.team_member.data




            conn = mysql.connect
            cur= conn.cursor()
                # execute a query
            cur.execute(f"""INSERT INTO Awards (Year, AwardingBody, Details, TeamMember, ORCID) VALUES ({year},
            '{award_body}','{details}','{team_member}', {current_user.orcid} );  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('awardsInfo'))


    return render_template('awardsInfo.html', form=form, list=awards_list)

@app.route('/team_members_info', methods=['GET', 'POST'])
@login_required
def team_members_info():
    #Creates proposal form
    form = AddTeamMembersForm(request.form)
    team= Team.query.filter_by(team_leader=current_user.orcid).all()
    if team==0:
        if request.method == 'POST':

            print(form.errors)
                #if input validates pushes to db
            if form.validate_on_submit():

                start_date = form.start_date.data
                departure_date = form.departure_date.data
                name = form.name.data
                position = form.position.data
                team_id = form.team_id.data
                primary_attribution = form.primary_attribution.data
                orcid = form.orcid.data




                conn = mysql.connect
                cur= conn.cursor()
                    # execute a query
                cur.execute(f"""INSERT INTO TeamMembers (StartDate, DepartureDate, Name, position,PrimaryAttribution,TeamID, ORCID) VALUES ('{start_date}',
                '{departure_date}', '{name}','{position}','{primary_attribution}', {team.team_id}, {orcid} );  """)
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('team_member_info'))
        return render_template('team_members_info.html', form=form)

   #team_members_list= TeamMembers.query.filter_by(team_id=team.team_id).all()


    if request.method == 'POST':

        print(form.errors)
                #if input validates pushes to db
        if form.validate_on_submit():

            start_date = form.start_date.data
            departure_date = form.departure_date.data
            name = form.name.data
            position = form.position.data
            team_id = form.team_id.data
            primary_attribution = form.primary_attribution.data
            orcid = form.orcid.data




            conn = mysql.connect
            cur= conn.cursor()
                    # execute a query
            cur.execute(f"""INSERT INTO TeamMembers (StartDate, DepartureDate, Name, position,PrimaryAttribution,TeamID, ORCID) VALUES ('{start_date}',
            '{departure_date}', '{name}','{position}','{primary_attribution}', {team.team_id}, {orcid} );  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
    return render_template('team_members_info.html', form=form)


@app.route('/impacts_info', methods=['GET','POST'])
@login_required
def impacts_info():
    form = AddImpactsForm()
    impacts = Impacts.query.all()
    print(impacts)

    if request.method == 'POST':
        print(form.errors)
        if form.validate_on_submit():
            title = form.title.data
            category = form.category.data
            primary_beneficiary = form.primary_beneficiary.data
            primary_attribution = form.primary_attribution.data
            impact = Impacts(title = title, category= category, primary_attribution=primary_attribution,
            primary_beneficiary=primary_beneficiary, ORCID= current_user.orcid)
            db.session.add(impact)
            db.session.commit()
        if request.method == 'POST':
            print(form.errors)
            if form.validate_on_submit():

                title = form.title.data
                category = form.category.data
                primary_beneficiary = form.primary_beneficiary.data
                primary_attribution = form.primary_attribution.data

                conn = mysql.connect
                cur = conn.cursor()
                cur.execute("""INSERT INTO Impacts (Title,Category,PrimaryBeneficiary,PrimaryAttribution, ORCID) VALUES('{title}','{category}',
                '{primary_benificiary}','{primary_attribution}', {current_user.orcid} ); """)
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('profile'))

        return render_template('impacts_info.html', form=form) # list=impacts_list
    else:
        impacts_list = current_user.impacts
        return render_template('impacts_info.html', form=form ,list=impacts_list)


@app.route('/projects')
@login_required
def projects():
    approved_submissions = Submissions.query.filter_by(user=current_user.orcid, status="Approved").all()
    all_fundings = Funding.query.filter_by(orcid=current_user.orcid).all()
    scientific_reports = Report.query.filter_by(ORCID=current_user.orcid, type="Scientific").all()
    financial_reports = Report.query.filter_by(ORCID=current_user.orcid, type="Financial").all()
    teams = Team.query.filter_by(team_leader=current_user.orcid).all()

    return render_template("projects.html", projects=approved_submissions, fundings=all_fundings, scientific_reports=scientific_reports, financial_reports=financial_reports, teams=teams)

@app.route('/manage_team', methods=["GET", "POST"])
@login_required
def manage_team():
    id = request.args.get("id")
    team = Team.query.filter_by(team_leader=current_user.orcid, subid=id).first()
    addform = AddTeamMemberForm(prefix="addform")
    createform = CreateTeamForm(prefix="createform")
    editform = EditTeamMemberForm(prefix="editform")
    deleteform = DeleteTeamMemberForm(prefix="deleteform")
    if team:
        if addform.submit.data and addform.validate():
            project = Submissions.query.filter_by(subid=id).first()
            researcher = User.query.filter_by(orcid=addform.ORCID.data).first()
            full_name = researcher.first_name + " " + researcher.last_name
            new_team_member = TeamMembers(start_date=addform.start_date.data, departure_date=addform.departure_date.data, name=full_name, position=addform.position.data, primary_attribution=project.location, ORCID=researcher.orcid, team_id=team.team_id)
            db.session.add(new_team_member)

        if deleteform.delete.data and deleteform.validate():
            orcid = request.args.get("ORCID")
            team_member = TeamMembers.query.filter_by(ORCID=orcid).first()
            db.session.delete(team_member)

        if editform.submit.data and editform.validate():
            orcid = request.args.get("ORCID")
            team_member = TeamMembers.query.filter_by(ORCID=orcid).first()
            if editform.start_date.data:
                team_member.start_date = editform.start_date.data
            if editform.departure_date.data:
                team_member.departure_date = editform.departure_date.data
            if editform.position.data:
                team_member.position = editform.position.data
            if editform.primary_attribution.data:
                team_member.primary_attribution = editform.primary_attribution.data

        db.session.commit()
        team_members = TeamMembers.query.filter_by(team_id=team.team_id).all()
        return render_template("manage_team.html", team=team, team_members=team_members, id=id, addform=addform, createform=createform, deleteform=deleteform, editform=editform)

    if createform.create.data and createform.validate():
        team = Team(team_leader=current_user.orcid, subid=id)
        print("team created")
        db.session.add(team)
        db.session.commit()
        return redirect(url_for("manage_team", team=team, id=id, addform=addform, createform=createform))

    return render_template("manage_team.html", team=team, createform=createform, id=id, addform=addform)




@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/sign_in?next=' + request.path)

@app.route('/profile')
@login_required
def profile():




    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # logs the user out
    return redirect(url_for('index'))  # or return a log out page

@app.route('/submitted')
@login_required
def submitted():
    return render_template('submitted.html')

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = ManageForm()
    if current_user.type == "Admin":
        researchers = []
        all_users = User.query.all()
        for each in all_users:
            if each.orcid != current_user.orcid:
                researchers.append(each)
        form.researcher.choices = [(user.orcid, "%s - %s %s. Role = %s" % (user.orcid, user.first_name, user.last_name, user.type)) for user in researchers]
        print(researchers)
        if request.method == "POST":
            print(form.researcher.data)
            print(form.role.data)
            if form.submit.data:
                researcher = User.query.filter_by(orcid=form.researcher.data).first()
                newRole = form.role.data
                if researcher.orcid == current_user.orcid:
                    flash("You can't change your own role unfortunately", category="unauthorised")
                    return redirect(url_for('manage'))
                if researcher.type == "Admin":
                    flash("You can't change another admin's role", category="unauthorised")
                    return redirect(url_for('manage'))
                researcher.type = newRole
                db.session.commit()
                flash("Role have been updated", category="success")
                return redirect(url_for('manage'))

            return render_template('manage.html', form=form, researchers=researchers)
        return render_template('manage.html', form=form, researchers=researchers)
    else:
        flash("You need to be an admin to manage others.", category="unauthorised")
        return redirect(url_for('manage'))

@app.route("/grants")
@login_required
def grants():
    #Show the calls that have been approved.For that user
    #For that application they need to add Team members[a link]
    #when grant is approved by admin we need to insert stuff into team table
    #the page will look like profile page
    #with application info [new page]
    #with the team info as well
    #Reports
    #fin and sci

    return render_template("grants.html")




def getProfileInfo():
    profileInfo = 0
    education = current_user.education
    employment = current_user.education
    societies = current_user.societies
    awards = current_user.awards
    funding = current_user.funding
    impacts = current_user.impacts
    inno_and_comm = current_user.inno_and_comm
    publications = current_user.publications
    presentations = current_user.presentations
    collab = current_user.collab
    organised_events = current_user.organised_events
    edu_and_public_engagement = current_user.edu_and_public_engagement
    if len(education) < 1:
        profileInfo += 1
    if len(employment) < 1:
        profileInfo += 1
    if len(societies) < 1:
        profileInfo += 1
    if len(awards) < 1:
        profileInfo += 1
    if len(funding) < 1:
        profileInfo += 1
    if len(impacts) < 1:
        profileInfo += 1
    if len(inno_and_comm) < 1:
        profileInfo += 1
    if len(publications) < 1:
        profileInfo += 1
    if len(presentations) < 1:
        profileInfo += 1
    if len(collab) < 1:
        profileInfo += 1
    if len(organised_events) < 1:
        profileInfo += 1
    if len(edu_and_public_engagement) < 1:
        profileInfo += 1
    return profileInfo

if __name__ == "__main__":
    app.run(debug=True)



