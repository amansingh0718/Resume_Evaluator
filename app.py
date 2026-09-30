import streamlit as st

from config.settings import APP_TITLE
from services.job_parser import parse_job_description
from services.resume_parser import parse_resume
from services.matcher import match_resume_to_job
from utils.file_reader import extract_text_from_uploaded_file
from ui.components import (
    inject_css,
    render_header,
    render_input_section,
    render_results,
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_header()

resume_file, job_description, analyze_clicked = render_input_section()

if analyze_clicked:
    if resume_file is None:
        st.error("Please upload a resume PDF or DOCX file.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste the job description.")
        st.stop()

    with st.status("Analyzing candidate profile...", expanded=False) as status:
        try:
            resume_text = extract_text_from_uploaded_file(resume_file)

            if not resume_text.strip():
                raise ValueError(
                    "Could not extract text from the uploaded resume."
                )

            status.update(label="Parsing job description...", state="running")
            job = parse_job_description(job_description)

            status.update(label="Parsing resume...", state="running")
            resume = parse_resume(resume_text)

            status.update(label="Calculating profile match...", state="running")
            result = match_resume_to_job(job, resume)

            status.update(label="Analysis complete", state="complete")
            st.session_state["analysis"] = {
                "job": job,
                "resume": resume,
                "result": result,
            }

        except Exception as exc:
            status.update(label="Analysis failed", state="error")
            st.error(f"Something went wrong: {exc}")

analysis = st.session_state.get("analysis")

if analysis:
    render_results(
        job=analysis["job"],
        resume=analysis["resume"],
        result=analysis["result"],
    )
