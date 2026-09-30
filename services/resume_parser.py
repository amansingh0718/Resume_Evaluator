from models.resume import Resume
from services.llm_service import generate_json


RESUME_SCHEMA = Resume.model_json_schema()

SYSTEM_PROMPT = f"""
You are an expert resume parser.

Extract structured information from the resume based on meaning,
not only exact section headings.

Possible experience headings include:
- Experience
- Professional Experience
- Work History
- Employment
- Internships

Skills can appear in skills, experience, internships, projects,
or certifications.

Return ONLY valid JSON matching this schema:
{RESUME_SCHEMA}

Rules:
1. Do not invent information.
2. If a scalar value is unavailable, return null.
3. If a list has no information, return an empty list.
4. Include internships inside experiences.
5. Extract relevant skills from the entire resume.
"""


def parse_resume(resume_text: str) -> Resume:
    data = generate_json(
        SYSTEM_PROMPT,
        f"""
Parse the following resume:

{resume_text}
""",
    )
    return Resume(**data)
