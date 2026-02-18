import streamlit as st
import pandas as pd
import numpy as np
import time
from pathlib import Path

st.set_page_config(page_title="Tovi Joshua | Portfolio", page_icon="✨", layout="wide")

CSS = """
<style>
body {background-color: #f8fafc}
.profile-photo {border-radius: 50%; border: 4px solid #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.15)}
.profile-photo {border-radius: 50%; border: 4px solid #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.15)}
.card {background: linear-gradient(180deg, #ffffff, #f6f9ff); padding: 18px; border-radius: 12px; box-shadow: 0 6px 20px rgba(59,130,246,0.06); color: #0f172a}
.skill-label {font-weight:600; color:#0f172a}
.timeline-item {padding:10px 0}
.small-muted {color:#6b7280; font-size:13px}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Resolve profile image relative to this file so it works locally and on Streamlit Cloud
PROFILE_IMG = str(Path(__file__).resolve().parents[1] / "profilepic" / "portfolio1.jpg")
PROJECT_IMG = "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80"


def show_home():
    st.title("Welcome — Personal Portfolio")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Hi, I'm Tovi Joshua")
        st.write("IT student focused on backend development, API design, and building structured systems using NestJS and Python.")
        st.markdown("**Currently:** Backend-focused student · Open to internships")

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.metric("Years Learning", "4")
        c2.metric("Projects Built", "12")
        c3.metric("Primary Focus", "Backend")

        st.markdown("---")

        if st.button("Say hello 👋"):
            st.success("Thanks for visiting! Feel free to message me in the Contact section.")

        if st.checkbox("Show sample activity chart"):
            chart_data = pd.DataFrame(
                np.random.randint(50, 500, 12),
                columns=["Activity"]
            )
            st.line_chart(chart_data)

        st.markdown("[GitHub](https://github.com/Choovyy)")
        

    with col2:
        st.image(PROFILE_IMG, width=260)
        progress = st.progress(0)
        for i in range(0, 101, 10):
            time.sleep(0.01)
            progress.progress(i)


def show_about():
    st.header("About Me")

    st.markdown("""
    <div class='card'>
    I am an IT student passionate about backend systems, API security, and clean architecture.
    I enjoy building structured applications and understanding how components connect together.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Education"):
        st.write("Bachelor of Science in IT")

    tab1, tab2 = st.tabs(["Mission", "Goals"])

    with tab1:
        st.write("Build reliable backend systems that follow strong architectural principles.")

    with tab2:
        st.write("Grow into a backend engineer role and continuously improve system design skills.")


def show_skills():
    st.header("Skills")

    skills = {
        "Python": 0.85,
        "NestJS": 0.8,
        "JavaScript": 0.75,
        "SQL": 0.7,
        "Supabase": 0.7,
        "Docker": 0.6
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        for name, value in skills.items():
            st.markdown(f"<div class='skill-label'>{name}</div>", unsafe_allow_html=True)
            st.progress(value)

        df = pd.DataFrame({
            "Skill": list(skills.keys()),
            "Proficiency (%)": [int(v * 100) for v in skills.values()]
        })
        st.dataframe(df)

    with col2:
        st.subheader("Skill Overview")
        st.bar_chart(df.set_index("Skill"))
        st.metric("Strongest Skill", max(skills, key=skills.get))


def show_projects():
    st.header("Projects")

    projects = [
        {
            "title": "Surplus Funds API",
            "desc": "RESTful API managing surplus funds lifecycle with validation and business rules.",
            "tech": ["NestJS", "Supabase", "TypeScript"],
            "difficulty": 4
        },
        {
            "title": "CapstoneConnect Matching System",
            "desc": "AI-based teammate matching using SBERT and FAISS with similarity scoring.",
            "tech": ["Python", "FastAPI", "FAISS"],
            "difficulty": 5
        },
        {
            "title": "Lead Intake System",
            "desc": "Multi-table relational intake system with DTO validation and API guards.",
            "tech": ["NestJS", "MySQL", "Class-validator"],
            "difficulty": 4
        }
    ]

    all_tech = sorted({t for p in projects for t in p["tech"]})
    selected = st.multiselect("Filter by Tech", all_tech, default=all_tech)
    max_difficulty = st.slider("Max Difficulty", 1, 5, 5)

    filtered = [
        p for p in projects
        if any(t in selected for t in p["tech"]) and p["difficulty"] <= max_difficulty
    ]

    st.info(f"Showing {len(filtered)} projects")

    for p in filtered:
        st.subheader(p["title"])
        st.write(p["desc"])
        st.write("Tech Stack:", ", ".join(p["tech"]))

        with st.expander("Details"):
            st.write("Difficulty Level:", p["difficulty"])

        st.download_button(
            f"Download {p['title']} Info",
            data=p["desc"].encode("utf-8"),
            file_name=f"{p['title']}.txt"
        )

        st.markdown("---")


def show_experience():
    st.header("Experience")

    timeline = [
        {
            "role": "Backend Developer (Academic Projects)",
            "company": "University Projects",
            "years": "2024 - Present",
            "summary": "Built structured REST APIs using NestJS and integrated Supabase with validation."
        },
        {
            "role": "System Design Learner",
            "company": "Self Learning",
            "years": "2023 - Present",
            "summary": "Studied API security, rate limiting, and clean architecture principles."
        }
    ]

    for item in timeline:
        st.markdown(f"""
        <div class='timeline-item'>
        <strong>{item['role']}</strong> — {item['company']}
        <div class='small-muted'>{item['years']}</div>
        <div>{item['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.table(pd.DataFrame(timeline)[["role", "company", "years"]])


def show_contact():
    st.header("Contact")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            if not name or not email or not message:
                st.error("Please complete all fields.")
            else:
                st.session_state["messages"].append({
                    "name": name,
                    "email": email,
                    "message": message
                })
                st.success("Message sent successfully!")

    if st.session_state["messages"]:
        with st.expander("Recent Messages"):
            for m in reversed(st.session_state["messages"][-5:]):
                st.write(f"**{m['name']}** ({m['email']})")
                st.write(m["message"])
                st.markdown("---")

    resume_text = """Tovi Joshua
IT Student
Backend Developer

Skills:
- NestJS
- Python
- SQL
- Supabase
- API Security

Projects:
- Surplus Funds API
- CapstoneConnect Matching System
- Lead Intake System
"""
    st.download_button("Download Resume", resume_text.encode("utf-8"), "resume.txt")


def main():
    # Show profile image if present, otherwise fall back to a remote placeholder
    profile_path = Path(PROFILE_IMG)
    if profile_path.exists():
        st.sidebar.image(str(profile_path), width=120)
    else:
        st.sidebar.image(PROJECT_IMG, width=120)
    menu = st.sidebar.radio("Navigation", [
        "Home",
        "About Me",
        "Skills",
        "Projects",
        "Experience",
        "Contact"
    ])

    if menu == "Home":
        show_home()
    elif menu == "About Me":
        show_about()
    elif menu == "Skills":
        show_skills()
    elif menu == "Projects":
        show_projects()
    elif menu == "Experience":
        show_experience()
    elif menu == "Contact":
        show_contact()


if __name__ == "__main__":
    main()
