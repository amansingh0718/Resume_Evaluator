import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 0%, #172554 0, transparent 32%),
                radial-gradient(circle at 90% 10%, #312e81 0, transparent 28%),
                #070b14;
            color: #e5e7eb;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            padding: 2.2rem;
            border: 1px solid rgba(148,163,184,.18);
            border-radius: 24px;
            background: rgba(15,23,42,.72);
            box-shadow: 0 20px 60px rgba(0,0,0,.25);
            margin-bottom: 1.5rem;
        }

        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: .3rem;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 1rem;
        }

        .card {
            background: rgba(15,23,42,.78);
            border: 1px solid rgba(148,163,184,.16);
            border-radius: 20px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }

        .score-card {
            text-align: center;
            padding: 1.8rem;
            border-radius: 24px;
            background: linear-gradient(
                145deg,
                rgba(30,41,59,.95),
                rgba(15,23,42,.9)
            );
            border: 1px solid rgba(96,165,250,.25);
        }

        .score {
            font-size: 4.5rem;
            line-height: 1;
            font-weight: 900;
        }

        .score-label {
            color: #94a3b8;
            margin-top: .5rem;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 750;
            margin: .5rem 0 1rem;
        }

        .badge {
            display: inline-block;
            padding: .35rem .7rem;
            margin: .2rem;
            border-radius: 999px;
            background: rgba(59,130,246,.14);
            border: 1px solid rgba(96,165,250,.25);
            color: #bfdbfe;
            font-size: .85rem;
        }

        .missing {
            background: rgba(239,68,68,.12);
            border-color: rgba(248,113,113,.25);
            color: #fecaca;
        }

        .metric-card {
            padding: 1rem;
            border-radius: 16px;
            background: rgba(30,41,59,.65);
            border: 1px solid rgba(148,163,184,.12);
        }

        .metric-title {
            color: #94a3b8;
            font-size: .82rem;
        }

        .metric-value {
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: .25rem;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 0;
            padding: .7rem 1rem;
            font-weight: 750;
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            color: white;
        }

        textarea, input {
            border-radius: 12px !important;
        }

        [data-testid="stFileUploader"] {
            border-radius: 16px;
        }

        .small-muted {
            color: #94a3b8;
            font-size: .9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">🎯 AI Resume Match Analyzer</div>
            <div class="hero-subtitle">
                Analyze how closely a candidate profile matches a job description
                using structured LLM-based resume intelligence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_section():
    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown('<div class="section-title">📄 Candidate Resume</div>',
                    unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx"],
            label_visibility="collapsed",
        )
        st.caption("Supported formats: PDF, DOCX")

    with right:
        st.markdown('<div class="section-title">💼 Job Description</div>',
                    unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste Job Description",
            height=245,
            placeholder="Paste the complete job description here...",
            label_visibility="collapsed",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Analyze Resume Match")

    return resume_file, job_description, analyze_clicked


def _badges(items, missing=False):
    if not items:
        return '<span class="small-muted">None identified</span>'

    css_class = "badge missing" if missing else "badge"
    return "".join(
        f'<span class="{css_class}">{item}</span>' for item in items
    )


def render_results(job, resume, result):
    details = result.details
    score = max(0, min(100, result.score))

    st.markdown("---")
    st.markdown(
        '<div class="section-title">📊 Match Analysis</div>',
        unsafe_allow_html=True,
    )

    score_col, info_col = st.columns([0.7, 1.3], gap="large")

    with score_col:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score">{score:.0f}%</div>
                <div class="score-label">PROFILE MATCH</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with info_col:
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Candidate</div>
                    <div class="metric-value">
                        {resume.name or "Not available"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            experience = (
                "Met"
                if details.experience_requirement_met is True
                else "Not Met"
                if details.experience_requirement_met is False
                else "Not specified"
            )
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Experience Requirement</div>
                    <div class="metric-value">{experience}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Verdict</div>
                    <div class="metric-value">{details.verdict or "—"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if details.summary:
            st.markdown(
                f'<div class="card"><b>Assessment</b><br>{details.summary}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    match_col, missing_col = st.columns(2, gap="large")

    with match_col:
        st.markdown(
            """
            <div class="card">
                <div class="section-title">✅ Matching Skills</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            _badges(details.matching_skills),
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with missing_col:
        st.markdown(
            """
            <div class="card">
                <div class="section-title">⚠️ Missing Important Skills</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            _badges(details.missing_skills, missing=True),
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-title">💼 Job Requirement Analysis</div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            '<div class="card"><b>Role</b><br>'
            f'{job.role or "Not specified"}</div>',
            unsafe_allow_html=True,
        )

    with b:
        skills = ", ".join(job.required_skills) or "None specified"
        st.markdown(
            '<div class="card"><b>Required Skills</b><br>'
            f'{skills}</div>',
            unsafe_allow_html=True,
        )

    with c:
        exp = (
            f"{job.minimum_experience:g} years"
            if job.minimum_experience is not None
            else "Not specified"
        )
        st.markdown(
            '<div class="card"><b>Minimum Experience</b><br>'
            f'{exp}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("View Parsed Candidate Profile"):
        st.json(resume.model_dump())

    with st.expander("View Parsed Job Description"):
        st.json(job.model_dump())
