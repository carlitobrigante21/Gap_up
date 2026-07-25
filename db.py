"""
GapUp database setup and seed data.
Creates a SQLite database (gapup.db) with 8 normalized tables (3NF) and
pre-populates them with 30 IT roles, 100 skills, 20 certifications, and
the bridge-table links between roles/skills/certs.

Run once:  python3 db.py
"""

import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gapup.db")

# ---------------------------------------------------------------------------
# Schema (DDL)
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS roles (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS skills (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    parent_skill_id INTEGER REFERENCES skills(id),
    estimated_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS cert (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    issuer          TEXT NOT NULL,
    estimated_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS prof (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS role_skills (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id  INTEGER NOT NULL REFERENCES roles(id),
    skill_id INTEGER NOT NULL REFERENCES skills(id),
    UNIQUE(role_id, skill_id)
);

CREATE TABLE IF NOT EXISTS role_certs (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    cert_id INTEGER NOT NULL REFERENCES cert(id),
    UNIQUE(role_id, cert_id)
);

CREATE TABLE IF NOT EXISTS prof_skills (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id  INTEGER NOT NULL REFERENCES prof(id),
    skill_id INTEGER NOT NULL REFERENCES skills(id),
    UNIQUE(prof_id, skill_id)
);

CREATE TABLE IF NOT EXISTS prof_certs (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    prof_id INTEGER NOT NULL REFERENCES prof(id),
    cert_id INTEGER NOT NULL REFERENCES cert(id),
    UNIQUE(prof_id, cert_id)
);
"""

# ---------------------------------------------------------------------------
# Seed data: 30 IT roles
# ---------------------------------------------------------------------------
ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Fullstack Developer",
    "DevOps Engineer",
    "Cloud Architect",
    "Data Scientist",
    "Data Engineer",
    "Data Analyst",
    "Cybersecurity Analyst",
    "Penetration Tester",
    "Network Engineer",
    "Systems Administrator",
    "Database Administrator",
    "Site Reliability Engineer (SRE)",
    "AI/ML Engineer",
    "QA Automation Engineer",
    "Security Engineer",
    "Solutions Architect",
    "Mobile App Developer (iOS)",
    "Mobile App Developer (Android)",
    "Embedded Systems Engineer",
    "Blockchain Developer",
    "UI/UX Engineer",
    "Scrum Master",
    "IT Project Manager",
    "Business Analyst",
    "DevSecOps Engineer",
    "Big Data Developer",
    "Game Developer",
    "ERP Consultant",
]

# ---------------------------------------------------------------------------
# Seed data: 100 hard skills (6 category parents + 94 children).
# Each entry: (name, parent_skill_name_or_None, estimated_hours)
# Parents are created first; children resolve parent_skill_id by name.
# ---------------------------------------------------------------------------
SKILLS = [
    # --- Category parents ---
    ("Programming", None, 30),
    ("Web", None, 30),
    ("Cloud/DevOps", None, 30),
    ("Data/AI", None, 30),
    ("Networking/Security", None, 30),
    ("Engineering Tools", None, 25),

    # --- Programming (14) ---
    ("Python", "Programming", 35),
    ("Java", "Programming", 45),
    ("JavaScript", "Programming", 30),
    ("TypeScript", "Programming", 25),
    ("C", "Programming", 50),
    ("C++", "Programming", 55),
    ("C#", "Programming", 45),
    ("Go", "Programming", 35),
    ("Kotlin", "Programming", 35),
    ("Swift", "Programming", 40),
    ("SQL", "Programming", 25),
    ("Shell Scripting (Bash)", "Programming", 20),
    ("PowerShell", "Programming", 20),
    ("Solidity", "Programming", 45),

    # --- Web (13) ---
    ("HTML5", "Web", 15),
    ("CSS3", "Web", 20),
    ("React", "Web", 40),
    ("Node.js", "Web", 35),
    ("Express.js", "Web", 25),
    ("Django", "Web", 40),
    ("Spring Boot", "Web", 45),
    ("REST APIs", "Web", 25),
    ("GraphQL", "Web", 30),
    ("Tailwind CSS", "Web", 15),
    ("Web Accessibility (a11y)", "Web", 25),
    ("Web Performance Optimization", "Web", 30),
    ("Figma", "Web", 25),

    # --- Cloud/DevOps (17) ---
    ("AWS EC2", "Cloud/DevOps", 30),
    ("AWS S3", "Cloud/DevOps", 20),
    ("AWS RDS", "Cloud/DevOps", 25),
    ("AWS Lambda", "Cloud/DevOps", 30),
    ("AWS IAM", "Cloud/DevOps", 25),
    ("Azure Virtual Machines", "Cloud/DevOps", 30),
    ("Google Compute Engine", "Cloud/DevOps", 30),
    ("Docker", "Cloud/DevOps", 35),
    ("Kubernetes", "Cloud/DevOps", 60),
    ("Terraform", "Cloud/DevOps", 40),
    ("Ansible", "Cloud/DevOps", 35),
    ("Jenkins", "Cloud/DevOps", 30),
    ("GitHub Actions", "Cloud/DevOps", 25),
    ("GitLab CI/CD", "Cloud/DevOps", 25),
    ("Prometheus", "Cloud/DevOps", 30),
    ("Grafana", "Cloud/DevOps", 25),
    ("Serverless Architecture", "Cloud/DevOps", 35),

    # --- Data/AI (17) ---
    ("Pandas", "Data/AI", 25),
    ("NumPy", "Data/AI", 20),
    ("Scikit-learn", "Data/AI", 35),
    ("TensorFlow", "Data/AI", 50),
    ("PyTorch", "Data/AI", 50),
    ("Natural Language Processing", "Data/AI", 45),
    ("Computer Vision", "Data/AI", 45),
    ("Deep Learning", "Data/AI", 55),
    ("Machine Learning", "Data/AI", 45),
    ("Statistical Analysis", "Data/AI", 35),
    ("Data Visualization", "Data/AI", 25),
    ("Tableau", "Data/AI", 30),
    ("Power BI", "Data/AI", 30),
    ("Apache Spark", "Data/AI", 45),
    ("Apache Kafka", "Data/AI", 40),
    ("Airflow", "Data/AI", 35),
    ("ETL Pipelines", "Data/AI", 35),

    # --- Networking/Security (18) ---
    ("TCP/IP", "Networking/Security", 25),
    ("DNS", "Networking/Security", 20),
    ("Firewalls", "Networking/Security", 25),
    ("Load Balancing", "Networking/Security", 25),
    ("Wireshark", "Networking/Security", 25),
    ("Cryptography", "Networking/Security", 40),
    ("SIEM", "Networking/Security", 35),
    ("Incident Response", "Networking/Security", 30),
    ("Threat Modeling", "Networking/Security", 30),
    ("Vulnerability Assessment", "Networking/Security", 35),
    ("Metasploit", "Networking/Security", 35),
    ("Burp Suite", "Networking/Security", 30),
    ("OWASP Top 10", "Networking/Security", 25),
    ("Network Security", "Networking/Security", 30),
    ("Cloud Security", "Networking/Security", 35),
    ("Identity & Access Management", "Networking/Security", 30),
    ("Zero Trust Architecture", "Networking/Security", 30),
    ("Penetration Testing", "Networking/Security", 40),

    # --- Engineering Tools (15) ---
    ("Git", "Engineering Tools", 20),
    ("Jira", "Engineering Tools", 15),
    ("Confluence", "Engineering Tools", 10),
    ("Agile/Scrum", "Engineering Tools", 20),
    ("Unit Testing", "Engineering Tools", 25),
    ("Integration Testing", "Engineering Tools", 25),
    ("Selenium", "Engineering Tools", 30),
    ("Cypress", "Engineering Tools", 25),
    ("Postman", "Engineering Tools", 15),
    ("Linux Administration", "Engineering Tools", 40),
    ("Windows Server Administration", "Engineering Tools", 35),
    ("System Design", "Engineering Tools", 40),
    ("Microservices", "Engineering Tools", 35),
    ("API Design", "Engineering Tools", 25),
    ("CI/CD", "Engineering Tools", 30),
]

# ---------------------------------------------------------------------------
# Seed data: 20 certifications
# ---------------------------------------------------------------------------
CERTS = [
    ("AWS Certified Solutions Architect – Associate", "Amazon Web Services", 60),
    ("AWS Certified Developer – Associate", "Amazon Web Services", 50),
    ("AWS Certified DevOps Engineer – Professional", "Amazon Web Services", 80),
    ("Microsoft Certified: Azure Solutions Architect Expert", "Microsoft", 80),
    ("Microsoft Certified: Azure Administrator Associate", "Microsoft", 50),
    ("Google Cloud Professional Cloud Architect", "Google Cloud", 70),
    ("Certified Kubernetes Administrator (CKA)", "Cloud Native Computing Foundation", 60),
    ("Certified Kubernetes Application Developer (CKAD)", "Cloud Native Computing Foundation", 55),
    ("Cisco Certified Network Associate (CCNA)", "Cisco", 80),
    ("Cisco Certified Network Professional (CCNP)", "Cisco", 120),
    ("CompTIA Security+", "CompTIA", 45),
    ("CompTIA Network+", "CompTIA", 40),
    ("Certified Ethical Hacker (CEH)", "EC-Council", 70),
    ("OSCP (Offensive Security Certified Professional)", "Offensive Security", 150),
    ("CISSP (Certified Information Systems Security Professional)", "ISC2", 120),
    ("CCSP (Certified Cloud Security Professional)", "ISC2", 90),
    ("Project Management Professional (PMP)", "Project Management Institute", 100),
    ("Certified ScrumMaster (CSM)", "Scrum Alliance", 25),
    ("ITIL 4 Foundation", "PeopleCert", 30),
    ("Google Cloud Professional Data Engineer", "Google Cloud", 70),
]

# ---------------------------------------------------------------------------
# Role -> required skills mapping (by skill name).
# Each role is logically linked to a realistic set of required skills.
# ---------------------------------------------------------------------------
ROLE_SKILL_MAP = {
    "Frontend Developer": [
        "HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Tailwind CSS",
        "Web Accessibility (a11y)", "Web Performance Optimization", "Git",
        "REST APIs", "Figma", "Unit Testing",
    ],
    "Backend Developer": [
        "Python", "Java", "SQL", "REST APIs", "GraphQL", "Node.js",
        "Express.js", "Django", "Spring Boot", "Postman", "API Design",
        "Microservices", "Git", "Unit Testing",
    ],
    "Fullstack Developer": [
        "HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Node.js",
        "Express.js", "SQL", "REST APIs", "Git", "Django", "Tailwind CSS",
        "Web Performance Optimization", "API Design",
    ],
    "DevOps Engineer": [
        "Linux Administration", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "GitLab CI/CD", "GitHub Actions", "AWS EC2",
        "AWS S3", "Prometheus", "Grafana", "Shell Scripting (Bash)", "Git",
        "CI/CD",
    ],
    "Cloud Architect": [
        "AWS EC2", "AWS S3", "AWS RDS", "AWS IAM", "AWS Lambda",
        "Azure Virtual Machines", "Google Compute Engine", "Terraform",
        "Serverless Architecture", "System Design", "Load Balancing", "DNS",
        "Microservices",
    ],
    "Data Scientist": [
        "Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning",
        "Statistical Analysis", "Data Visualization", "SQL", "Deep Learning",
        "Git",
    ],
    "Data Engineer": [
        "Python", "SQL", "Apache Spark", "Apache Kafka", "Airflow",
        "ETL Pipelines", "AWS S3", "Docker", "Linux Administration", "Git",
        "CI/CD",
    ],
    "Data Analyst": [
        "SQL", "Python", "Pandas", "Tableau", "Power BI",
        "Data Visualization", "Statistical Analysis", "Git",
    ],
    "Cybersecurity Analyst": [
        "SIEM", "Incident Response", "Threat Modeling", "OWASP Top 10",
        "Cloud Security", "Wireshark", "Firewalls", "TCP/IP",
        "Vulnerability Assessment", "Network Security",
    ],
    "Penetration Tester": [
        "Penetration Testing", "Metasploit", "Burp Suite", "OWASP Top 10",
        "Vulnerability Assessment", "Linux Administration", "Python",
        "Network Security", "Wireshark",
    ],
    "Network Engineer": [
        "TCP/IP", "DNS", "Firewalls", "Load Balancing", "Wireshark",
        "Network Security",
    ],
    "Systems Administrator": [
        "Linux Administration", "Windows Server Administration",
        "Shell Scripting (Bash)", "PowerShell", "Docker", "AWS EC2", "DNS",
        "Firewalls", "Git",
    ],
    "Database Administrator": [
        "SQL", "Linux Administration", "AWS RDS", "Docker", "Git", "CI/CD",
        "System Design",
    ],
    "Site Reliability Engineer (SRE)": [
        "Linux Administration", "Docker", "Kubernetes", "Prometheus",
        "Grafana", "Go", "Python", "Terraform", "AWS EC2",
        "Shell Scripting (Bash)",
    ],
    "AI/ML Engineer": [
        "Python", "TensorFlow", "PyTorch", "Deep Learning",
        "Natural Language Processing", "Computer Vision", "Machine Learning",
        "Scikit-learn", "Pandas", "NumPy", "Git", "Docker",
    ],
    "QA Automation Engineer": [
        "Selenium", "Cypress", "Python", "Java", "Unit Testing",
        "Integration Testing", "Postman", "REST APIs", "Git", "Jira",
    ],
    "Security Engineer": [
        "Cryptography", "Identity & Access Management",
        "Zero Trust Architecture", "Cloud Security", "OWASP Top 10",
        "Threat Modeling", "Python", "Linux Administration", "Firewalls",
    ],
    "Solutions Architect": [
        "System Design", "Microservices", "AWS EC2", "AWS S3", "AWS Lambda",
        "Azure Virtual Machines", "Google Compute Engine", "API Design",
        "Terraform", "Serverless Architecture", "REST APIs",
    ],
    "Mobile App Developer (iOS)": [
        "Swift", "REST APIs", "Git", "Unit Testing", "Figma",
        "Web Performance Optimization",
    ],
    "Mobile App Developer (Android)": [
        "Kotlin", "Java", "REST APIs", "Git", "Unit Testing", "Figma",
    ],
    "Embedded Systems Engineer": [
        "C", "C++", "Python", "Git", "Linux Administration",
        "Shell Scripting (Bash)",
    ],
    "Blockchain Developer": [
        "Solidity", "Python", "JavaScript", "Cryptography", "Go", "Git",
        "REST APIs",
    ],
    "UI/UX Engineer": [
        "HTML5", "CSS3", "JavaScript", "Figma", "Web Accessibility (a11y)",
        "Tailwind CSS", "Git",
    ],
    "Scrum Master": [
        "Agile/Scrum", "Jira", "Confluence", "Git",
    ],
    "IT Project Manager": [
        "Agile/Scrum", "Jira", "Confluence", "Git", "System Design",
    ],
    "Business Analyst": [
        "SQL", "Power BI", "Tableau", "Data Visualization", "Jira",
        "Confluence", "Git",
    ],
    "DevSecOps Engineer": [
        "Docker", "Kubernetes", "Terraform", "GitHub Actions", "GitLab CI/CD",
        "Cloud Security", "OWASP Top 10", "Identity & Access Management",
        "Linux Administration", "Shell Scripting (Bash)", "Python", "CI/CD",
    ],
    "Big Data Developer": [
        "Apache Spark", "Apache Kafka", "Python", "SQL", "Airflow",
        "ETL Pipelines", "Git", "CI/CD",
    ],
    "Game Developer": [
        "C++", "C#", "Git", "System Design", "Python",
    ],
    "ERP Consultant": [
        "SQL", "Jira", "Confluence", "Git", "API Design",
    ],
}

# ---------------------------------------------------------------------------
# Role -> recommended certifications mapping (by cert name).
# ---------------------------------------------------------------------------
ROLE_CERT_MAP = {
    "Frontend Developer": [
        "AWS Certified Developer – Associate",
    ],
    "Backend Developer": [
        "AWS Certified Developer – Associate",
    ],
    "Fullstack Developer": [
        "AWS Certified Developer – Associate",
        "Certified Kubernetes Application Developer (CKAD)",
    ],
    "DevOps Engineer": [
        "AWS Certified DevOps Engineer – Professional",
        "Certified Kubernetes Administrator (CKA)",
    ],
    "Cloud Architect": [
        "AWS Certified Solutions Architect – Associate",
        "Microsoft Certified: Azure Solutions Architect Expert",
        "Google Cloud Professional Cloud Architect",
    ],
    "Data Scientist": [
        "Google Cloud Professional Data Engineer",
    ],
    "Data Engineer": [
        "Google Cloud Professional Data Engineer",
        "AWS Certified Developer – Associate",
    ],
    "Data Analyst": [
        "Google Cloud Professional Data Engineer",
    ],
    "Cybersecurity Analyst": [
        "CompTIA Security+",
        "CompTIA Network+",
    ],
    "Penetration Tester": [
        "Certified Ethical Hacker (CEH)",
        "OSCP (Offensive Security Certified Professional)",
    ],
    "Network Engineer": [
        "Cisco Certified Network Associate (CCNA)",
        "Cisco Certified Network Professional (CCNP)",
        "CompTIA Network+",
    ],
    "Systems Administrator": [
        "Microsoft Certified: Azure Administrator Associate",
        "CompTIA Network+",
    ],
    "Database Administrator": [
        "AWS Certified Solutions Architect – Associate",
    ],
    "Site Reliability Engineer (SRE)": [
        "Certified Kubernetes Administrator (CKA)",
        "AWS Certified DevOps Engineer – Professional",
    ],
    "AI/ML Engineer": [
        "Google Cloud Professional Data Engineer",
    ],
    "QA Automation Engineer": [
        "Certified Kubernetes Application Developer (CKAD)",
    ],
    "Security Engineer": [
        "CompTIA Security+",
        "CISSP (Certified Information Systems Security Professional)",
        "CCSP (Certified Cloud Security Professional)",
    ],
    "Solutions Architect": [
        "AWS Certified Solutions Architect – Associate",
        "Microsoft Certified: Azure Solutions Architect Expert",
        "Google Cloud Professional Cloud Architect",
    ],
    "Mobile App Developer (iOS)": [
        "AWS Certified Developer – Associate",
    ],
    "Mobile App Developer (Android)": [
        "AWS Certified Developer – Associate",
    ],
    "Embedded Systems Engineer": [
        "CompTIA Network+",
    ],
    "Blockchain Developer": [
        "CompTIA Security+",
    ],
    "UI/UX Engineer": [],
    "Scrum Master": [
        "Certified ScrumMaster (CSM)",
    ],
    "IT Project Manager": [
        "Project Management Professional (PMP)",
        "Certified ScrumMaster (CSM)",
        "ITIL 4 Foundation",
    ],
    "Business Analyst": [
        "ITIL 4 Foundation",
    ],
    "DevSecOps Engineer": [
        "CompTIA Security+",
        "Certified Kubernetes Administrator (CKA)",
        "CCSP (Certified Cloud Security Professional)",
    ],
    "Big Data Developer": [
        "Google Cloud Professional Data Engineer",
    ],
    "Game Developer": [],
    "ERP Consultant": [
        "ITIL 4 Foundation",
        "Project Management Professional (PMP)",
    ],
}

# ---------------------------------------------------------------------------
# A few sample professionals (for the prof / prof_skills / prof_certs tables).
# Required by the schema; not used by the main workflow.
# ---------------------------------------------------------------------------
PROFS = [
    ("Alex Morgan", "alex.morgan@example.com"),
    ("Priya Patel", "priya.patel@example.com"),
    ("Diego Ramirez", "diego.ramirez@example.com"),
    ("Mei Chen", "mei.chen@example.com"),
    ("Samuel Okafor", "samuel.okafor@example.com"),
]


def build_database(force: bool = False) -> str:
    """Create and seed the SQLite database. Returns the DB path."""
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executescript(SCHEMA)

    # Wipe (idempotent re-runs)
    for t in [
        "prof_certs", "prof_skills", "role_certs", "role_skills",
        "prof", "cert", "skills", "roles",
    ]:
        cur.execute(f"DELETE FROM {t};")

    # Roles
    for name in ROLES:
        cur.execute("INSERT INTO roles (name) VALUES (?);", (name,))

    # Skills (parents first, then children)
    skill_id_by_name: dict[str, int] = {}
    for name, parent, hours in SKILLS:
        if parent is None:
            cur.execute(
                "INSERT INTO skills (name, parent_skill_id, estimated_hours) VALUES (?, NULL, ?);",
                (name, hours),
            )
            skill_id_by_name[name] = cur.lastrowid
    for name, parent, hours in SKILLS:
        if parent is not None:
            pid = skill_id_by_name.get(parent)
            cur.execute(
                "INSERT INTO skills (name, parent_skill_id, estimated_hours) VALUES (?, ?, ?);",
                (name, pid, hours),
            )
            skill_id_by_name[name] = cur.lastrowid

    # Certs
    cert_id_by_name: dict[str, int] = {}
    for name, issuer, hours in CERTS:
        cur.execute("INSERT INTO cert (name, issuer, estimated_hours) VALUES (?, ?, ?);", (name, issuer, hours))
        cert_id_by_name[name] = cur.lastrowid

    # role_skills
    role_id_by_name = {n: i for i, n in enumerate(ROLES, start=1)}
    for role_name, skill_names in ROLE_SKILL_MAP.items():
        rid = role_id_by_name[role_name]
        for sn in skill_names:
            sid = skill_id_by_name.get(sn)
            if sid is None:
                raise ValueError(f"Skill '{sn}' referenced by role '{role_name}' is not defined.")
            cur.execute(
                "INSERT OR IGNORE INTO role_skills (role_id, skill_id) VALUES (?, ?);",
                (rid, sid),
            )

    # role_certs
    for role_name, cert_names in ROLE_CERT_MAP.items():
        rid = role_id_by_name[role_name]
        for cn in cert_names:
            cid = cert_id_by_name.get(cn)
            if cid is None:
                raise ValueError(f"Cert '{cn}' referenced by role '{role_name}' is not defined.")
            cur.execute(
                "INSERT OR IGNORE INTO role_certs (role_id, cert_id) VALUES (?, ?);",
                (rid, cid),
            )

    # prof + prof_skills + prof_certs (sample data)
    for pname, pemail in PROFS:
        cur.execute("INSERT INTO prof (name, email) VALUES (?, ?);", (pname, pemail))
        pid = cur.lastrowid
        if pname == "Alex Morgan":
            for sn in ["JavaScript", "React", "HTML5", "CSS3", "Node.js"]:
                cur.execute(
                    "INSERT OR IGNORE INTO prof_skills (prof_id, skill_id) VALUES (?, ?);",
                    (pid, skill_id_by_name[sn]),
                )
        elif pname == "Priya Patel":
            for sn in ["Python", "SQL", "Pandas", "Machine Learning", "Scikit-learn"]:
                cur.execute(
                    "INSERT OR IGNORE INTO prof_skills (prof_id, skill_id) VALUES (?, ?);",
                    (pid, skill_id_by_name[sn]),
                )

    conn.commit()
    conn.close()
    return DB_PATH


def get_connection():
    """Return a sqlite3 connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    path = build_database(force=True)
    conn = get_connection()
    cur = conn.cursor()
    counts = {}
    for t in ["roles", "skills", "cert", "prof", "role_skills", "role_certs", "prof_skills", "prof_certs"]:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        counts[t] = cur.fetchone()[0]
    conn.close()
    print(f"Database ready at: {path}")
    print("Row counts:")
    print(json.dumps(counts, indent=2))
