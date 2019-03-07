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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Authorised Personnel Only.'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://seintu:0mYkNrVI0avq@mysql.netsoc.co/seintu_project2'  # set the database directory
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

#setup for proposal call form
app.config["MYSQL_HOST"] = "mysql.netsoc.co"
app.config["MYSQL_USER"] = "seintu"
app.config["MYSQL_PASSWORD"] = "0mYkNrVI0avq"
app.config["MYSQL_DB"] = "seintu_project2"
mysql = MySQL(app)
mysql.init_app(app)



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


    def __init__(self, Deadline, title, TextOfCall, TargetAudience, EligibilityCriteria, Duration, ReportingGuidelines, TimeFrame, picture):
        self.Deadline = Deadline
        self.title = title
        self.TextOfCall = TextOfCall
        self.TargetAudience = TargetAudience
        self.EligibilityCriteria = EligibilityCriteria
        self.Duration = Duration
        self.ReportingGuidelines = ReportingGuidelines
        self.TimeFrame = TimeFrame
        self.picture = picture

    def __repr__(self):
        return f"User('{self.Dealine}', '{self.TargetAudience}', '{self.TimeFrame}')"

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
    PrimaryAttribution = db.Column(db.String(255), nullable=False, primary_key=True)
    orcid = db.Column(db.Integer, db.ForeignKey('Researcher.orcid'), nullable=False)

    def __init__(self, StartDate, EndDate, AmountFunding, FundingBody, FundingProgramme, Status, PrimaryAttribution, orcid):
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.AmountFunding = AmountFunding
        self.FundingBody = FundingBody
        self.FundingProgramme = FundingProgramme
        self.Status = Status
        self.PrimaryAttribution = PrimaryAttribution
        self.orcid = orcid

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

class Team(db.Model):
    __tablename__ = "Team"
    team_id = db.Column("TeamID", db.Integer, primary_key=True)
    team_leader = db.Column("TeamLeader", db.Integer, db.ForeignKey('Researcher.orcid'))
    propasal_id = db.Column("ProposalID", db.Integer, db.ForeignKey('Proposal.id'))

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
    doi = db.Column("DOI", db.String(255), primary_key=True)
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
    #same as funding




# Below are the form classes that inherit the FlaskForm class.
# You can set the requirements for each attribute here instead of doing it in the html file
class LoginForm(FlaskForm):
    # this is the class for the login form in the sign_in.html
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


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

class UpdateEmploymentForm(FlaskForm):
    id = StringField('ID:', validators=[ Length(max=50)])
    company = StringField('Company:', validators=[ Length(max=50)])
    location = StringField('Location:', validators=[ Length(max=50)])
    years = IntegerField('Years:')
    submit_emp = SubmitField('Edit Employment')
    remove_emp = SubmitField('Remove')



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
    



class AddAwardsForm(FlaskForm):

	year = IntegerField('Year:')
	award_body = StringField('Awarding Body:', validators=[ Length(max=50)])
	details = StringField('Detail:', validators=[Length(max=50)])
	team_member = StringField('Team Member ', validators=[Length(max=50)])
	submit = SubmitField('Add')


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


@login_manager.user_loader
def load_user(user_id):
    # this is a function that callsback the user by the user_id
    return User.query.get(int(user_id))


def mail(receiver, content="", email="", password=""):
    #function provides default content message, sender's email, and password but accepts
    #them as parameters if given
    #for now it sends an email to all researchers(i hope) not sure how im supposed to narrow it down yet
	#cur = mysql.get_db().cursor()
    #cur.execute("SELECT email FROM researchers")
    #rv = cur.fetchall()
    if not content:
        content = "Account made confirmation message"
    if not email:
        email = "team9sendermail@gmail.com"
    if not password:
        password = "default password"

        password = "team9admin"
	
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email, password)
    #for email in rv:
    mail.sendmail(email, receiver,content)
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

@app.route('/scientific_reports')
@login_required
def scientific_reports():
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
            file.save('uploads/'+filename)
            filenamesecret = uuid.uuid4().hex
            print("file saved")

        newReport = Report(title=form.title.data, type="Scientific", pdf=filenamesecret, ORCID=current_user.orcid)
        db.session.add(newReport)
        db.session.commit()
        return redirect(url_for('scientific_reports'))
    return render_template("scientific_reports.html", reports=s_reports, form=form)
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

@app.route('/financial_reports')
@login_required
def financial_reports():
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
            file.save('uploads/'+filename)
            filenamesecret = uuid.uuid4().hex
            print("file saved")

        newReport = Report(title=form.title.data, type="Financial", pdf=filenamesecret, ORCID=current_user.orcid)
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
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("completed_reviews.html",form=form,sub=sub,rev=rev,prop=prop)


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

    elif form.ORCID.data!=None:
        print("here")
        #database push external review link to user
        new_external_review=ExternalPendingReviews(post,form.ORCID.data,False)
        db.session.add(new_external_review)
        db.session.commit()
    if form.complete.data:
        #change submission to external review when done button is pressed
        i.status="review"
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("dashboard"))



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
    conn = mysql.connect
    cur = conn.cursor()
    # execute a query

    cur.execute("""
                SELECT *
                FROM Proposal;
                """)
    for i in cur.fetchall():
        post={}
        post["id"] = i[0]
        post["deadline"] = i[1]
        post["text"] = i[2]
        post["audience"] = i[3]
        post["eligibility"] = i[4]
        post["duration"] = i[5]
        post["guidelines"] = i[6]
        post["timeframe"] = i[7]
        posts.append(post)
    conn.commit()

    cur.close()
    conn.close()
    return render_template('create_submission_form.html', user=current_user, posts=posts)
# @app.route('/resetpassword')

@app.route('/proposals', methods=['GET' , 'POST'])
@login_required
def proposals():
    posts = []
    conn = mysql.connect
    cur = conn.cursor()
    # execute a query

    cur.execute("""
                 SELECT *
                 FROM Proposal;
                 """)
    for i in cur.fetchall():
        post = {}
        print(i)
        post["id"] = i[9]
        post["deadline"] = i[0]
        post["text"] = i[2]
        post["audience"] = i[3]
        post["eligibility"] = i[4]
        post["duration"] = i[5]
        post["guidelines"] = i[6]
        post["timeframe"] = i[7]
        post["title"] = i[1]
        posts.append(post)
    conn.commit()

    cur.close()
    conn.close()
    return render_template('proposals.html', user=current_user, posts=posts)

@app.route('/submissions',methods=['GET' , 'POST'])
@login_required
def submissions():
    #fix request shit
    sub={}
    form=Submission_Form()
    post=request.args.get("id")
    form.setPropId(post)
    conn = mysql.connect
    cur = conn.cursor()
    previousFile=None
    cur.execute(f"""
                             SELECT *
                             FROM Submission
                             WHERE propid = {post} AND user='{current_user.orcid}';
                             """)
    for i in cur.fetchall():
        if i[15]==0:
            return render_template("submitted.html")
        form.propid=i[0]
        form.title.data=i[2]
        form.duration.data=i[3]
        form.NRP.data=i[4]
        form.legal_remit.data=i[5]
        form.ethical_animal.data=i[6]
        form.ethical_human.data=i[7]
        form.location.data=i[8]
        form.co_applicants.data=i[9]
        form.collaborators.data=i[10]
        form.scientific_abstract.data=i[11]
        form.lay_abstract.data=i[12]
        form.declaration.data=i[13]
        previousFile=i[16]



    cur.close()
    conn.close()


    if form.validate_on_submit():
        if form.validate.data:
            flash("Input Successfully Validated")
        elif form.draft.data:
            filenamesecret=previousFile
            if form.proposalPDF.data != None:
                filenamesecret = uuid.uuid4().hex
                while True:
                    filecheck = Path(f"uploads/{filenamesecret}")
                    if filecheck.is_file():
                        filenamesecret = uuid.uuid4().hex
                    else:
                        break
                form.proposalPDF.data.save('uploads/' + filenamesecret)
                if previousFile!=None:
                    os.remove(f"uploads/{previousFile}")



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
            return redirect(url_for("submissions",id=form.propid,sub=sub))
        elif form.submit.data:
            filenamesecret = previousFile
            if form.proposalPDF.data!=None:
                filenamesecret = uuid.uuid4().hex
                while True:
                    filecheck=Path(f"uploads/{filenamesecret}")
                    if filecheck.is_file():
                        filenamesecret = uuid.uuid4().hex
                    else:
                        break
                form.proposalPDF.data.save('uploads/' + filenamesecret)
                if previousFile != None:
                    os.remove(f"uploads/{previousFile}")


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
            return redirect(url_for("submissions", id=form.propid, sub=sub))



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

    return render_template('submissions.html', user=current_user, sub=sub,form=form)

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
        form.pdfReview.data.save('uploads/' + filenamesecret)
        sub=Submissions.query.filter_by(proposalPDF=file).first()
        new_review = ExternalReview(sub.subid,current_user.orcid,True,filenamesecret)
        sub.status="Approval Pending"
        db.session.add(new_review)
        db.session.commit()

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


            conn = mysql.connect
            cur = conn.cursor()
            # execute a query
            cur.execute("""INSERT INTO Proposal(Deadline,Title, TextOfCall, TargetAudience, EligibilityCriteria, Duration, ReportingGuidelines, TimeFrame)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",(deadline,title, textofcall, targetaudience, eligibilitycriteria, duration, reportingguidelines, timeframe))
            # rv contains the result of the execute
            conn.commit()
            cur.close()
            conn.close()
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
    user = current_user
    print(user.societies)
    
    if request.method == 'POST':

        #print(update_general.errors)
        #if input validates pushes to db
        # 
        if update_general.validate_on_submit() :

            first_name = update_general.first_name.data
            last_name = update_general.last_name.data
            email = update_general.email.data
            job = update_general.job.data
            prefix = update_general.prefix.data
            suffix = update_general.suffix.data
            phone = update_general.phone.data
            phone_extension = update_general.phone_extension.data

            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""UPDATE Researcher SET FirstName='{first_name}', LastName='{last_name}', Job='{job}', Prefix='{prefix}', Suffix='{suffix}',
                    Phone={phone}, PhoneExtension={phone_extension}, Email='{email}' WHERE ORCID ={current_user.orcid};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))


        
       # Edit societies
        elif update_societies.validate_on_submit and "submit_soc" in request.form:
            print("here")
            start_date = update_societies.start_date.data
            end_date = update_societies.end_date.data
            society = update_societies.society.data
            membership = update_societies.membership.data
            status = update_societies.status.data
            id1 = update_societies.id.data
            

            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""UPDATE Societies SET StartDate= '{start_date}', EndDate='{end_date}', Society = '{society}', Membership = '{membership}',
            Status = '{status}' WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('societiesInfo'))
        # Remove societies
        elif update_societies.validate_on_submit and "remove_soc" in request.form:
            print("here")
            
            id1 = update_societies.id.data
        
            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Societies WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('edit_info'))
        # Edit Education
        elif update_education.validate_on_submit and "submit_edu" in request.form:
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
        elif update_education.validate_on_submit and "remove_edu" in request.form:
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
        elif update_employment.validate_on_submit and "submit_emp" in request.form:
            company = update_employment.company.data
            location = update_employment.location.data
            years = update_employment.years.data
            id2 = update_employment.id.data

            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""UPDATE Employment SET Company = '{company}',  Location= '{location}',
             Years= {years}  WHERE ID ={id2};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('employmentInfo'))
        #Remove Employment
        elif update_employment.validate_on_submit and "remove_emp" in request.form:
            print("here")
            
            id1 = update_employment.id.data
        
            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Employment WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('edit_info'))

        #Edit Awards
        elif update_awards.validate_on_submit and "submit_awrd" in request.form:
            year = update_awards.year.data
            award_body = update_awards.award_body.data
            details = update_awards.details.data
            team_member = update_awards.team_member.data
            id3 = update_awards.id.data

            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""UPDATE Awards SET Year = {year}, AwardingBody = '{award_body}', Details = '{details}',TeamMember = '{team_member}' WHERE ID ={id3};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('awardsInfo'))
        #Remove Awards
        elif update_awards.validate_on_submit and "remove_awrd" in request.form:
            print("here")
            
            id1 = update_awards.id.data
        
            conn = mysql.connect
            cur= conn.cursor()
            # execute a query
            cur.execute(f"""DELETE FROM Awards WHERE ID ={id1};  """)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('edit_info'))

   
            
       
        
    return render_template('edit_info.html', form1=update_general, form2=update_education , form3=update_societies, form4 = update_employment,
    form5 = update_awards, user=user)




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


@app.route('/publications_info', methods=['GET','POST'])
@login_required
def publications_info():
    form = AddPublications(request.form)
    publications = Publications.query.all()
    if len(publications) ==0:
        if request.method =='POST':
            if form.validate_on_submit():
                
                year = form.year.data
                type = form.type.data
                title = form.title.data
                name = form.name.data
                status = form.status.data
                doi = form.doi.data
                primary_attribution = form.primary_attribution
                cur= conn.cursor()
                        # execute a query
                cur.execute(f"""INSERT INTO Publications (Year, Type, Title, Name, Status, DOI, PrimaryAttribution,ORCID) 
                VALUES ({year},'{type}','{title}',{name},'{status}','{doi}','{primary_attribution}'',{current_user.orcid});  """)
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
    if len(impacts) == 0:

        
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



def getProfileInfo():
    #for the demo the profileInfo will start at -9
    profileInfo = -9
    education = current_user.education
    employment = current_user.education
    societies = current_user.societies
    awards = current_user.awards
    funding = current_user.funding
    team_members = current_user.team_members
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
    if len(team_members) < 1:
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
