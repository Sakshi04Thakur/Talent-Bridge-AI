import streamlit as st
import re
import hashlib
import json 
import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from io import BytesIO
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TalentBridge AI",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* ==========================================
   MAIN BACKGROUND
========================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #F0F7FF,
        #FFF5FA,
        #F0FFF7
    );
}

/* ==========================================
   SIDEBAR
========================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        to bottom,
        #172554,
        #3730A3,
        #4C1D95
    );
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* ==========================================
   MAIN TITLE BOX
========================================== */

.main-title {
    display: inline-block;
    background: linear-gradient(
        90deg,
        #172554,
        #3730A3,
        #581C87
    );

    color: #FFFFFF !important;
    font-size: 40px;
    font-weight: 800;

    padding: 15px 28px;
    border-radius: 15px;

    border-left: 6px solid #FACC15;

    box-shadow: 0px 6px 20px rgba(55, 48, 163, 0.25);

    margin-bottom: 12px;
}

/* ==========================================
   SUBTITLE
========================================== */

.subtitle {
    font-size: 17px;
    color: #475569;
    font-weight: 500;
    margin-top: 8px;
}

/* ==========================================
   FEATURE CARDS
========================================== */

.card {
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #F0F7FF
    );

    padding: 24px;
    border-radius: 18px;

    border: 1px solid #BFDBFE;
    border-top: 5px solid #6366F1;

    box-shadow: 0px 5px 18px rgba(30, 41, 59, 0.08);

 Text */
.stMarkdown p {
    color: #505B78;
}
}    margin-bottom: 18px;

    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    border-top-color: #EC4899;

    box-shadow: 0px 9px 22px rgba(99, 102, 241, 0.18);
}

.card h3 {
    color: #3730A3;
}

/* ==========================================
   METRIC CARDS
========================================== */

.metric-card {
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #EFF6FF
    );

    padding: 22px;
    border-radius: 18px;

    text-align: center;

    border: 1px solid #BFDBFE;
    border-bottom: 5px solid #06B6D4;

    box-shadow: 0px 5px 15px rgba(30, 41, 59, 0.07);
}

.metric-value {
    font-size: 32px;
    font-weight: bold;

    background: linear-gradient(
        90deg,
        #4F46E5,
        #0891B2,
        #059669
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ==========================================
   BUTTONS
========================================== */

.stButton button {
    background: linear-gradient(
        90deg,
        #4F46E5,
        #7C3AED,
        #DB2777
    );

    color: #FFFFFF;
    border-radius: 12px;

    border: none;

    padding: 11px 22px;
    font-weight: bold;

    transition: 0.3s; 
    }/*/* PREMIUM LAVENDER WHITE THEME */

.stApp {
    background: #F5F6FC;
}

/* Main Headings */
h1, h2, h3 {
    color: #303B63;
}

/* Feature Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DDE2F2;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(48, 59, 99, 0.06);
    padding: 10px;
}

/* Buttons */
.stButton > butto
    color: #303B63;
    border: 1px solid #D5DCF2;
    border-radius: 12px;
    font-weight: 600;
    transition: 0.3s;
}
 
.stButton > button:hover {
    background: #CBD5F0;
    color: #202B50;
    border: 1px solid #B9C7E8;
}
/* =====================================
   TALENTBRIDGE AI - NAVY & PARROT THEME
===================================== */

/* MAIN BACKGROUND */
.stApp {
    background: #F5F8FC;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #101D3A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* =====================================
   PREMIUM CENTERED BRAND HEADING
===================================== */

h1 {
    color: #14284B !important;
    font-size: 42px !important;
    font-weight: 850 !important;
    text-align: center !important;
    letter-spacing: 1.5px;
    width: 100%;
    margin: 20px auto 12px auto !important;
    padding-bottom: 12px;
    border-bottom: 3px solid #A8E63D;
    max-width: 750px;
}

h2, h3 {
    color: #263B5C !important;
    text-align: center !important;
    font-weight: 650 !important;
}

/* FEATURE CARDS */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DCE5EF;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(16, 29, 58, 0.08);
}

/* BUTTONS */
.stButton > button {
    background: #A8E63D;
    color: #10213B;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    transition: 0.3s ease;
}

/* BUTTON HOVER */
.stButton > button:hover {
    background: #8FD326;
    color: #10213B;
    border: none;
}

/* INPUT BOXES */
.stTextInput input,
.stTextArea textarea {
    background: #FFFFFF;
    border: 1px solid #CCD8E8;
    border-radius: 10px;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    border-left: 4px solid #A8E63D;
} V

/* DIVIDER */
hr {
    border-color: #DCE5EF;
}n {
    background: #E5E9FA;



    </style>
    """, unsafe_allow_html=True)
# ==========================================
# USER DATA STORAGE
# ==========================================

USER_DATA_FOLDER = "user_data"


def get_user_file(username):
    os.makedirs(USER_DATA_FOLDER, exist_ok=True)

    user_id = hashlib.sha256(
        username.encode()
    ).hexdigest()

    return os.path.join(
        USER_DATA_FOLDER,
        user_id + ".json"
    )


def save_user_data(username):

    data = {
        "created_resume": st.session_state.get(
            "created_resume", ""
        ),
        "interview_answers": st.session_state.get(
            "interview_answers", []
        )
    }

    with open(get_user_file(username), "w") as file:
        json.dump(data, file)


def load_user_data(username):

    file_path = get_user_file(username)

    if os.path.exists(file_path):

        with open(file_path, "r") as file:
            data = json.load(file)

    else:
        data = {}

    st.session_state["created_resume"] = data.get(
        "created_resume", ""
    )

    st.session_state["interview_answers"] = data.get(
        "interview_answers", []
    )


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = "username"

load_user_data("username")


# ==========================================
# SKILLS DATABASE
# ==========================================

SKILLS = [
    "Python", "Java", "C++", "C#", "SQL",
    "HTML", "CSS", "JavaScript", "React",
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "NLP",
    "Data Analysis", "Pandas", "NumPy",
    "TensorFlow", "PyTorch", "Excel",
    "Power BI", "Tableau", "DBMS",
    "MySQL", "Django", "Flask",
    "Scikit-learn", "Git", "AWS",
    "Computer Networks", "Operating Systems"
]


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================
def create_resume_pdf(resume_text,
    template="Classic"):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    left = 50
    y = height - 50

    lines = resume_text.split("\n")

    name = lines[0] if lines else "My Resume"
    remaining_lines = lines[1:]

    # Template colors
    if template == "Modern":
        primary = HexColor("#5497E3")
        heading_color = HexColor("#2874A6")
    elif template == "Classic":
        primary = HexColor("#221540")
        heading_color = HexColor("#597186")
    else:
        primary = HexColor("#000000")
        heading_color = HexColor("#000000")

    # Header background
    if template == "Modern":
        pdf.setFillColor(primary)
        pdf.rect(0, height - 145, width, 145, fill=1, stroke=0)

    # Candidate name
    pdf.setFillColor(
        HexColor("#FFFFFF") if template == "Modern"
        else primary
    )
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(left, height - 65, name[:45])

    y = height - 95

    # Contact information
    pdf.setFont("Helvetica", 9)
    contact_color = (
        HexColor("#FFFFFF") if template == "Modern"
        else HexColor("#555555")
    )
    pdf.setFillColor(contact_color)

    for line in remaining_lines[:3]:
        if line.strip():
            pdf.drawString(left, y, line[:90])
            y -= 15

    y = height - 175 if template == "Modern" else height - 125

    # Resume content
    headings = [
        "CAREER OBJECTIVE",
        "EDUCATION",
        "TECHNICAL SKILLS",
        "PROJECTS",
        "CERTIFICATIONS",
        "EXPERIENCE"
    ]

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(HexColor("#333333"))

    for line in remaining_lines[3:]:

        line = line.strip()

        if not line:
            y -= 8
            continue

        if y < 65:
            pdf.showPage()
            y = height - 50

        if line.upper() in headings:

            y -= 10
            pdf.setFillColor(heading_color)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(left, y, line.upper())

            y -= 18

            pdf.setStrokeColor(heading_color)
            pdf.line(left, y, width - left, y)

            y -= 12

            pdf.setFillColor(HexColor("#333333"))
            pdf.setFont("Helvetica", 10)

        else:
            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(HexColor("#333333"))

            wrapped = simpleSplit(
                line, "Helvetica", 10, width - 100
            )

            for item in wrapped:
                if y < 50:
                    pdf.showPage()
                    y = height - 50

                pdf.drawString(left, y, item)
        y -= 16

    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()
def extract_resume(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ==========================================
# RESUME INFORMATION EXTRACTION
# ==========================================

def extract_information(text):

    email = re.findall(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    phone = re.findall(
        r'\+?\d[\d\s().-]{8,}\d',
        text
    )

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    name = "Not detected"

    for line in lines[:8]:
        if (
            len(line) < 55
            and not re.search(r'@|https?://|resume|phone|email', line, re.I)
            and not any(char.isdigit() for char in line)
        ):
            name = line
            break

    return {
        "Name": name,
        "Email": email[0] if email else "Not detected",
        "Phone": phone[0] if phone else "Not detected"
    }


# ==========================================
# SKILL DETECTION
# ==========================================

def detect_skills(text):

    detected = []

    for skill in SKILLS:

        pattern = (
            r'(?<![a-z0-9])'
            + re.escape(skill.lower())
            + r'(?![a-z0-9])'
        )

        if re.search(pattern, text.lower()):
            detected.append(skill)

    return detected


# ==========================================
# AI MATCHING ENGINE
# ==========================================

def calculate_match(resume, job):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        [resume, job]
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# ==========================================
# JOB RECOMMENDATION
# ==========================================

JOB_ROLES = {

    "Python Developer": [
        "Python", "SQL", "Django", "Flask", "Git"
    ],

    "Data Analyst": [
        "Python", "SQL", "Excel",
        "Power BI", "Data Analysis"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning",
        "Deep Learning", "TensorFlow"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React"
    ],

    "AI Developer": [
        "Python", "Artificial Intelligence",
        "Machine Learning", "NLP"
    ],

    "Database Developer": [
        "SQL", "MySQL", "DBMS"
    ]

}


def recommend_jobs(candidate_skills):

    recommendations = []

    for role, required in JOB_ROLES.items():

        matched = [
            skill for skill in required
            if skill in candidate_skills
        ]

        score = round(
            len(matched) / len(required) * 100
        )

        recommendations.append(
            (role, score, matched)
        )

    return sorted(
        recommendations,
        key=lambda x: x[1],
        reverse=True
    )
# ==========================================
# USER AUTHENTICATION
# ==========================================

USER_FILE = "users.json"


def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# ==========================================
# PUBLIC DASHBOARD - TALENTBRIDGE AI
# ==========================================

if st.session_state.get("page", "Home") == "Home":
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("pending_feature", None)
    st.session_state.setdefault("page", "Home")

    FEATURES = {
        "Resume Screening": "Resume Analysis",
        "Job Matching": "Job Recommendations",
        "Resume Builder": "Resume Builder",
        "Mock Interview": "Mock Interview",
        "Performance Analytics": "Performance Analytics",
        "AI Career Assistant": "AI Career Assistant"
    }

    if not st.session_state["logged_in"] and not st.session_state["pending_feature"]:

        st.title("🚀 TalentBridge AI")
        st.subheader("AI Powered Career Development Platform")

        st.markdown("""
<p style="text-align:center; color:#263B5C; font-size:19px; font-weight:600; margin:20px auto;">
Build your resume,
<span style="color:#78B82A;">discover suitable jobs</span>
and prepare for your
<span style="color:#78B82A;">dream career.</span>
</p>
""", unsafe_allow_html=True)
    
    

        st.markdown("---")
        st.subheader("Explore Our Features")

        feature_list = list(FEATURES.keys())

        for row in range(0, len(feature_list), 3):
            cols = st.columns(3)

            for i, col in enumerate(cols):
                index = row + i

                if index < len(feature_list):
                    feature = feature_list[index]

                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                background:white;
                                padding:22px;
                                border-radius:15px;
                                text-align:center;
                                min-height:130px;
                                box-shadow:0 3px 12px #00000015;
                            ">
                                <h3>{feature}</h3>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            f"Explore {feature}",
                            key=f"public_{index}",
                            use_container_width=True
                        ):
                            st.session_state["pending_feature"] = feature
                            st.rerun()

        st.markdown("---")

        st.subheader("How Our System Works")

        st.write("1. Upload candidate resume.")
        st.write("2. Extract resume information.")
        st.write("3. Detect technical skills.")
        st.write("4. Analyze job description.")
        st.write("5. Calculate matching score.")
        st.write("6. Recommend suitable job roles.")

        st.markdown("---")
        st.info("🔐 Login or Register to access platform features.")

        st.stop()


# ==========================================
# LOGIN AND REGISTRATION SCREEN
# ==========================================

if not st.session_state["logged_in"]:

    st.markdown(
        "<h1 style='text-align:center;color:#2563EB;'>🚀 TalentBridge AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>AI Career Development Platform</h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        login_tab, register_tab = st.tabs(
            ["🔐 Login", "📝 Register"]
        )

        users = load_users()

        with login_tab:

            st.subheader("Welcome Back!")

            username = st.text_input("Username", key="login_user")
            password = st.text_input(
                "Password",
                type="password",
                key="login_pass"
            )

            if st.button("Login", use_container_width=True):

                if username in users and users[username] == hash_password(password):

                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

        with register_tab:

            st.subheader("Create Your Account")

            new_user = st.text_input("Create Username", key="new_user")
            new_pass = st.text_input(
                "Create Password",
                type="password",
                key="new_pass"
            )

            confirm_pass = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_pass"
            )

            if st.button("Register", use_container_width=True):

                users = load_users()

                if not new_user.strip() or not new_pass:
                    st.warning("Please fill in all fields.")

                elif len(new_pass) < 8:
                    st.warning("Password must be at least 8 characters.")

                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")

                elif new_user in users:
                    st.error("Username already exists.")

                else:
                    users[new_user] = hash_password(new_pass)
                    save_users(users)
                    st.success("Registration successful! Please login.")

    st.stop()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🤖 TalentBridge AI")

    st.caption("Intelligent Recruitment System")

    st.markdown("---")

# =====================================
# HOME NAVIGATION BUTTON
# =====================================

    page = st.radio(
        "NAVIGATION",
        [
            "Home",
            "Resume Builder",
            "Resume Analysis",
            "Job Recommendations",
            "Mock Interview",
            "AI Career Assistant",
            "About Project"
        ]
    )

    st.markdown("---")

    st.info(
        "AI-powered resume screening and job matching."
    )

st.sidebar.markdown("---")

st.sidebar.write(
    f"👤 Welcome, {st.session_state['username']}"
)

if st.sidebar.button("🚪 Logout", use_container_width=True):

    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

    st.rerun()

# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

        st.title("🚀 TalentBridge AI")
        st.subheader("AI Powered Career Development Platform")

        st.markdown("""
<p style="text-align:center; color:#263B5C; font-size:19px; font-weight:600; margin:20px auto;">
Build your resume,
<span style="color:#78B82A;">discover suitable jobs</span>
and prepare for your
<span style="color:#78B82A;">dream career.</span>
</p>
""", unsafe_allow_html=True)
    
    

        st.markdown("---")
        st.subheader("Explore Our Features")

        feature_list = list(FEATURES.keys())

        for row in range(0, len(feature_list), 3):
            cols = st.columns(3)

            for i, col in enumerate(cols):
                index = row + i

                if index < len(feature_list):
                    feature = feature_list[index]

                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                background:white;
                                padding:22px;
                                border-radius:15px;
                                text-align:center;
                                min-height:130px;
                                box-shadow:0 3px 12px #00000015;
                            ">
                                <h3>{feature}</h3>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            f"Explore {feature}",
                            key=f"public_{index}",
                            use_container_width=True
                        ):
                            st.session_state["pending_feature"] = feature
                            st.rerun()

        st.markdown("---")

        st.subheader("How Our System Works")

        st.write("1. Upload candidate resume.")
        st.write("2. Extract resume information.")
        st.write("3. Detect technical skills.")
        st.write("4. Analyze job description.")
        st.write("5. Calculate matching score.")
        st.write("6. Recommend suitable job roles.")

        st.markdown("---")
    

        st.stop()

# ==========================================
# RESUME ANALYSIS PAGE
# ==========================================

elif page == "Resume Analysis":

    st.markdown(
        '<div class="main-title">Resume Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Analyze candidate resumes using AI and NLP techniques.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.markdown("### 📄 Upload Resume")

        uploaded_file = st.file_uploader(
            "Upload PDF Resume",
            type=["pdf"]
        )

    with right:

        st.markdown("### 💼 Job Information")

        job_title = st.text_input(
            "Job Role",
            placeholder="Python Developer"
        )

        company = st.text_input(
            "Company Name",
            placeholder="Company name"
        )

    job_description = st.text_area(
        "Enter Job Description",
        height=180,
        placeholder="Enter the complete job description and required skills..."
    )

    st.write("")

    analyze = st.button(
        "🚀 ANALYZE RESUME",
        use_container_width=True
    )

    if analyze:

        if uploaded_file is None:

            st.error("Please upload a PDF resume.")

        elif not job_description.strip():

            st.error("Please enter a job description.")

        else:

            try:

                resume_text = extract_resume(
                    uploaded_file
                )

                if not resume_text.strip():

                    st.error(
                        "No readable text found in PDF. Try a text-based PDF."
                    )

                else:

                    candidate = extract_information(
                        resume_text
                    )

                    resume_skills = detect_skills(
                        resume_text
                    )

                    job_skills = detect_skills(
                        job_description
                    )

                    matched_skills = [
                        skill for skill in job_skills
                        if skill in resume_skills
                    ]

                    missing_skills = [
                        skill for skill in job_skills
                        if skill not in resume_skills
                    ]

                    skill_score = (
                        len(matched_skills) /
                        len(job_skills) * 100
                        if job_skills else 0
                    )

                    text_score = calculate_match(
                        resume_text,
                        job_description
                    )

                    if job_skills:

                        final_score = round(
                            0.70 * skill_score +
                            0.30 * text_score
                        )

                    else:

                        final_score = text_score

                    st.session_state["result"] = {
                        "candidate": candidate,
                        "resume_skills": resume_skills,
                        "job_skills": job_skills,
                        "matched_skills": matched_skills,
                        "missing_skills": missing_skills,
                        "score": final_score,
                        "text_score": text_score,
                        "job_title": job_title
                    }

            except Exception as error:

                st.error(
                    f"Error processing resume: {error}"
                )

    # ======================================
    # DISPLAY RESULTS
    # ======================================

    if "result" in st.session_state:

        result = st.session_state["result"]

        st.markdown("---")

        st.markdown(
            '<div class="main-title">Analysis Results</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)

        with a:

            st.markdown(f"""
            <div class="metric-card">
            <h4>Overall Match</h4>
            <div class="metric-value">{result['score']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with b:

            st.markdown(f"""
            <div class="metric-card">
            <h4>Matched Skills</h4>
            <div class="metric-value">{len(result['matched_skills'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with c:

            st.markdown(f"""
            <div class="metric-card">
            <h4>Missing Skills</h4>
            <div class="metric-value">{len(result['missing_skills'])}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        st.progress(
            result["score"] / 100
        )

        st.caption(
            "Indicative score: 70% skill coverage + 30% TF-IDF text similarity when job skills are detected. This is not a validated hiring assessment."
        )

        st.markdown("---")

        st.subheader("👤 Candidate Information")

        x, y, z = st.columns(3)

        x.write(
            f"**Name:** {result['candidate']['Name']}"
        )

        y.write(
            f"**Email:** {result['candidate']['Email']}"
        )

        z.write(
            f"**Phone:** {result['candidate']['Phone']}"
        )

        st.markdown("---")

        x, y = st.columns(2)

        with x:

            st.subheader("✅ Matching Skills")

            if result["matched_skills"]:

                for skill in result["matched_skills"]:

                    st.success(skill)

            else:

                st.warning("No matching skills found.")

        with y:

            st.subheader("❌ Missing Skills")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:

                    st.warning(skill)

            else:

                st.success("No missing detected skills.")

        st.markdown("---")

        st.subheader("🧠 All Detected Resume Skills")

        st.write(
            ", ".join(result["resume_skills"])
            if result["resume_skills"]
            else "No skills detected."
        )

        st.subheader("📊 Text Similarity")

        st.metric(
            "Resume and Job Description Similarity",
            f"{result['text_score']}%"
        )

        report = f"""
TALENTBRIDGE AI - RESUME ANALYSIS REPORT

Candidate: {result['candidate']['Name']}
Email: {result['candidate']['Email']}
Phone: {result['candidate']['Phone']}

Job Role: {result['job_title']}
Company: {company}

Overall Match: {result['score']}%

Matched Skills:
{', '.join(result['matched_skills'])}

Missing Skills:
{', '.join(result['missing_skills'])}

Resume Skills:
{', '.join(result['resume_skills'])}

Text Similarity: {result['text_score']}%

Note: This is an indicative automated analysis, not a hiring decision.
"""

        st.download_button(
            "⬇ Download Analysis Report",
            report,
            file_name="Resume_Analysis_Report.txt",
            mime="text/plain"
        )


# ==========================================
# JOB RECOMMENDATION PAGE
# ==========================================

elif page == "Job Recommendations":

    st.markdown(
        '<div class="main-title">Job Recommendations</div>',
        unsafe_allow_html=True
    )

    if "result" not in st.session_state:

        st.info(
            "Please analyze a resume first."
        )

    else:

        result = st.session_state["result"]

        recommendations = recommend_jobs(
            result["resume_skills"]
        )

        st.subheader(
            "Recommended Career Opportunities"
        )

        for role, score, skills in recommendations:

            with st.container(border=True):

                st.markdown(f"### 💼 {role}")

                st.metric(
                    "Skills Match",
                    f"{score}%"
                )

                st.progress(score / 100)

                st.write(
                    "**Relevant Skills:**",
                    ", ".join(skills) if skills else "None detected"
                )

# ==========================================
# MOCK INTERVIEW MODULE
# ==========================================

elif page == "Mock Interview":

    st.title("🎤 AI Mock Interview")
    st.write("Practice interviews and improve your communication skills.")

    st.markdown("---")

    st.subheader("Select Your Interview Role")

    job_role = st.selectbox(
        "Choose Job Role",
        [
            "Python Developer",
            "Data Analyst",
            "Machine Learning Engineer",
            "Web Developer",
            "AI Developer"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        ["Fresher", "Intermediate", "Experienced"]
    )

    questions = {
        "Python Developer": [
            "What is Python?",
            "What is the difference between a list and a tuple?",
            "What are Python functions?",
            "What is OOP in Python?",
            "What is exception handling?"
        ],

        "Data Analyst": [
            "What is Data Analysis?",
            "What is the difference between SQL and Excel?",
            "What is data cleaning?",
            "What is Pandas?",
            "What is data visualization?"
        ],

        "Machine Learning Engineer": [
            "What is Machine Learning?",
            "What is supervised learning?",
            "What is overfitting?",
            "What is feature engineering?",
            "What is model training?"
        ],

        "Web Developer": [
            "What is HTML?",
            "What is CSS?",
            "What is JavaScript?",
            "What is frontend development?",
            "What is backend development?"
        ],

        "AI Developer": [
            "What is Artificial Intelligence?",
            "What is NLP?",
            "What is Deep Learning?",
            "What is a neural network?",
            "What is Generative AI?"
        ]
    }
    if "interview_started" not in st.session_state:
        st.session_state["interview_started"] = False

    if "interview_answers" not in st.session_state:
        st.session_state["interview_answers"] = []

    if st.button("🚀 Start Interview"):

        st.session_state["interview_role"] = job_role
        st.session_state["interview_level"] = experience
        st.session_state["interview_started"] = True
        st.session_state.setdefault("interview_answers", [])

    if st.session_state["interview_started"]:

        selected_questions = questions[
            st.session_state["interview_role"]
        ]

        st.success("Your interview is ready!")

        total_questions = len(selected_questions)

        answered_questions = len({
    item["question"]
    for item in st.session_state["interview_answers"]
})

        progress = min(
            answered_questions / total_questions, 1.0
        )

        st.progress(progress)

        st.caption(
            f"Interview Progress: {answered_questions}/{total_questions} questions answered"
        )
        st.markdown("---")
        st.subheader("📝 Interview Questions")

        for i, question in enumerate(selected_questions, 1):
            st.write(f"**Question {i}:** {question}")
            st.markdown("---")

        st.subheader("✍️ Submit Your Answer")

        answered_question_texts = {
            item["question"]
            for item in st.session_state["interview_answers"]
        }

        unanswered_questions = [
            q for q in selected_questions
            if q not in answered_question_texts
        ]

        if unanswered_questions:
            with st.form("interview_answer_form"):
                selected_question = st.selectbox(
                    "Select Question",
                    unanswered_questions
                )

                user_answer = st.text_area(
                    "Write Your Answer",
                    placeholder="Type your interview answer here..."
                )

                submit_answer = st.form_submit_button("Submit Answer")

            if submit_answer:
                if user_answer.strip():
                    word_count = len(user_answer.split())

                    st.session_state["interview_answers"].append({
                        "question": selected_question,
                        "answer": user_answer,
                        "words": word_count
                    })

                    st.success("Answer submitted successfully!")
                    st.subheader("📊 Answer Feedback")

                    if word_count < 15:
                        st.warning(
                            "Your answer is too short. Try explaining with an example."
                        )
                    elif word_count < 40:
                        st.info(
                            "Good attempt! Add more technical details."
                        )
                    else:
                        st.success(
                            "Good answer length! Keep your explanation clear and relevant."
                        )
                else:
                    st.error("Please write your answer first.")
        else:
            st.success("🎉 All interview questions have been answered!")

        st.markdown("---")
        st.subheader("📊 Interview Performance Report")

        total_answers = len(
            st.session_state["interview_answers"]
        )

        if total_answers == total_questions:
            st.success("🎉 Congratulations! You have completed the interview.")
        else:
            remaining = total_questions - total_answers
            st.info(f"📝 {remaining} questions remaining.")

        st.metric("Questions Answered", total_answers)

        if total_answers > 0:

            average_words = sum(
                item["words"]
                for item in st.session_state["interview_answers"]
            ) / total_answers

            st.metric(
                "Average Answer Length",
                f"{average_words:.0f} words"
            )
            st.markdown("---")
        st.subheader("📋 Review Your Answers")

        if total_answers > 0:

            with st.expander("View All Submitted Answers"):

                for i, item in enumerate(
                    st.session_state["interview_answers"], 1
                ):

                    st.write(f"**Question {i}:** {item['question']}")

                    st.write("**Your Answer:**")
                    st.write(item["answer"])

                    st.caption(f"Word Count: {item['words']}")

                    st.markdown("---")

        else:
            st.info("No answers submitted yet.")
            
# ==========================================
# AI CAREER ASSISTANT
# ==========================================

elif page == "AI Career Assistant":

    st.title("🤖 AI Career Assistant")

    st.subheader("Your Personal Career Guidance Centre")

    st.write(
        "Get career advice, resume improvement tips, "
        "job recommendations and interview preparation."
    )

    st.markdown("---")

    st.subheader("🎯 Select Your Career Goal")

    career_goal = st.selectbox(
        "What do you want help with?",
        [
            "Choose a Topic",
            "Resume Improvement",
            "Job Recommendations",
            "Interview Preparation",
            "Technical Skills",
            "Career Roadmap"
        ]
    )

    job_role = st.selectbox(
        "Select Your Target Job Role",
        [
            "Python Developer",
            "Data Analyst",
            "Machine Learning Engineer",
            "AI Developer",
            "Web Developer"
        ]
    )

    st.markdown("---")

    st.subheader("💬 Ask Your Career Question")

    if "career_chat" not in st.session_state:
        st.session_state["career_chat"] = []

    with st.form("career_assistant_form"):

        question = st.text_area(
            "Enter your question",
            placeholder="Example: How can I prepare for a Data Analyst job?"
        )

        submit = st.form_submit_button(
            "🤖 Get Career Guidance"
        )

    if submit:

        if question.strip():

            query = question.lower()

            if career_goal == "Resume Improvement" or "resume" in query:

                response = """
                 RESUME IMPROVEMENT PLAN

                1. Write a clear professional summary.
                2. Add your technical skills.
                3. Include academic and personal projects.
                4. Mention relevant certifications.
                5. Use simple ATS-friendly formatting.

                Recommendation: Highlight your practical projects
                and explain your contribution clearly.
                """

            elif career_goal == "Job Recommendations" or "job" in query:

                response = f"""
                 CAREER RECOMMENDATION

                Your selected target role is: {job_role}

                Recommended preparation:

                1. Learn the fundamentals of the role.
                2. Build practical projects.
                3. Improve problem-solving skills.
                4. Practise technical interview questions.
                5. Prepare your resume for this role.
                """

            elif career_goal == "Interview Preparation" or "interview" in query:

                response = """
                 INTERVIEW PREPARATION PLAN

                1. Prepare your self-introduction.
                2. Study technical fundamentals.
                3. Practise explaining your projects.
                4. Prepare common HR questions.
                5. Improve communication and confidence.

                Tip: Practise answering questions in your
                own words rather than memorising answers.
                """

            elif career_goal == "Technical Skills" or "skill" in query:

                response = f"""
                 TECHNICAL SKILL ROADMAP

                Target Role: {job_role}

                Recommended learning areas:

                1. Python programming.
                2. Data structures and problem solving.
                3. SQL and database fundamentals.
                4. Practical project development.
                5. Git and GitHub basics.

                Focus on understanding concepts and building
                small projects while learning.
                """

            elif career_goal == "Career Roadmap" or "career" in query:

                response = f"""
                 CAREER DEVELOPMENT ROADMAP

                Target Role: {job_role}

                Phase 1: Learn programming fundamentals.

                Phase 2: Develop technical skills.

                Phase 3: Build two or three practical projects.

                Phase 4: Create a professional resume.

                Phase 5: Practise mock interviews.

                Phase 6: Apply for internships and jobs.
                """

            else:

                response = """
                 CAREER GUIDANCE

                I can help you with:

                Resume improvement
                 Job recommendations
                 Interview preparation
                 Technical skills
                 Career roadmaps

                Select a career topic above to receive
                more focused guidance.
                """

            st.session_state["career_chat"].append(
                {
                    "question": question,
                    "response": response
                }
            )

        else:
            st.warning("Please enter your question.")

    st.markdown("---")

    st.subheader(" Career Assistant Conversation")

    for chat in st.session_state["career_chat"]:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.markdown(chat["response"])

    if st.button(" Clear Chat History"):
        st.session_state["career_chat"] = []
        st.rerun()

# ==========================================
# ABOUT PROJECT
# ==========================================

elif page == "About Project":

    st.markdown(
        '<div class="main-title">About Our Project</div>',
        unsafe_allow_html=True
    )

    st.write("""
    TalentBridge AI is an AI-assisted resume building , screening
    and job matching application with personalized mock interview module.

    The system analyzes candidate resumes and compares
    their skills with job descriptions.

    It helps identify relevant skills, missing skills
    and potential job opportunities.
    """)

    st.subheader("Technologies Used")

    technologies = [
        "HTML",
        "CSS",
        "Python",
        "Streamlit",
        "PyPDF",
        "Scikit-learn",
        "Natural Language Processing",
        "TF-IDF",
        "Cosine Similarity",
        "Report Lab",
        "Machine Learning Concepts"
    ]

    for technology in technologies:

        st.success(technology)

    st.subheader("Project Objectives")

    st.write("""
    1. Automate basic resume screening.
    2. Extract candidate information.
    3. Identify technical skills.
    4. Compare resumes with job descriptions.
    5. Calculate an indicative matching score.
    6. Recommend relevant job roles.
    7. Provide a Mock Interview Module for practice.
    8. Generate professional resumes.
    """)

    st.info(
        "Developed as a B.Tech AIML minor project by 3rd year students."
        
    )
# ==========================================
# RESUME BUILDER MODULE
# ==========================================


elif page == "Resume Builder":

    st.markdown(
        '<div class="main-title">AI Resume Builder</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Create your professional resume easily.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    with st.form("resume_builder_form"):

        st.subheader(" Personal Information")
        resume_template = st.selectbox(
    "Choose Resume Template",
    ["Classic", "Modern", "ATS-Friendly"]
)
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")

        st.markdown("---")

        st.subheader(" Career Objective")

        objective = st.text_area(
            "Career Objective",
            placeholder="Write your career goals..."
        )

        st.markdown("---")

        st.subheader(" Education")

        degree = st.text_input("Degree")
        college = st.text_input("College Name")
        cgpa = st.text_input("CGPA / Percentage")
        graduation = st.text_input("Graduation Year")

        st.markdown("---")

        st.subheader(" Technical Skills")

        skills = st.text_area(
            "Enter Your Skills",
            placeholder="Python, SQL, HTML, CSS..."
        )

        st.markdown("---")

        st.subheader(" Projects")

        projects = st.text_area(
            "Project Details"
        )

        st.markdown("---")

        st.subheader(" Certifications")

        certifications = st.text_area(
            "Your Certifications"
        )

        st.markdown("---")

        st.subheader(" Experience")

        experience = st.text_area(
            "Internship / Experience"
        )

        submitted = st.form_submit_button(
            " Generate My Resume",
            use_container_width=True
        )

    if submitted:

        if not name or not email or not degree:

            st.error(
                "Please fill Name, Email and Degree."
            )

        else:

            resume = f"""
{ name.upper() }

Email: {email}
Phone: {phone}
Address: {address}

CAREER OBJECTIVE
{objective}

EDUCATION
Degree: {degree}
College: {college}
CGPA: {cgpa}
Graduation Year: {graduation}

TECHNICAL SKILLS
{skills}

PROJECTS
{projects}

CERTIFICATIONS
{certifications}

EXPERIENCE
{experience}
"""

            st.session_state["created_resume"] = resume

    if "created_resume" in st.session_state:

        st.markdown("---")

        st.subheader(" Your Professional Resume is Ready!")
        st.caption("Review your resume below and download it in your preferred format.")

        st.markdown(
            f"""
            <div style= "
                background: white;
                color: #263746;
                padding: 30px;
                border-radius: 15px;
                border: 2px solid #2874A6;
                box-shadow: 0 4px 15px rgba(0,0,0,0.12);
                width: 100%;
                font-family: Arial;
                line-height: 1.7;
            ">
                {st.session_state["created_resume"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.download_button(
            label="⬇ Download Resume",
            data=st.session_state["created_resume"],
            file_name="Professional_Resume.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.download_button(
            label="📄 Download Resume as PDF",
            data=create_resume_pdf(
                st.session_state["created_resume"],
                resume_template,
            ),
            file_name="My_Professional_Resume.pdf",
            mime="application/pdf",
        )