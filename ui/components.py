import html

import streamlit as st

GREEN = "#12946b"
AMBER = "#d18a0b"
RED = "#d64545"


def _html(markup: str) -> str:
    """Flatten markup so Streamlit's markdown never treats it as a code block."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


def _esc(value) -> str:
    return html.escape(str(value)) if value is not None else ""


def inject_css():
    st.markdown(
        """
        <style>
        :root { color-scheme: light; }

        .stApp { background: #f6f7fb; color: #111827; }
        .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3 {
            color: #111827;
        }
        #MainMenu, footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent; }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }
        section[data-testid="stSidebar"] .block-container,
        section[data-testid="stSidebar"] > div > div {
            padding-top: 1.2rem;
        }
        .brand {
            display: flex; align-items: center; gap: .55rem;
            font-weight: 700; font-size: 1.1rem; color: #111827;
            margin-bottom: .2rem;
        }
        .brand-icon {
            width: 34px; height: 34px; border-radius: 10px;
            background: #eef2ff; display: flex;
            align-items: center; justify-content: center; font-size: 1.1rem;
        }
        .brand-sub { color: #6b7280; font-size: .82rem; margin-bottom: 1.1rem; }
        .field-label {
            font-size: .78rem; font-weight: 600; color: #4b5563;
            text-transform: uppercase; letter-spacing: .04em;
            margin: .9rem 0 .35rem;
        }

        [data-testid="stFileUploader"] section {
            background: #f9fafb;
            border: 1.5px dashed #cbd5e1;
            border-radius: 12px;
        }
        [data-testid="stFileUploader"] section:hover { border-color: #6366f1; }
        [data-testid="stFileUploader"] small { color: #6b7280; }

        textarea {
            border-radius: 12px !important;
            background: #f9fafb !important;
            color: #111827 !important;
            border: 1px solid #e5e7eb !important;
        }
        textarea:focus { border-color: #6366f1 !important; }

        button[kind="primary"],
        [data-testid="stBaseButton-primary"] {
            width: 100%;
            border: 0;
            border-radius: 10px;
            padding: .6rem 1rem;
            font-weight: 600;
            background: #111827;
            color: #ffffff;
            transition: background .15s ease, transform .05s ease;
        }
        button[kind="primary"]:hover,
        [data-testid="stBaseButton-primary"]:hover {
            background: #312e81; color: #ffffff; border: 0;
        }
        button[kind="primary"]:active,
        [data-testid="stBaseButton-primary"]:active { transform: scale(.98); }

        /* ---------- Main area ---------- */
        .page-title { font-size: 1.6rem; font-weight: 700; margin: 0; }
        .page-sub { color: #6b7280; font-size: .95rem; margin: .2rem 0 1.2rem; }

        .empty {
            text-align: center; padding: 4rem 1.5rem;
            background: #ffffff; border: 1px dashed #d1d5db;
            border-radius: 16px; margin-top: 1rem;
        }
        .empty-icon { font-size: 2.4rem; margin-bottom: .5rem; }
        .empty-title { font-size: 1.15rem; font-weight: 650; margin-bottom: .3rem; }
        .empty-text { color: #6b7280; font-size: .95rem; }
        .steps { display: flex; gap: .75rem; justify-content: center;
                 margin-top: 1.6rem; flex-wrap: wrap; }
        .step {
            background: #f3f4f6; border-radius: 999px;
            padding: .4rem .9rem; font-size: .85rem; color: #374151;
        }

        .card {
            background: #ffffff; border: 1px solid #e5e7eb;
            border-radius: 14px; padding: 1rem 1.15rem; margin-bottom: .9rem;
        }
        .card-title {
            font-size: .95rem; font-weight: 650; margin-bottom: .6rem;
        }
        .card-text { color: #4b5563; font-size: .95rem; line-height: 1.6; }

        .hero-score {
            display: flex; align-items: center; gap: 1.4rem;
            background: #ffffff; border: 1px solid #e5e7eb;
            border-radius: 16px; padding: 1.3rem 1.5rem; margin-bottom: 1rem;
        }
        .ring {
            width: 108px; height: 108px; border-radius: 50%; flex: none;
            display: flex; align-items: center; justify-content: center;
        }
        .ring-inner {
            width: 82px; height: 82px; border-radius: 50%; background: #ffffff;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.7rem; font-weight: 750;
        }
        .hero-name { font-size: 1.3rem; font-weight: 700; }
        .hero-role { color: #6b7280; font-size: .92rem; margin: .1rem 0 .55rem; }
        .pill {
            display: inline-block; padding: .25rem .75rem; border-radius: 999px;
            font-size: .82rem; font-weight: 600;
        }

        .metric {
            background: #ffffff; border: 1px solid #e5e7eb;
            border-radius: 12px; padding: .8rem 1rem; margin-bottom: .9rem;
        }
        .metric-title { color: #6b7280; font-size: .78rem; }
        .metric-value { font-size: 1.25rem; font-weight: 700; margin-top: .15rem; }

        .bar { height: 8px; border-radius: 999px; background: #e5e7eb; overflow: hidden; }
        .bar > div { height: 100%; border-radius: 999px; }
        .bar-caption {
            display: flex; justify-content: space-between;
            color: #6b7280; font-size: .8rem; margin-top: .4rem;
        }

        .badge {
            display: inline-block; padding: .3rem .7rem; margin: .18rem .25rem .18rem 0;
            border-radius: 999px; font-size: .83rem; font-weight: 500;
            background: #e6f6f0; color: #0b6b4d;
        }
        .badge.missing { background: #fdecec; color: #a52a2a; }
        .badge.neutral { background: #eef2ff; color: #3730a3; }
        .muted { color: #9ca3af; font-size: .9rem; }

        button[data-baseweb="tab"] { font-weight: 600; }
        [data-testid="stExpander"] {
            background: #ffffff; border-radius: 12px; border: 1px solid #e5e7eb;
        }

        @media (max-width: 720px) {
            .hero-score { flex-direction: column; text-align: center; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        _html(
            """
            <div class="page-title">Resume Match Analysis</div>
            <div class="page-sub">
                See how closely a candidate profile fits a job description.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    if not st.session_state.get("analysis"):
        st.markdown(
            _html(
                """
                <div class="empty">
                    <div class="empty-icon">🎯</div>
                    <div class="empty-title">Ready when you are</div>
                    <div class="empty-text">
                        Add a resume and a job description in the sidebar,
                        then run the analysis.
                    </div>
                    <div class="steps">
                        <span class="step">1 · Upload resume</span>
                        <span class="step">2 · Paste job description</span>
                        <span class="step">3 · Analyze match</span>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


def render_input_section():
    with st.sidebar:
        st.markdown(
            _html(
                """
                <div class="brand">
                    <div class="brand-icon">🎯</div>Match Analyzer
                </div>
                <div class="brand-sub">AI-powered resume screening</div>
                """
            ),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="field-label">Resume</div>',
                    unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx"],
            label_visibility="collapsed",
        )
        st.caption("PDF or DOCX")

        st.markdown('<div class="field-label">Job description</div>',
                    unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste Job Description",
            height=240,
            placeholder="Paste the complete job description here...",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        analyze_clicked = st.button("Analyze match", type="primary")

    return resume_file, job_description, analyze_clicked


def _badges(items, kind=""):
    if not items:
        return '<span class="muted">None identified</span>'

    css_class = f"badge {kind}".strip()
    return "".join(
        f'<span class="{css_class}">{_esc(item)}</span>' for item in items
    )


def _tone(score):
    if score >= 75:
        return GREEN, "#e6f6f0", "Strong fit"
    if score >= 50:
        return AMBER, "#fdf3dc", "Partial fit"
    return RED, "#fdecec", "Weak fit"


def _metric(title, value, color=None):
    style = f' style="color:{color}"' if color else ""
    return _html(
        f"""
        <div class="metric">
            <div class="metric-title">{_esc(title)}</div>
            <div class="metric-value"{style}>{_esc(value)}</div>
        </div>
        """
    )


def render_results(job, resume, result):
    details = result.details
    score = max(0, min(100, result.score))
    color, tint, fit_label = _tone(score)

    candidate = resume.name or details.candidate_name or "Candidate"
    role = job.role or "Role not specified"

    if details.experience_requirement_met is True:
        experience, exp_color = "Met", GREEN
    elif details.experience_requirement_met is False:
        experience, exp_color = "Not met", RED
    else:
        experience, exp_color = "Not specified", None

    matched = len(details.matching_skills)
    missing = len(details.missing_skills)
    total = matched + missing
    coverage = round(matched / total * 100) if total else 0

    overview_tab, skills_tab, data_tab = st.tabs(
        ["Overview", "Skills", "Parsed data"]
    )

    with overview_tab:
        st.markdown(
            _html(
                f"""
                <div class="hero-score">
                    <div class="ring"
                         style="background: conic-gradient({color} {score * 3.6}deg, #e5e7eb 0);">
                        <div class="ring-inner" style="color:{color}">{score:.0f}%</div>
                    </div>
                    <div>
                        <div class="hero-name">{_esc(candidate)}</div>
                        <div class="hero-role">{_esc(role)}</div>
                        <span class="pill" style="background:{tint}; color:{color}">
                            {fit_label}
                        </span>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                _metric("Experience requirement", experience, exp_color),
                unsafe_allow_html=True,
            )
        with c2:
            min_exp = (
                f"{job.minimum_experience:g} years"
                if job.minimum_experience is not None
                else "Not specified"
            )
            st.markdown(_metric("Minimum experience", min_exp),
                        unsafe_allow_html=True)
        with c3:
            st.markdown(_metric("Verdict", details.verdict or "—"),
                        unsafe_allow_html=True)

        if total:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">Skill coverage</div>
                        <div class="bar">
                            <div style="width:{coverage}%; background:{color}"></div>
                        </div>
                        <div class="bar-caption">
                            <span>{matched} of {total} key skills matched</span>
                            <span>{coverage}%</span>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

        if details.summary:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">Assessment</div>
                        <div class="card-text">{_esc(details.summary)}</div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

    with skills_tab:
        left, right = st.columns(2, gap="medium")

        with left:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">✅ Matching skills ({matched})</div>
                        {_badges(details.matching_skills)}
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">⚠️ Missing important skills ({missing})</div>
                        {_badges(details.missing_skills, "missing")}
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

        req, pref = st.columns(2, gap="medium")
        with req:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">Required by the job</div>
                        {_badges(job.required_skills, "neutral")}
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )
        with pref:
            st.markdown(
                _html(
                    f"""
                    <div class="card">
                        <div class="card-title">Preferred by the job</div>
                        {_badges(job.preferred_skills, "neutral")}
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

    with data_tab:
        with st.expander("Parsed candidate profile", expanded=False):
            st.json(resume.model_dump())

        with st.expander("Parsed job description", expanded=False):
            st.json(job.model_dump())
