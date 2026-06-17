import streamlit as st
import pdfplumber

st.title("AI Resume & Job Description Matcher")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type="pdf"
)

job_description = st.text_area(
    "Paste Job Description Here"
)

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    skills = [
        "python",
        "sql",
        "excel",
        "power bi",
        "machine learning",
        "pandas",
        "numpy",
        "tableau",
        "streamlit",
        "statistics",
        "data analysis",
        "mysql",
        "git",
        "github"
    ]

    resume_skills = []

    for skill in skills:
        if skill in text:
            resume_skills.append(skill)

    jd_skills = []

    for skill in skills:
        if skill in job_description.lower():
            jd_skills.append(skill)

    matched_skills = list(
        set(resume_skills).intersection(set(jd_skills))
    )

    if len(jd_skills) > 0:
        score = int(
            (len(matched_skills) / len(jd_skills)) * 100
        )
    else:
        score = 0

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    st.subheader("Match Score")
st.success(f"{score}%")

st.progress(score / 100)

if score >= 80:
    st.success("Excellent Match! You are highly suitable for this role.")
elif score >= 60:
    st.warning("Good Match! Improve a few skills to increase compatibility.")
else:
    st.error("Low Match! Consider learning the missing skills.")

st.subheader("Matched Skills")
st.write(matched_skills)

st.subheader("Missing Skills")
st.write(missing_skills)

report = f"""
Match Score: {score}%

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}
"""

st.download_button(
    "Download Report",
    report,
    file_name="job_match_report.txt"
)