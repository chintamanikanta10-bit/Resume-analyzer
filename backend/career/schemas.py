from typing import List
from pydantic import BaseModel, Field


class RecommendedProject(BaseModel):
    title: str
    description: str = ""
    technologies: List[str] = Field(default_factory=list)


class WeeklyPlanItem(BaseModel):
    week: int
    focus: str
    topics: List[str] = Field(default_factory=list)


class CareerRoadmap(BaseModel):
    target_role: str

    current_strengths: List[str] = Field(
        default_factory=list
    )

    skills_to_learn: List[str] = Field(
        default_factory=list
    )

    recommended_projects: List[RecommendedProject] = Field(
        default_factory=list
    )

    recommended_certifications: List[str] = Field(
        default_factory=list
    )

    learning_resources: List[str] = Field(
        default_factory=list
    )

    weekly_plan: List[WeeklyPlanItem] = Field(
        default_factory=list
    )

    estimated_duration: str

    motivation: str