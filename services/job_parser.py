from models.job import JobDescription
from services.llm_service import generate_json


JOB_SCHEMA = JobDescription.model_json_schema()

SYSTEM_PROMPT = f"""
You are an expert HR job-description parser.

Extract structured information from the supplied job description.

Return ONLY valid JSON matching this schema:
{JOB_SCHEMA}

Rules:
- Extract only information supported by the job description.
- Do not invent skills, experience, education, or responsibilities.
- If minimum experience is not mentioned, return null.
- If a list has no information, return an empty list.
"""


def parse_job_description(job_description: str) -> JobDescription:
    data = generate_json(
        SYSTEM_PROMPT,
        f"""
Analyze this job description:

{job_description}
""",
    )
    return JobDescription(**data)
