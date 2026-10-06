import streamlit as st
import json

from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_matcher import find_matching_skills


with open("data/skills.json", "r") as file:

    skills_data = json.load(file)

st.set_page_config(
    page_title="Resume Lens",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Resume Lens")

st.write(
    "Check which job skills are present in your resume."
)

st.sidebar.title("Resume Lens")

st.sidebar.write(
    "Upload your resume and compare it "
    "with a job requirement."
)

st.sidebar.text_input(
    "Enter Your Name"
)

resume = st.file_uploader("Upload your resume",type=["pdf"])

job = st.text_area(
    "Paste company job requirement",
    height=200,
    placeholder="Paste the job description here..."
)


if st.button("🔍 Analyze Resume"):

  
    if resume is None:

        st.warning(
            "Please upload your resume."
        )

  
    elif job.strip() == "":

        st.warning(
            "Please enter the job requirement."
        )

    else:

        resume_text = extract_text_from_pdf(
            resume
        )
        resume_text = clean_text(
            resume_text
        )

        job_text = clean_text(
            job
        )

        job_skills = []

        for category, skills in skills_data.items():

            for skill in skills:

                if skill in job_text:

                    job_skills.append(skill)

        job_skills = list(
            dict.fromkeys(job_skills)
        )
        if len(job_skills) == 0:

            st.warning(
                "No known skills were found "
                "in the job description."
            )

        else:
            found, missing = find_matching_skills(
                job_skills,
                resume_text
            )

            score = (len(found) /len(job_skills) ) * 100

            score = round(score)


            st.subheader(
                "📊 Resume Analysis"
            )

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Match Score",
                    f"{score}%"
                )


            with col2:

                st.metric(
                    "Skills Found",
                    len(found)
                )


            with col3:

                st.metric(
                    "Skills Missing",
                    len(missing)
                )

            st.progress(
                score / 100
            )

            if score >= 80:

                st.success(
                    "🔥 Strong Match"
                )

            elif score >= 60:

                st.warning(
                    "⚡ Moderate Match"
                )

            else:

                st.error(
                    "📚 Needs Improvement"
                )

            tab1, tab2, tab3 = st.tabs(
                [
                    "📋 Job Skills",
                    "🟢 Skills Found",
                    "🔴 Skills Missing"
                ]
            )

            with tab1:

                st.subheader(
                    "Skills found in Job Requirement"
                )

                for skill in job_skills:

                    st.write(
                        "•",
                        skill
                    )

            with tab2:

                st.subheader(
                    "Skills found in your Resume"
                )

                if len(found) == 0:

                    st.info(
                        "No matching skills found."
                    )

                else:

                    for skill in found:

                        st.success(
                            skill
                        )

            with tab3:

                st.subheader(
                    "Skills missing from your Resume"
                )

                if len(missing) == 0:

                    st.success(
                        "🎉 No important skills are missing."
                    )

                else:

                    for skill in missing:

                        st.error(
                            skill
                        )