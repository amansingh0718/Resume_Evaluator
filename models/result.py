from pydantic import BaseModel, Field


class MatchDetails(BaseModel):
    candidate_name: str | None = None
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    experience_requirement_met: bool | None = None
    verdict: str = ""
    summary: str = ""


class MatchResult(BaseModel):
    score: float = 0.0
    details: MatchDetails
