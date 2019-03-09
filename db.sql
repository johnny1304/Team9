/*Researcher */
DROP TABLE IF EXISTS Researcher;
CREATE TABLE Researcher(
	FirstName varchar(255) NOT NULL,
	LastName VARCHAR(255) NOT NULL,
	Job varchar(255) NOT NULL,
	Prefix varchar(20) NOT NULL,
	Suffix VARCHAR(20) NOT NULL,
	Phone int (30),
	PhoneExtension int(30),
	Email varchar(255) NOT NULL,
	ORCID int NOT NULL,
	Password char(80) NOT NULL,
	Type varchar(20) NOT NULL,
	PRIMARY KEY (ORCID)
);
/*Education */
DROP TABLE IF EXISTS Education;
CREATE TABLE Education(
	ID int NOT NULL AUTO_INCREMENT,
	ORCID int NOT NULL,
	Degree varchar(255),Field varchar(255),
	Institution varchar(255),
	Location varchar(255),
	Year int,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Employment */
DROP TABLE IF EXISTS Employment;
CREATE TABLE Employment(
	ID int NOT NULL AUTO_INCREMENT,
	Company varchar(255),
	Location varchar(255),
	Years INT,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Societies */
DROP TABLE IF EXISTS Societies;
CREATE TABLE Societies(
	ID int NOT NULL AUTO_INCREMENT,
	StartDate DATE,
	EndDate DATE,
	Society VARCHAR(255),
	Membership VARCHAR(255),
	Status VARCHAR(20),
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Award */
DROP TABLE IF EXISTS Awards;
CREATE TABLE Awards(
	ID int NOT NULL AUTO_INCREMENT,
	Year INT,
	AwardingBody VARCHAR(255),
	Details VARCHAR(255),
	TeamMember VARCHAR(255),
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Funding */
DROP TABLE IF EXISTS Funding;
CREATE TABLE Funding(
	ID int NOT NULL AUTO_INCREMENT,
	StartDate DATE,
	EndDate DATE,
	AmountFunding int,
	FundingBody VARCHAR(255),
	FundingProgramme VARCHAR(255),
	Stats VARCHAR(255),
	PrimaryAttribution VARCHAR(255),
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Team*/
DROP TABLE IF EXIST Team;
CREATE TABLE Team(
	ID int NOT NULL AUTO_INCREMENT,
	TeamID int NOT NULL AUTO_INCREMENT,
	TeamLeader int NOT NULL,
	proposalID int NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*TeamMembers */
DROP TABLE IF EXISTS TeamMembers;
CREATE TABLE TeamMembers(
	ID int NOT NULL AUTO_INCREMENT,
	StartDate DATE,
	DepartureDate DATE,
	Name VARCHAR(255),
	Position VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Impacts */
DROP TABLE IF EXISTS Impacts;
CREATE TABLE Impacts(
	ID int NOT NULL AUTO_INCREMENT,
	Title VARCHAR(255),
	Category VARCHAR(255),
	PrimaryBeneficiary VARCHAR(255) NOT NULL,
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*InnovationAndCommercialisation */
DROP TABLE IF EXISTS InnovationAndCommercialisation;
CREATE TABLE InnovationAndCommercialisation(
	ID int NOT NULL AUTO_INCREMENT,
	Year int,
	Type VARCHAR(255),
	Title VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
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
	ORCID int NOT NULL,
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
	PRIMARY KEY (DOI)
);
/*Presentations */
DROP TABLE IF EXISTS Presentations;
CREATE TABLE Presentations(
	ID int NOT NULL AUTO_INCREMENT,
	Year int,
	Title VARCHAR(255),
	Type VARCHAR(255),
	Conference VARCHAR(255),
	InvitedSeminar VARCHAR(255),
	Keynote VARCHAR(255),
	OrganisingBody VARCHAR(255),
	Location VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Collaborations */
DROP TABLE IF EXISTS Collaborations;
CREATE TABLE Collaborations(
	ID int NOT NULL AUTO_INCREMENT,
	StartDate DATE,
	EndDate DATE,
	Institution VARCHAR(255),
	Department VARCHAR(255),
	Location VARCHAR(255),
	NameCollaborator VARCHAR(255),
	PrimaryGoal VARCHAR(255),
	FrequencyOfInteraction VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL, 
	Academic Boolean,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*OrganisedEvents */
DROP TABLE IF EXISTS OrganisedEvents;
CREATE TABLE OrganisedEvents(
	ID int NOT NULL AUTO_INCREMENT,
	StartDate DATE,
	EndDate DATE,
	Title VARCHAR(255),
	Type VARCHAR(255),
	Role VARCHAR(255),
	Location VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*EducationAndPublicEngagement */
DROP TABLE IF EXISTS EducationAndPublicEngagement;
CREATE TABLE EducationAndPublicEngagement(
	ID int NOT NULL AUTO_INCREMENT,
	Name VARCHAR(255),
	StartDate DATE,
	EndDate DATE,
	Activity VARCHAR(255),
	Topic VARCHAR(255),
	TargetArea VARCHAR(255),
	PrimaryAttribution VARCHAR(255) NOT NULL,
	ORCID int NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);
/*Submission */
DROP TABLE IF EXISTS Submission; 
CREATE TABLE Submission (
	propid INT NOT NULL,
 	subid int NOT NULL PRIMARY KEY AUTO_INCREMENT,
 	title varchar(255) NOT NULL,
  	duration int NOT NULL,
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
  	draft Boolean DEFAULT True,
  	proposalPDF varchar(255) NOT NULL
	ORCID int NOT NULl,
	FOREIGN KEY (ORCID) REFERENCES Researcher (ORCID)
);