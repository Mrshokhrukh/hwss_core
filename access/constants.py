import os

GLOBAL_FILE_PATH = os.path.join(os.path.dirname(__file__), "global.json")

USER_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "user_data.json")
AGENCY_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "agency_data.json")

ROLE_STUDENT = "student"
ROLE_PUBLIC = "general_public"
ROLE_CLINICAL_COUNSELOR = "clinical_counselor"
ROLE_GYALSUNG_COUNSELOR = "gyalsung_counselor"
ROLE_SCHOOL_COUNSELOR = "school_counselor"
ROLE_TRAINED_PROFESSIONAL = "trained_professional"
ROLE_ADMIN = "mh_admin"
ROLE_RD_ADMIN = "rd_admin"
ROLE_SUD_ADMIN = "sud_admin"
ROLE_AAA_ADMIN = "aaa_admin"
ROLE_CECD_ADMIN = "cecd_admin"
ROLE_PSYCHIATRIST = "psychiatrist"
ROLE_MEDICAL_OFFICER = "medical_officer"
ROLE_REASSESMENT_TEAM = "reassesment_team"
ROLE_GYALSUNG_REASSESSMENT_TEAM = "gyalsung_reassessment_team" 

ROLE_CHOICES = [
    (ROLE_STUDENT, "Student"),
    (ROLE_PUBLIC, "General Public"),
    (ROLE_CLINICAL_COUNSELOR, "Clinical Counselor"),
    (ROLE_GYALSUNG_COUNSELOR, "Gyalsung Counselor"),
    (ROLE_SCHOOL_COUNSELOR, "School Counselor"),
    (ROLE_TRAINED_PROFESSIONAL, "Trained Professional"),
    (ROLE_ADMIN, "Mental Health Care Admin"),
    (ROLE_RD_ADMIN, "R&D Admin"),
    (ROLE_SUD_ADMIN, "SUD Admin"),
    (ROLE_AAA_ADMIN, "AAA Admin"),
    (ROLE_CECD_ADMIN, "CECD Admin"),
    (ROLE_PSYCHIATRIST, "Psychiatrist"),
    (ROLE_MEDICAL_OFFICER, "Medical Officer"),
    (ROLE_REASSESMENT_TEAM, "Reassesment Team"),
    (ROLE_GYALSUNG_REASSESSMENT_TEAM, "Gyalsung Reassessment Team"),
    
]
REGISTRATION_METHOD_CHOICES = [
    ("cluster_registration", "Clustered Registered"),
    ("case_registration", "Counselor Case Registered"),
    ("event_registration", "Counselor Event Registered"),
    (
        "gyalsung_registration",
        "Gyalsung Registered",
    ),
    ("unknown_registration", "Unknown/Legacy"),
]
GYALSUNG_STATUS = [
    ("", ""),
    ("registered", "Registered"),
    ("screened", "Screened"),
    ("pending", "Pending"),
    ("completed", "Completed"),
]
