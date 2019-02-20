/*Resercher */
DROP TABLE IF EXISTS Researcher;
CREATE TABLE Researcher(
	FirstName varchar(255) NOT NULL,
	LastName VARCHAR(255) NOT NULL,
	Job varchar(255) NOT NULL,
	Prefix varchar(20) NOT NULL,
	Suffix VARCHAR(20) NOT NULL,
	Phone VARCHAR (30),
	PhoneExtension varchar(30),
	Email varchar(255) NOT NULL,
	ORCID varchar(255) NOT NULL,
	Password char(80) NOT NULL,
	Type varchar(20) NOT NULL,PRIMARY KEY (ORCID)
	);
/*Education */
DROP TABLE IF EXISTS Education;
CREATE TABLE Education(
	ORCID varchar(255) NOT NULL,
	Degree varchar(255),Field varchar(255),
	Institution varchar(255),
	Location varchar(255),
	Year int);
/*Employment */
DROP TABLE IF EXISTS Employment;
CREATE TABLE Employment(
	Company varchar(255),
	Location varchar(255),
	Years INT,
	ORCID varchar(255) NOT NULL
	);
/*Societies */
DROP TABLE IF EXISTS Societies;
CREATE TABLE Societies(
	StartDate DATE,
	EndDate DATE,
	Society VARCHAR(255),
	Membership VARCHAR(255),
	Status VARCHAR(20),
	ORCID VARCHAR(255) NOT NULL
	);
/*Award */
DROP TABLE IF EXISTS Awards;
CREATE TABLE Awards(
	Year INT,
	AwardingBody VARCHAR(255),
	Details VARCHAR(255),
	TeamMember VARCHAR(255),
	ORCID VARCHAR(255) NOT NULL
	);
/*Funding */
DROP TABLE IF EXISTS Funding;
CREATE TABLE Funding(
	StartDate DATE,
	EndDate DATE,
	AmountFunding int,
	FundingBody VARCHAR(255),
	FundingProgramme VARCHAR(255),
	Stats VARCHAR(255),
	PrimaryAttribution VARCHAR(255),
	ORCID VARCHAR(255) NOT NULL
	);
/*TeamMembers */
DROP TABLE IF EXISTS TeamMembers;
CREATE TABLE TeamMembers(
	StartDate DATE,
	DepartureDate DATE,
	Name VARCHAR(255),
	Position VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL
	);
/*Impacts */
DROP TABLE IF EXISTS Impacts;
CREATE TABLE Impacts(
	Title VARCHAR(255),
	Category VARCHAR(255),
	PrimaryBeneficiary VARCHAR(255) NOT NULL,
	PrimaryAttribution VARCHAR(255) NOT NULL
	);
/*InnovationAndCommercialisation */
DROP TABLE IF EXISTS InnovationAndCommercialisation;
CREATE TABLE InnovationAndCommercialisation(
	Year int,
	Type VARCHAR(255),
	Title VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL
	);
/*Publications */
DROP TABLE IF EXISTS Publications;
CREATE TABLE Publications(
	Year int,
	Type VARCHAR(255),
	Title VARCHAR(255),
	Name VARCHAR(255),
	Status VARCHAR(255),
	DOI VARCHAR(255) NOT NULL, 
	PrimaryAttribution VARCHAR(255) NOT NULL,
	PRIMARY KEY (DOI));
/*Presentations */
DROP TABLE IF EXISTS Presentations;
CREATE TABLE Presentations(
	Year int,
	Title VARCHAR(255),
	Type VARCHAR(255),
	Conference VARCHAR(255),
	InvitedSeminar VARCHAR(255),
	Keynote VARCHAR(255),
	OrganisingBody VARCHAR(255),
	Location VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL
	);
/*Collaborations */
DROP TABLE IF EXISTS Collaborations;
CREATE TABLE Collaborations(
	StartDate DATE,
	EndDate DATE,
	Institution VARCHAR(255),
	Department VARCHAR(255),
	Location VARCHAR(255),
	NameCollaborator VARCHAR(255),
	PrimaryGoal VARCHAR(255),
	FrequencyOfInteraction VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL, 
	Academic Boolean);
/*OrganisedEvents */
DROP TABLE IF EXISTS OrganisedEvents;
CREATE TABLE OrganisedEvents(
	StartDate DATE,
	EndDate DATE,
	Title VARCHAR(255),
	Type VARCHAR(255),
	Role VARCHAR(255),
	Location VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL);
/*EducationAndPublicEngagement */
DROP TABLE IF EXISTS EducationAndPublicEngagement;
CREATE TABLE EducationAndPublicEngagement(
	Name VARCHAR(255),
	StartDate DATE,
	EndDate DATE,
	Activity VARCHAR(255),
	Topic VARCHAR(255),
	TargetArea VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL);
/*Submission */
DROP TABLE IF EXISTS Submission; 
CREATE TABLE Submission (
	propid INT not null,
 	subid int not null primary key AUTO_INCREMENT,
 	title varchar(255) NOT NULL,
  	duration int not null,
  	NRP varchar(1000) NOT NULL,
    legal TEXT NOT NULL,
    ethicalAnimal TEXT NOT NULL,
    ethicalHuman TEXT NOT NULL,
    location TEXT NOT NULL,
    coapplicants TEXT, 
    collaborators TEXT, 
    scientific TEXT NOT NULL,
    lay TEXT NOT NULL,
    declaration BOOLEAN NOT NULL,
    user varchar(255) NOT NULL,
  	draft Boolean default True,
  	proposalPDF varchar(255) NOT NULL);