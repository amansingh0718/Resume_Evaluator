from models.job import JobDescription
from models.resume import Resume
from models.result import MatchResult
from services.llm_service import generate_json


RESULT_SCHEMA = MatchResult.model_json_schema()

SYSTEM_PROMPT = f"""
You are an expert technical recruiter.

Compare a candidate resume against a job description.

Return ONLY valid JSON matching this schema:
{RESULT_SCHEMA}

Scoring guidance:
- Return a score from 0 to 100.
- Consider required skills, preferred skills, experience,
  education, and relevant project/work evidence.
- Missing a critical required skill should materially reduce the score.
- Do not invent experience or skills.
- Keep the verdict concise.
- matching_skills should contain skills supported by the resume.
- missing_skills should contain important job skills not supported
  by the resume.
"""


def match_resume_to_job(
    job: JobDescription,
    resume: Resume,
) -> MatchResult:
    data = generate_json(
        SYSTEM_PROMPT,
        f"""
JOB DESCRIPTION:
{job.model_dump_json(indent=2)}

CANDIDATE RESUME:
{resume.model_dump_json(indent=2)}
""",
    )

    return MatchResult(**data)
