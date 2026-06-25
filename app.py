import streamlit as st
from ai_questions import generate_ai_questions
from parser import extract_text
import pandas as pd

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #4CAF50;
}

.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

.stTextArea textarea {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
# 🤖 AI Interview Assistant

### AI-Powered Resume Analysis & Interview Preparation Platform

Upload your resume, analyze ATS score, match with job descriptions, and generate personalized interview questions.
""")


def calculate_ats_score(resume_text):

    skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "streamlit",
        "git",
        "github",
        "power bi",
        "excel",
        "data analysis"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)

    ats_score = min(len(found_skills) * 8, 100)

    return ats_score, found_skills


def match_resume_jd(resume_text, jd_text):

    skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "streamlit",
        "git",
        "github",
        "power bi",
        "excel",
        "aws"
    ]

    matched = []
    missing = []

    for skill in skills:

        if skill.lower() in jd_text.lower():

            if skill.lower() in resume_text.lower():
                matched.append(skill)
            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    if total == 0:
        score = 0
    else:
        score = int((len(matched) / total) * 100)

    return score, matched, missing


uploaded_files = st.file_uploader(
    "📄 Upload Resume(s)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    results = []

    for uploaded_file in uploaded_files:

        resume_text = extract_text(uploaded_file)

        st.markdown("---")

        st.subheader(f"👤 {uploaded_file.name}")

        ats_score, found_skills = calculate_ats_score(
            resume_text
        )

        st.metric(
            label="ATS Score",
            value=f"{ats_score}/100"
        )

        st.progress(ats_score / 100)

        st.subheader("🛠 Skills Found")

        col1, col2 = st.columns(2)

        half = len(found_skills) // 2 + 1

        with col1:
            for skill in found_skills[:half]:
                st.success(skill)

        with col2:
            for skill in found_skills[half:]:
                st.success(skill)

        results.append({
            "Candidate": uploaded_file.name,
            "ATS Score": ats_score,
            "Skills Found": len(found_skills)
        })

        jd_text = st.text_area(
            f"📄 Paste JD for {uploaded_file.name}",
            key=uploaded_file.name
        )

        if jd_text:

            score, matched, missing = match_resume_jd(
                resume_text,
                jd_text
            )

            st.subheader("📄 Resume vs JD Match")

            st.metric(
                label="Match Score",
                value=f"{score}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Matched Skills")

                for skill in matched:
                    st.success(skill)

            with col2:

                st.subheader("❌ Missing Skills")

                for skill in missing:
                    st.error(skill)

        if st.button(
            f"🚀 Generate Questions - {uploaded_file.name}"
        ):

            ai_questions = generate_ai_questions(
                resume_text
            )

            st.subheader(
                f"🎯 Questions for {uploaded_file.name}"
            )

            st.markdown(
                f'''
                <div style="
                font-size:22px;
                line-height:2;
                padding:20px;
                background-color:#1E1E1E;
                border-radius:15px;
                ">
                {ai_questions}
                </div>
                ''',
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.subheader("🏆 Candidate Ranking")

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="ATS Score",
        ascending=False
    )

    st.dataframe(
        df,
        use_container_width=True
    )