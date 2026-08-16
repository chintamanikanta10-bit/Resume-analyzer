from typing import List
from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    institution: str
    score: str


class Experience(BaseModel):
    role: str
    company: str
    duration: str


class Project(BaseModel):
    title: str
    description: str


class ResumeSchema(BaseModel):
    name: str
    email: str
    phone: str
    location: str

    skills: List[str]

    education: List[Education]

    experience: List[Experience]

    projects: List[Project]

    certifications: List[str]

    achievements: List[str]