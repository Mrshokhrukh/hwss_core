CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Role TEXT NOT NULL,
    LocationID INTEGER,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

CREATE TABLE Locations (
    LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
    LocationName TEXT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SurveyData (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ParticipantName TEXT,
    Age INTEGER,
    Gender TEXT,
    ContactNumber TEXT,
    Email TEXT,
    ResidentialAddress TEXT,
    HealthFacilityName TEXT,
    ServiceType TEXT,
    ServiceDate DATE,
    Feedback TEXT,
    HIVStatus TEXT,
    RiskGroup TEXT,
    MedicationDetails TEXT,
    FollowUpDate DATE,
    MaritalStatus TEXT,
    EmploymentStatus TEXT,
    EducationLevel TEXT,
    Ethnicity TEXT,
    Languages TEXT,
    Disability TEXT,
    InsuranceStatus TEXT,
    PreviousServiceUsage TEXT,
    TravelTime INTEGER,
    TransportMode TEXT,
    TreatmentChallenges TEXT,
    DietInfo TEXT,
    ExerciseHabits TEXT,
    SmokingAlcoholUse TEXT,
    MentalHealthStatus TEXT,
    SafetyConcerns TEXT,
    CommunitySupport TEXT,
    HealthAwareness TEXT,
    ImprovementSuggestions TEXT,
    UserID INTEGER,
    LocationID INTEGER,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);


CREATE TABLE Settings (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    SettingKey TEXT NOT NULL,
    SettingValue TEXT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
