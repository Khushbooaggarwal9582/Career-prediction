"""Seed domain-specific career roadmaps into MongoDB.

The ML model predicts one of the 55 career titles used below.  Every predicted
career has its OWN roadmap; there are no tech-roadmap fallbacks for non-tech
roles.

Run:
    pip install -r requirements.txt
    python seed_mongodb.py

Set MONGO_URI / MONGO_DB / MONGO_COLLECTION for MongoDB Atlas or another server.
"""

import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "career_compass")
COLLECTION = os.getenv("MONGO_COLLECTION", "roadmaps")


def p(title, skill, project):
    return (title, skill, project)


ROADMAPS = {
    # ---------------- Technology ----------------
    "AI Engineer": [
        p("Python Foundations", "Python", "Python Automation Toolkit"),
        p("Statistics & Probability", "Statistics", "Data Analysis Mini Project"),
        p("Machine Learning Fundamentals", "Machine_Learning", "House Price Predictor"),
        p("Deep Learning Basics", "Deep_Learning", "Image Classification Project"),
        p("Generative AI & Model APIs", "Generative_AI", "AI Assistant Prototype"),
        p("Deployment & MLOps Basics", "Cloud", "Deployed AI Application"),
    ],
    "Data Analyst": [
        p("Excel & Data Cleaning", "Excel", "Sales Data Cleanup"),
        p("SQL for Analytics", "SQL", "Business KPI Queries"),
        p("Statistics Fundamentals", "Statistics", "A/B Test Analysis"),
        p("Python for Data Analysis", "Python", "EDA Notebook"),
        p("Dashboards & Visualization", "Data_Visualization", "Interactive Sales Dashboard"),
        p("Business Storytelling", "Communication", "Analytics Case Study"),
    ],
    "Data Scientist": [
        p("Python for Data Science", "Python", "EDA Portfolio Project"),
        p("Statistics & Probability", "Statistics", "Experiment Analysis"),
        p("SQL & Data Wrangling", "SQL", "Customer Analytics Database"),
        p("Machine Learning", "Machine_Learning", "Churn Prediction"),
        p("Model Evaluation & Feature Engineering", "Machine_Learning", "Model Comparison Study"),
        p("End-to-End Data Science Project", "Communication", "Published Case Study"),
    ],
    "Software Architect": [
        p("Programming & OOP", "OOP", "Modular Application"),
        p("Data Structures & Algorithms", "DSA", "DSA Portfolio"),
        p("Databases & Data Modeling", "DBMS", "Database Design Project"),
        p("System Design Fundamentals", "System_Design", "Scalable Service Design"),
        p("Distributed Systems Concepts", "System_Design", "Service Architecture Case Study"),
        p("Architecture Documentation & Trade-offs", "Communication", "Architecture Portfolio"),
    ],
    "Software Developer": [
        p("Programming Fundamentals", "Programming", "Console Application"),
        p("OOP & Clean Code", "OOP", "Library Management System"),
        p("DSA", "DSA", "Problem Solving Portfolio"),
        p("DBMS & SQL", "DBMS", "CRUD Application"),
        p("Git & Team Development", "Git", "Collaborative Project"),
        p("Full Application Project", "Communication", "Deployable Portfolio App"),
    ],
    "Software Engineer": [
        p("Programming & OOP", "OOP", "Library Management System"),
        p("Data Structures & Algorithms", "DSA", "DSA Portfolio"),
        p("DBMS & SQL", "DBMS", "Database-Driven App"),
        p("APIs & Backend Fundamentals", "APIs", "REST API Project"),
        p("Testing & Git Workflow", "Git", "Tested Team Project"),
        p("System Design & Interview Prep", "System_Design", "System Design Case Study"),
    ],
    "System Analyst": [
        p("Requirement Gathering", "Requirements", "Requirements Document"),
        p("Process Mapping & UML", "Analysis", "Business Process Model"),
        p("SQL & Data Analysis", "SQL", "Data Investigation Project"),
        p("Systems Analysis", "Systems_Analysis", "System Specification"),
        p("Stakeholder Communication", "Communication", "Stakeholder Presentation"),
        p("Capstone Systems Case Study", "Analysis", "End-to-End Analysis Portfolio"),
    ],
    "Web Developer": [
        p("HTML & Semantic Web", "HTML", "Responsive Personal Site"),
        p("CSS & Responsive Design", "CSS", "Responsive Landing Page"),
        p("JavaScript Fundamentals", "JavaScript", "Interactive Web App"),
        p("React / Frontend Frameworks", "React", "React Dashboard"),
        p("APIs & State Management", "APIs", "API-Powered Web App"),
        p("Testing, Deployment & Portfolio", "Git", "Deployed Portfolio Website"),
    ],

    # ---------------- Finance ----------------
    "Accountant": [
        p("Accounting Fundamentals", "Accounting", "Journal & Ledger Workbook"),
        p("Financial Statements", "Financial_Reporting", "Income Statement Project"),
        p("Excel for Accounting", "Excel", "Automated Accounting Workbook"),
        p("Tax & Compliance Fundamentals", "Compliance", "Compliance Checklist Project"),
        p("Accounting Software Workflow", "Accounting_Systems", "Bookkeeping Simulation"),
        p("Financial Reporting Case Study", "Communication", "Annual Report Analysis"),
    ],
    "Auditor": [
        p("Accounting Foundations", "Accounting", "Trial Balance Review"),
        p("Internal Controls", "Audit", "Control-Mapping Exercise"),
        p("Audit Evidence & Documentation", "Audit", "Audit Working Paper"),
        p("Risk Assessment", "Risk_Management", "Risk Register"),
        p("Compliance & Professional Ethics", "Compliance", "Compliance Case Study"),
        p("Audit Analytics", "Data_Analysis", "Audit Data Review"),
    ],
    "Clerk": [
        p("Office & Record Management", "Administration", "Digital Filing System"),
        p("Excel & Data Entry", "Excel", "Records Workbook"),
        p("Document Accuracy & Quality", "Quality", "Document QA Checklist"),
        p("Basic Accounting Support", "Accounting", "Invoice Register"),
        p("Communication & Customer Handling", "Communication", "Service Workflow"),
        p("Office Process Improvement", "Process_Improvement", "Process Improvement Proposal"),
    ],
    "Finance Manager": [
        p("Corporate Finance Fundamentals", "Finance", "Financial Planning Workbook"),
        p("Budgeting & Forecasting", "Budgeting", "Department Budget Model"),
        p("Financial Analysis", "Financial_Analysis", "Company Performance Analysis"),
        p("Risk Management", "Risk_Management", "Risk Dashboard"),
        p("Leadership & Decision Making", "Leadership", "Management Case Study"),
        p("Strategic Financial Planning", "Strategy", "Strategic Finance Presentation"),
    ],
    "Financial Analyst": [
        p("Excel for Financial Analysis", "Excel", "Financial Model Workbook"),
        p("Accounting & Financial Statements", "Accounting", "Statement Analysis"),
        p("Financial Ratios & Valuation", "Valuation", "Company Valuation Case"),
        p("Forecasting & Scenario Analysis", "Forecasting", "Forecast Model"),
        p("Risk & Portfolio Basics", "Risk_Management", "Risk Analysis Report"),
        p("Investment Research Presentation", "Communication", "Equity Research Style Report"),
    ],
    "Junior Assistant": [
        p("Office Administration", "Administration", "Office Workflow Map"),
        p("Excel & Documentation", "Excel", "Administrative Tracker"),
        p("Scheduling & Records", "Organization", "Scheduling System"),
        p("Basic Finance & Billing Support", "Accounting", "Billing Register"),
        p("Communication & Professional Skills", "Communication", "Professional Email Portfolio"),
        p("Process Improvement", "Process_Improvement", "Simple Process Improvement Plan"),
    ],
    "Senior Accountant": [
        p("Advanced Financial Accounting", "Accounting", "Financial Close Workbook"),
        p("Financial Statement Analysis", "Financial_Reporting", "Annual Report Review"),
        p("Tax & Compliance", "Compliance", "Compliance Review Project"),
        p("Budgeting & Variance Analysis", "Budgeting", "Variance Analysis Model"),
        p("Accounting Controls & Audit Coordination", "Audit", "Internal Control Review"),
        p("Management Reporting", "Communication", "Management Reporting Pack"),
    ],

    # ---------------- Business ----------------
    "Analyst": [
        p("Business Fundamentals", "Business", "Business Model Summary"),
        p("Excel & Data Analysis", "Excel", "KPI Analysis Workbook"),
        p("Problem Structuring", "Analysis", "Business Problem Tree"),
        p("Market & Competitor Research", "Research", "Competitor Analysis"),
        p("Data Storytelling", "Communication", "Insight Presentation"),
        p("Business Case Study", "Strategy", "Recommendation Deck"),
    ],
    "Assistant Manager": [
        p("Business Operations", "Operations", "Process Map"),
        p("Team Coordination", "Leadership", "Team Planning Exercise"),
        p("Excel & Reporting", "Excel", "Operations Dashboard"),
        p("Customer & Stakeholder Management", "Communication", "Stakeholder Plan"),
        p("Problem Solving & Decision Making", "Decision_Making", "Operations Case Study"),
        p("Leadership Practice", "Leadership", "Team Improvement Proposal"),
    ],
    "Business Analyst": [
        p("Business Analysis Fundamentals", "Analysis", "Business Requirement Document"),
        p("Excel & Data Analysis", "Excel", "KPI Dashboard"),
        p("SQL for Business", "SQL", "Business Data Queries"),
        p("Requirements & Process Modeling", "Requirements", "Process Model"),
        p("Stakeholder Communication", "Communication", "Stakeholder Presentation"),
        p("Business Case Capstone", "Strategy", "Business Case Recommendation"),
    ],
    "Consultant": [
        p("Consulting Problem Solving", "Problem_Solving", "Issue Tree"),
        p("Research & Market Analysis", "Research", "Market Landscape"),
        p("Data Analysis with Excel", "Excel", "Consulting Analysis Workbook"),
        p("Structured Communication", "Communication", "Executive Slide Deck"),
        p("Strategy & Recommendations", "Strategy", "Strategy Case Study"),
        p("Client Presentation Skills", "Presentation", "Mock Client Presentation"),
    ],
    "Customer Support Executive": [
        p("Customer Service Fundamentals", "Customer_Service", "Support Process Map"),
        p("Communication Skills", "Communication", "Customer Response Library"),
        p("Ticketing & CRM Basics", "CRM", "Support Ticket Workflow"),
        p("Problem Resolution", "Problem_Solving", "Resolution Playbook"),
        p("Customer Feedback Analysis", "Data_Analysis", "Feedback Summary"),
        p("Service Quality Improvement", "Quality", "Customer Experience Proposal"),
    ],
    "Data Entry Operator": [
        p("Keyboard & Data Accuracy", "Data_Entry", "Data Quality Checklist"),
        p("Excel Fundamentals", "Excel", "Structured Data Workbook"),
        p("Document Management", "Documentation", "Digital Filing Exercise"),
        p("Data Validation & Quality", "Quality", "Validation Rules Sheet"),
        p("Basic Reporting", "Reporting", "Simple Reporting Dashboard"),
        p("Workflow Automation Basics", "Productivity", "Automated Data Template"),
    ],
    "HR Specialist": [
        p("HR Fundamentals", "Human_Resources", "HR Process Map"),
        p("Recruitment & Selection", "Recruitment", "Job Description Portfolio"),
        p("Employee Relations", "Employee_Relations", "Employee Case Study"),
        p("HR Analytics Basics", "Data_Analysis", "Attrition Dashboard"),
        p("Learning & Development", "Learning", "Training Plan"),
        p("HR Policies & Professional Ethics", "Compliance", "HR Policy Summary"),
    ],
    "Manager": [
        p("Management Fundamentals", "Management", "Team Operating Plan"),
        p("Goal Setting & KPIs", "Planning", "KPI Scorecard"),
        p("Finance & Resource Basics", "Finance", "Department Budget"),
        p("People & Performance Management", "Leadership", "Performance Plan"),
        p("Decision Making", "Decision_Making", "Management Case Study"),
        p("Strategic Planning", "Strategy", "12-Month Strategy Plan"),
    ],
    "Marketing Executive": [
        p("Marketing Fundamentals", "Marketing", "Campaign Brief"),
        p("Market Research", "Research", "Customer Persona Study"),
        p("Content & Communication", "Content", "Content Calendar"),
        p("Digital Marketing Basics", "Digital_Marketing", "Campaign Simulation"),
        p("Analytics & KPIs", "Data_Analysis", "Marketing Dashboard"),
        p("Campaign Strategy", "Strategy", "Integrated Campaign Proposal"),
    ],
    "Receptionist": [
        p("Front Desk Fundamentals", "Customer_Service", "Reception Workflow"),
        p("Professional Communication", "Communication", "Phone & Email Script Library"),
        p("Scheduling & Records", "Organization", "Appointment Tracker"),
        p("Visitor & Customer Handling", "Customer_Service", "Service Scenario Workbook"),
        p("Office Software Basics", "Productivity", "Office Productivity Pack"),
        p("Service Quality Improvement", "Quality", "Front Desk Improvement Plan"),
    ],
    "Sales Assistant": [
        p("Sales Fundamentals", "Sales", "Sales Process Map"),
        p("Product Knowledge", "Product_Knowledge", "Product Pitch Sheet"),
        p("Customer Communication", "Communication", "Customer Conversation Practice"),
        p("CRM & Sales Tracking", "CRM", "Sales Tracker"),
        p("Objection Handling", "Negotiation", "Objection Response Library"),
        p("Sales Reporting", "Data_Analysis", "Sales Performance Report"),
    ],
    "Sales Executive": [
        p("Sales Fundamentals", "Sales", "Sales Funnel Map"),
        p("Prospecting & Lead Management", "Lead_Generation", "Lead Tracker"),
        p("Negotiation & Communication", "Negotiation", "Negotiation Case Study"),
        p("CRM & Pipeline Management", "CRM", "Sales Pipeline Dashboard"),
        p("Sales Analytics", "Data_Analysis", "Conversion Dashboard"),
        p("Account & Relationship Management", "Customer_Service", "Account Growth Plan"),
    ],

    # ---------------- Media ----------------
    "Content Writer": [
        p("Writing Fundamentals", "Writing", "Writing Sample Portfolio"),
        p("Research & Fact Checking", "Research", "Research-Based Article"),
        p("SEO & Digital Content Basics", "SEO", "SEO Blog Series"),
        p("Editing & Proofreading", "Editing", "Before/After Editing Samples"),
        p("Content Strategy", "Content_Strategy", "Content Calendar"),
        p("Portfolio & Personal Brand", "Communication", "Writer Portfolio"),
    ],
    "Editor": [
        p("Grammar & Style", "Editing", "Style Guide"),
        p("Copyediting", "Editing", "Edited Article Portfolio"),
        p("Fact Checking", "Research", "Fact-Check Report"),
        p("Structural Editing", "Editing", "Long-Form Editing Sample"),
        p("Publishing Workflow", "Publishing", "Editorial Workflow"),
        p("Portfolio & Editorial Judgment", "Communication", "Editorial Portfolio"),
    ],
    "Journalist": [
        p("Journalism Fundamentals", "Journalism", "News Writing Samples"),
        p("Reporting & Interview Preparation", "Reporting", "Interview Plan"),
        p("Research & Verification", "Research", "Fact-Checked Report"),
        p("News Writing & Editing", "Writing", "News Article Portfolio"),
        p("Media Ethics & Source Handling", "Ethics", "Media Ethics Case Study"),
        p("Digital Journalism Portfolio", "Digital_Media", "Multimedia Story Package"),
    ],
    "Writer": [
        p("Writing Fundamentals", "Writing", "Writing Portfolio"),
        p("Research & Idea Development", "Research", "Research Essay"),
        p("Narrative & Structure", "Storytelling", "Short Story Collection"),
        p("Editing & Revision", "Editing", "Revision Portfolio"),
        p("Publishing Basics", "Publishing", "Publishing Plan"),
        p("Personal Brand & Portfolio", "Communication", "Author Portfolio"),
    ],

    # ---------------- Education ----------------
    "Academic Coordinator": [
        p("Academic Administration", "Education_Administration", "Academic Calendar"),
        p("Curriculum Planning", "Curriculum", "Course Plan"),
        p("Student Support & Communication", "Communication", "Student Support Plan"),
        p("Assessment & Reporting", "Assessment", "Assessment Dashboard"),
        p("Faculty Coordination", "Coordination", "Faculty Planning Workflow"),
        p("Education Program Improvement", "Quality", "Program Improvement Proposal"),
    ],
    "Lecturer": [
        p("Subject Mastery", "Subject_Knowledge", "Topic Notes Portfolio"),
        p("Lesson Planning", "Teaching", "Lesson Plan Series"),
        p("Assessment Design", "Assessment", "Assessment Blueprint"),
        p("Classroom Communication", "Communication", "Teaching Demonstration"),
        p("Educational Technology Basics", "EdTech", "Digital Lesson"),
        p("Academic Development & Research", "Research", "Mini Research Review"),
    ],
    "Principal": [
        p("Educational Leadership", "Leadership", "School Improvement Plan"),
        p("Academic Administration", "Education_Administration", "Annual Academic Plan"),
        p("Staff & Team Management", "People_Management", "Staff Development Plan"),
        p("Student Wellbeing & Support", "Student_Support", "Student Support Framework"),
        p("Policy & Quality Management", "Quality", "Quality Improvement Plan"),
        p("Strategic School Planning", "Strategy", "School Strategy Document"),
    ],
    "Professor": [
        p("Advanced Subject Expertise", "Subject_Knowledge", "Advanced Topic Seminar"),
        p("Teaching & Course Design", "Teaching", "University Course Plan"),
        p("Research Methods", "Research", "Research Proposal"),
        p("Academic Writing & Publication", "Academic_Writing", "Literature Review"),
        p("Mentoring & Student Guidance", "Mentoring", "Mentoring Framework"),
        p("Research Portfolio Development", "Research", "Research Portfolio"),
    ],
    "Research Assistant": [
        p("Research Fundamentals", "Research", "Research Question Map"),
        p("Literature Review", "Academic_Writing", "Literature Review"),
        p("Data Collection & Organization", "Data_Collection", "Research Dataset Log"),
        p("Basic Data Analysis", "Data_Analysis", "Analysis Report"),
        p("Academic Writing", "Academic_Writing", "Research Manuscript Draft"),
        p("Research Presentation", "Communication", "Research Poster / Presentation"),
    ],
    "Research Scientist": [
        p("Advanced Research Methods", "Research", "Research Protocol"),
        p("Literature Synthesis", "Academic_Writing", "Systematic Literature Review"),
        p("Experimental / Analytical Design", "Methodology", "Study Design"),
        p("Data Analysis & Interpretation", "Data_Analysis", "Research Analysis Report"),
        p("Scientific Writing & Publication", "Scientific_Writing", "Paper Draft"),
        p("Research Communication", "Communication", "Conference-Style Presentation"),
    ],
    "School Coordinator": [
        p("School Operations", "Education_Administration", "School Operations Calendar"),
        p("Timetable & Resource Planning", "Planning", "Timetable Plan"),
        p("Teacher Coordination", "Coordination", "Teacher Coordination Workflow"),
        p("Student Support", "Student_Support", "Student Support Plan"),
        p("Assessment & Reporting", "Assessment", "Academic Report"),
        p("Quality Improvement", "Quality", "School Improvement Proposal"),
    ],
    "Teacher": [
        p("Subject Knowledge", "Subject_Knowledge", "Teaching Notes Portfolio"),
        p("Lesson Planning", "Teaching", "Lesson Plan Series"),
        p("Classroom Management", "Classroom_Management", "Classroom Management Plan"),
        p("Assessment & Feedback", "Assessment", "Assessment Toolkit"),
        p("Educational Technology", "EdTech", "Digital Lesson Project"),
        p("Professional Teaching Portfolio", "Communication", "Teaching Portfolio"),
    ],
    "Tutor": [
        p("Subject Fundamentals", "Subject_Knowledge", "Topic Revision Pack"),
        p("Explaining Concepts Clearly", "Teaching", "Concept Explanation Samples"),
        p("Lesson Planning", "Planning", "Weekly Lesson Plan"),
        p("Practice & Assessment", "Assessment", "Practice Question Set"),
        p("Student Feedback", "Communication", "Feedback Framework"),
        p("Online Tutoring Tools", "EdTech", "Digital Tutoring Session"),
    ],

    # ---------------- Design ----------------
    "Animator": [
        p("Drawing & Visual Fundamentals", "Drawing", "Character Sketches"),
        p("Design Principles", "Design_Principles", "Visual Style Board"),
        p("Storyboarding", "Storytelling", "Short Storyboard"),
        p("2D / 3D Animation Basics", "Animation", "Short Animation"),
        p("Motion & Timing", "Animation", "Motion Study"),
        p("Animation Portfolio", "Portfolio", "Demo Reel"),
    ],
    "Fashion Designer": [
        p("Fashion Drawing & Design", "Fashion_Design", "Design Sketchbook"),
        p("Textiles & Materials", "Textiles", "Material Study"),
        p("Color & Trend Research", "Research", "Trend Board"),
        p("Pattern & Garment Development", "Pattern_Making", "Garment Concept"),
        p("Collection Development", "Collection_Design", "Mini Collection"),
        p("Portfolio & Presentation", "Portfolio", "Fashion Portfolio"),
    ],
    "Graphic Designer": [
        p("Design Principles", "Design_Principles", "Visual Design Study"),
        p("Typography & Layout", "Typography", "Poster Series"),
        p("Color & Branding", "Branding", "Brand Identity Kit"),
        p("Figma / Design Tools", "Design_Tools", "Digital Design Set"),
        p("Visual Communication", "Communication", "Campaign Graphics"),
        p("Portfolio & Client Presentation", "Portfolio", "Design Portfolio"),
    ],

    # ---------------- Engineering ----------------
    "AutoCAD Designer": [
        p("Engineering Drawing Fundamentals", "Engineering_Drawing", "Drawing Sheet Portfolio"),
        p("AutoCAD 2D", "AutoCAD", "2D Drawing Set"),
        p("Dimensioning & Standards", "Engineering_Standards", "Technical Drawing Pack"),
        p("3D Modeling Basics", "CAD", "3D Part Model"),
        p("Design Documentation", "Documentation", "Design Documentation Set"),
        p("CAD Portfolio & Review", "Portfolio", "CAD Portfolio"),
    ],
    "Civil Engineer": [
        p("Engineering Mathematics & Mechanics", "Engineering_Fundamentals", "Mechanics Problem Set"),
        p("Structural & Construction Fundamentals", "Construction", "Structural Concept Study"),
        p("Surveying & Site Basics", "Surveying", "Site Survey Report"),
        p("Civil Design Tools", "CAD", "Civil CAD Project"),
        p("Project Planning & Estimation", "Project_Management", "Construction Estimate"),
        p("Capstone Design Portfolio", "Engineering_Design", "Civil Design Portfolio"),
    ],
    "Design Engineer": [
        p("Engineering Fundamentals", "Engineering_Fundamentals", "Engineering Problem Set"),
        p("Engineering Drawing & CAD", "CAD", "CAD Design Set"),
        p("Design Methods & Tolerances", "Engineering_Design", "Component Design"),
        p("Materials & Manufacturing Basics", "Manufacturing", "Material Selection Study"),
        p("Testing & Design Validation", "Quality", "Design Validation Report"),
        p("Engineering Design Portfolio", "Portfolio", "Design Portfolio"),
    ],
    "Electrical Engineer": [
        p("Circuit Fundamentals", "Circuits", "Circuit Analysis Workbook"),
        p("Electrical Machines & Systems", "Electrical_Systems", "System Study"),
        p("Electronics & Measurement", "Electronics", "Measurement Project"),
        p("Control & Instrumentation Basics", "Control_Systems", "Control System Model"),
        p("Power Systems / Embedded Elective", "Engineering", "Applied Electrical Project"),
        p("Engineering Design Portfolio", "Portfolio", "Electrical Engineering Portfolio"),
    ],
    "Energy Analyst": [
        p("Energy Systems Fundamentals", "Energy", "Energy Systems Summary"),
        p("Excel & Data Analysis", "Excel", "Energy Data Workbook"),
        p("Energy Efficiency Concepts", "Energy_Efficiency", "Efficiency Assessment"),
        p("Renewable Energy Basics", "Renewables", "Renewable Energy Case Study"),
        p("Energy Economics & Policy", "Policy", "Energy Policy Review"),
        p("Energy Analysis Capstone", "Analysis", "Energy Assessment Report"),
    ],
    "Junior Engineer": [
        p("Engineering Fundamentals", "Engineering_Fundamentals", "Engineering Problem Set"),
        p("Technical Drawing & Documentation", "Engineering_Drawing", "Drawing Portfolio"),
        p("Tools & Measurement", "Technical_Skills", "Measurement Exercise"),
        p("Quality & Safety Fundamentals", "Quality", "Quality Checklist"),
        p("Project & Team Collaboration", "Communication", "Project Work Plan"),
        p("Engineering Mini Project", "Engineering_Design", "Mini Engineering Project"),
    ],
    "Lab Technician": [
        p("Laboratory Fundamentals", "Laboratory", "Lab Notebook Template"),
        p("Measurement & Instrumentation", "Instrumentation", "Measurement Log"),
        p("Sample Handling & Documentation", "Documentation", "Sample Tracking Sheet"),
        p("Quality Control Basics", "Quality", "QC Checklist"),
        p("Data Recording & Reporting", "Data_Analysis", "Lab Report"),
        p("Lab Safety & Professional Practice", "Safety", "Lab Safety Portfolio"),
    ],
    "Mechanical Engineer": [
        p("Engineering Mechanics", "Mechanics", "Mechanics Problem Set"),
        p("Thermodynamics & Materials", "Thermodynamics", "Thermal System Study"),
        p("CAD & Engineering Drawing", "CAD", "Mechanical CAD Assembly"),
        p("Manufacturing Processes", "Manufacturing", "Process Selection Study"),
        p("Design & Validation", "Engineering_Design", "Component Design Project"),
        p("Engineering Portfolio", "Portfolio", "Mechanical Design Portfolio"),
    ],
    "Technician": [
        p("Technical Fundamentals", "Technical_Skills", "Technical Skills Workbook"),
        p("Tools & Measurement", "Instrumentation", "Measurement Exercise"),
        p("Equipment Operation Basics", "Equipment", "Equipment Checklist"),
        p("Maintenance & Troubleshooting", "Troubleshooting", "Maintenance Log"),
        p("Quality & Safety", "Safety", "Safety & Quality Checklist"),
        p("Practical Skills Portfolio", "Portfolio", "Technician Skills Portfolio"),
    ],

    # ---------------- Healthcare ----------------
    # These are educational/professional-development pathways, not clinical instructions.
    "Doctor": [
        p("Human Anatomy & Physiology", "Anatomy", "Medical Learning Notes"),
        p("Pathophysiology Fundamentals", "Physiology", "Case-Based Study Notes"),
        p("Clinical Reasoning Foundations", "Diagnosis", "Clinical Reasoning Casebook"),
        p("Evidence-Based Medicine", "Research", "Evidence Review Project"),
        p("Patient Communication & Ethics", "Patient_Care", "Communication & Ethics Portfolio"),
        p("Residency / Specialty Planning", "Specialization", "Medical Career Roadmap"),
    ],
    "General Practitioner": [
        p("Human Anatomy & Physiology", "Anatomy", "Medical Learning Notes"),
        p("Clinical Reasoning Foundations", "Diagnosis", "Case Reasoning Portfolio"),
        p("Common Conditions & Preventive Care", "Public_Health", "Preventive Care Case Study"),
        p("Patient Communication", "Patient_Care", "Patient Communication Portfolio"),
        p("Evidence-Based Primary Care", "Research", "Primary Care Evidence Review"),
        p("Continuing Education Planning", "Professional_Development", "CPD Learning Plan"),
    ],
    "Surgeon": [
        p("Human Anatomy & Physiology", "Anatomy", "Anatomy Learning Portfolio"),
        p("Pathology & Clinical Foundations", "Pathology", "Pathology Case Review"),
        p("Clinical Assessment & Imaging Concepts", "Diagnosis", "Clinical Case Study"),
        p("Surgical Principles & Perioperative Care", "Surgery", "Surgical Learning Portfolio"),
        p("Evidence-Based Surgical Practice", "Research", "Surgical Evidence Review"),
        p("Residency & Specialty Development", "Specialization", "Specialty Career Plan"),
    ],
}


def seed():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION]
    collection.delete_many({})

    domain_map = {
        "AI Engineer": "Technology", "Data Analyst": "Technology", "Data Scientist": "Technology",
        "Software Architect": "Technology", "Software Developer": "Technology", "Software Engineer": "Technology",
        "System Analyst": "Technology", "Web Developer": "Technology",
        "Accountant": "Finance", "Auditor": "Finance", "Clerk": "Finance", "Finance Manager": "Finance",
        "Financial Analyst": "Finance", "Junior Assistant": "Finance", "Senior Accountant": "Finance",
        "Analyst": "Business", "Assistant Manager": "Business", "Business Analyst": "Business",
        "Consultant": "Business", "Customer Support Executive": "Business", "Data Entry Operator": "Business",
        "HR Specialist": "Business", "Manager": "Business", "Marketing Executive": "Business",
        "Receptionist": "Business", "Sales Assistant": "Business", "Sales Executive": "Business",
        "Content Writer": "Media", "Editor": "Media", "Journalist": "Media", "Writer": "Media",
        "Academic Coordinator": "Education", "Lecturer": "Education", "Principal": "Education",
        "Professor": "Education", "Research Assistant": "Education", "Research Scientist": "Education",
        "School Coordinator": "Education", "Teacher": "Education", "Tutor": "Education",
        "Animator": "Design", "Fashion Designer": "Design", "Graphic Designer": "Design",
        "AutoCAD Designer": "Engineering", "Civil Engineer": "Engineering", "Design Engineer": "Engineering",
        "Electrical Engineer": "Engineering", "Energy Analyst": "Engineering", "Junior Engineer": "Engineering",
        "Lab Technician": "Engineering", "Mechanical Engineer": "Engineering", "Technician": "Engineering",
        "Doctor": "Healthcare", "General Practitioner": "Healthcare", "Surgeon": "Healthcare",
    }

    docs = []
    for career, steps in ROADMAPS.items():
        docs.append({
            "career": career,
            "domain": domain_map.get(career, "Other"),
            "steps": [
                {"step": i, "title": title, "skill": skill, "project": project}
                for i, (title, skill, project) in enumerate(steps, start=1)
            ],
        })

    collection.insert_many(docs)
    collection.create_index("career", unique=True)
    print(f"Seeded {len(docs)} domain-specific career roadmaps into {DB_NAME}.{COLLECTION}")
    client.close()


if __name__ == "__main__":
    seed()
